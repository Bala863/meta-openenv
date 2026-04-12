#!/usr/bin/env python3
"""
inference.py — EmailOps-Env Inference Script
Adhering to OpenEnv submission standards for validation.
"""

import asyncio
import os
import json
import textwrap
from typing import List, Optional

from openai import OpenAI

# We use the local environment for direct evaluation speed during validation,
# or we can use the HTTPClient if testing against a deployed space.
from emailops_env.server.email_environment import EmailEnvironment
from emailops_env.models import EmailAction, EmailState, EmailObservation

# OpenEnv Hackathon required environment variables
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/hf-inference/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

TASK_NAME = os.getenv("EMAILOPS_TASK", "email_operations")
BENCHMARK = os.getenv("EMAILOPS_BENCHMARK", "emailops_env")
MAX_STEPS = 3  # The environment always takes 3 steps: Intent, Extract, Respond
SUCCESS_SCORE_THRESHOLD = 0.5

SYSTEM_PROMPT = """You are an expert customer support AI agent. You process emails and perform tasks as instructed.
Always respond with valid JSON matching the required schema. Be precise and professional."""


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error is not None else "null"
    done_val = str(done).lower()
    # Replace newlines in action string to adhere to "no newlines within a line" rule
    action_single_line = action.replace('\n', '\\n').replace('\r', '')
    print(
        f"[STEP] step={step} action={action_single_line} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)


def agent_classify_intent(client: OpenAI, obs: EmailObservation) -> str:
    prompt = f"""Classify the intent of the following email into exactly ONE of these categories:
- billing
- technical_support
- complaint
- general_query
- account_issue
- shipping
- refund_request
- feedback

Email From: {obs.email_from}
Email Subject: {obs.email_subject}
Email Body:
{obs.email_body}

Respond with ONLY a JSON object: {{"intent": "<category>"}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=60,
        response_format={"type": "json_object"},
    )
    return (response.choices[0].message.content or "").strip()


def agent_extract_info(client: OpenAI, obs: EmailObservation) -> str:
    prompt = f"""Extract the following information from this email. If a field is not present, use an empty string.

Fields to extract:
- order_id: Any order, invoice, account, or reference number
- customer_name: The sender's full name
- issue_description: A concise description of the issue or request
- product_name: Any product or service mentioned
- requested_resolution: What the customer wants done
- urgency_level: One of "low", "medium", "high", "critical"
- email_address: The sender's email address

Email From: {obs.email_from}
Email Subject: {obs.email_subject}
Email Body:
{obs.email_body}

Respond with ONLY a JSON object containing all fields listed above."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=500,
        response_format={"type": "json_object"},
    )
    return (response.choices[0].message.content or "").strip()


def agent_generate_response(client: OpenAI, obs: EmailObservation, history: List[dict]) -> str:
    # Get previous actions for context
    intent_json = history[0] if len(history) > 0 else {}
    extracted_json = history[1] if len(history) > 1 else {}
    
    prompt = f"""Draft a professional email response to the following customer email.

Context:
- Intent: {intent_json.get('intent', 'unknown')}
- Customer: {extracted_json.get('customer_name', 'Customer')}
- Order/Reference: {extracted_json.get('order_id', 'N/A')}
- Issue: {extracted_json.get('issue_description', obs.email_subject)}
- Requested Resolution: {extracted_json.get('requested_resolution', 'Not specified')}
- Urgency: {extracted_json.get('urgency_level', 'medium')}

Original Email From: {obs.email_from}
Original Subject: {obs.email_subject}
Original Body:
{obs.email_body}

Requirements:
1. Address the customer by name
2. Acknowledge their specific issue
3. Provide clear resolution or next steps
4. Be professional, empathetic where appropriate
5. Include relevant reference numbers
6. Keep it concise but complete (100-250 words)

Respond with ONLY a JSON object: {{"response_text": "<your complete email response>"}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=800,
        response_format={"type": "json_object"},
    )
    return (response.choices[0].message.content or "").strip()


async def main() -> None:
    HF_TOKEN = os.getenv("HF_TOKEN")

    if HF_TOKEN is None:
        raise ValueError("HF_TOKEN environment variable is required")

    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

    # Creating a local instance of the environment for inference validation
    # This avoids the overhead of managing a WebSocket connection just for local validation
    env = EmailEnvironment(seed=42)

    rewards: List[float] = []
    actions_history: List[dict] = []
    steps_taken = 0
    score = 0.0
    success = False

    try:
        obs = env.reset()
        
        for step in range(1, MAX_STEPS + 1):
            if obs.done:
                break
                
            error = None
            action_log_str = ""
            action_obj = EmailAction()
            
            # Let the OpenEnv validator know we are starting a specific task evaluation
            current_task_name = obs.task_name
            log_start(task=current_task_name, env=BENCHMARK, model=MODEL_NAME)
            
            try:
                if obs.task_id == 1:
                    raw_action = agent_classify_intent(client, obs)
                    action_log_str = raw_action
                    action_dict = json.loads(raw_action)
                    actions_history.append(action_dict)
                    action_obj.intent = action_dict.get("intent", "")
                    
                elif obs.task_id == 2:
                    raw_action = agent_extract_info(client, obs)
                    action_log_str = raw_action
                    action_dict = json.loads(raw_action)
                    actions_history.append(action_dict)
                    action_obj.order_id = action_dict.get("order_id", "")
                    action_obj.customer_name = action_dict.get("customer_name", "")
                    action_obj.issue_description = action_dict.get("issue_description", "")
                    action_obj.product_name = action_dict.get("product_name", "")
                    action_obj.requested_resolution = action_dict.get("requested_resolution", "")
                    action_obj.urgency_level = action_dict.get("urgency_level", "")
                    action_obj.email_address = action_dict.get("email_address", "")
                    
                elif obs.task_id == 3:
                    raw_action = agent_generate_response(client, obs, actions_history)
                    action_log_str = raw_action
                    action_dict = json.loads(raw_action)
                    actions_history.append(action_dict)
                    action_obj.response_text = action_dict.get("response_text", "")
                    
            except Exception as e:
                error = str(e)
                action_log_str = f"Error generating action: {error}"

            # Step the environment
            step_res = env.step(action_obj)
            next_obs = step_res["observation"]
            reward = step_res["reward"]
            
            # Log as a distinct 1-step episode for the validator
            log_step(step=1, action=action_log_str, reward=reward, done=True, error=error)
            
            step_success = reward >= SUCCESS_SCORE_THRESHOLD
            log_end(success=step_success, steps=1, rewards=[reward])
            
            obs = next_obs

    except Exception as general_error:
        print(f"[DEBUG] Execution error: {general_error}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
