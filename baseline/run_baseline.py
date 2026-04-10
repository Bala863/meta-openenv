#!/usr/bin/env python3
"""
EmailOps-Env: Baseline inference script using OpenAI's API.
Demonstrates how an AI agent interacts with the environment across all 3 tasks.

Usage:
    export OPENAI_API_KEY="sk-..."
    python baseline/run_baseline.py [--base-url http://localhost:7860] [--num-episodes 5]
"""

import os
import sys
import json
import argparse
import httpx
import time

# ── OpenAI setup ─────────────────────────────────────────────────────────────

def get_openai_client():
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ Set OPENAI_API_KEY environment variable")
        sys.exit(1)

    if api_key.startswith("gsk_"):
        # Use Groq OpenAI-compatible endpoint
        return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1"), "llama-3.3-70b-versatile"
    else:
        return OpenAI(api_key=api_key), "gpt-4o-mini"



# ── Agent logic ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert customer support AI agent. You process emails and perform tasks as instructed.
Always respond with valid JSON matching the required schema. Be precise and professional."""


def agent_classify_intent(client, model_name: str, email_subject: str, email_body: str, email_from: str) -> dict:
    """Task 1: Use GPT to classify the email intent."""
    prompt = f"""Classify the intent of the following email into exactly ONE of these categories:
- billing
- technical_support
- complaint
- general_query
- account_issue
- shipping
- refund_request
- feedback

Email From: {email_from}
Email Subject: {email_subject}
Email Body:
{email_body}

Respond with ONLY a JSON object: {{"intent": "<category>"}}"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=50,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, IndexError):
        return {"intent": "general_query"}


def agent_extract_info(client, model_name: str, email_subject: str, email_body: str, email_from: str) -> dict:
    """Task 2: Use GPT to extract structured information."""
    prompt = f"""Extract the following information from this email. If a field is not present, use an empty string.

Fields to extract:
- order_id: Any order, invoice, account, or reference number
- customer_name: The sender's full name
- issue_description: A concise description of the issue or request
- product_name: Any product or service mentioned
- requested_resolution: What the customer wants done
- urgency_level: One of "low", "medium", "high", "critical"
- email_address: The sender's email address

Email From: {email_from}
Email Subject: {email_subject}
Email Body:
{email_body}

Respond with ONLY a JSON object containing all fields listed above."""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        max_tokens=500,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, IndexError):
        return {}


def agent_generate_response(client, model_name: str, email_subject: str, email_body: str, email_from: str, intent: str, extracted: dict) -> dict:
    """Task 3: Use GPT to generate a professional email response."""
    prompt = f"""Draft a professional email response to the following customer email.

Context:
- Intent: {intent}
- Customer: {extracted.get('customer_name', 'Customer')}
- Order/Reference: {extracted.get('order_id', 'N/A')}
- Issue: {extracted.get('issue_description', email_subject)}
- Requested Resolution: {extracted.get('requested_resolution', 'Not specified')}
- Urgency: {extracted.get('urgency_level', 'medium')}

Original Email From: {email_from}
Original Subject: {email_subject}
Original Body:
{email_body}

Requirements:
1. Address the customer by name
2. Acknowledge their specific issue
3. Provide clear resolution or next steps
4. Be professional, empathetic where appropriate
5. Include relevant reference numbers
6. Keep it concise but complete (100-250 words)

Respond with ONLY a JSON object: {{"response_text": "<your complete email response>"}}"""

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=800,
        response_format={"type": "json_object"},
    )
    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, IndexError):
        return {"response_text": ""}


# ── Main loop ────────────────────────────────────────────────────────────────

def run_episode(openai_client, model_name: str, http_client: httpx.Client, base_url: str, email_id: str | None = None):
    """Run a single episode through all 3 tasks."""
    print(f"\n{'='*70}")
    print(f"Starting new episode...")
    print(f"{'='*70}")

    # Reset
    reset_payload = {}
    if email_id:
        reset_payload["email_id"] = email_id
    resp = http_client.post(f"{base_url}/reset", json=reset_payload)
    resp.raise_for_status()
    data = resp.json()
    session_id = data["session_id"]
    obs = data["observation"]

    email_subject = obs["email_subject"]
    email_body = obs["email_body"]
    email_from = obs["email_from"]

    print(f"\nEmail: {email_subject}")
    print(f"   From: {email_from}")
    print(f"   Email ID: {obs['email_id']}")

    task_scores = {}
    intent_result = {}
    extraction_result = {}

    # ── Task 1: Intent Classification ──────────────────────────
    print(f"\nTask 1: {obs['task_name']}")
    t1_start = time.time()
    intent_result = agent_classify_intent(openai_client, model_name, email_subject, email_body, email_from)
    t1_time = time.time() - t1_start

    action_1 = {"intent": intent_result.get("intent", "general_query")}
    print(f"   Agent predicted: {action_1['intent']} ({t1_time:.2f}s)")

    resp = http_client.post(f"{base_url}/step/{session_id}", json=action_1)
    resp.raise_for_status()
    result_1 = resp.json()
    task_scores["task_1"] = result_1["reward"]
    print(f"   Score: {result_1['reward']:.4f}")

    obs = result_1["observation"]

    # ── Task 2: Information Extraction ─────────────────────────
    print(f"\nTask 2: {obs['task_name']}")
    t2_start = time.time()
    extraction_result = agent_extract_info(openai_client, model_name, email_subject, email_body, email_from)
    t2_time = time.time() - t2_start

    action_2 = {
        "order_id": extraction_result.get("order_id", ""),
        "customer_name": extraction_result.get("customer_name", ""),
        "issue_description": extraction_result.get("issue_description", ""),
        "product_name": extraction_result.get("product_name", ""),
        "requested_resolution": extraction_result.get("requested_resolution", ""),
        "urgency_level": extraction_result.get("urgency_level", ""),
        "email_address": extraction_result.get("email_address", ""),
    }
    print(f"   Extracted {sum(1 for v in action_2.values() if v)} fields ({t2_time:.2f}s)")

    resp = http_client.post(f"{base_url}/step/{session_id}", json=action_2)
    resp.raise_for_status()
    result_2 = resp.json()
    task_scores["task_2"] = result_2["reward"]
    print(f"   Score: {result_2['reward']:.4f}")

    obs = result_2["observation"]

    # ── Task 3: Response Generation ────────────────────────────
    print(f"\nTask 3: {obs['task_name']}")
    t3_start = time.time()
    response_result = agent_generate_response(
        openai_client, model_name, email_subject, email_body, email_from,
        intent_result.get("intent", ""), extraction_result
    )
    t3_time = time.time() - t3_start

    action_3 = {"response_text": response_result.get("response_text", "")}
    word_count = len(action_3["response_text"].split())
    print(f"   Generated {word_count} words ({t3_time:.2f}s)")

    resp = http_client.post(f"{base_url}/step/{session_id}", json=action_3)
    resp.raise_for_status()
    result_3 = resp.json()
    task_scores["task_3"] = result_3["reward"]
    print(f"   Score: {result_3['reward']:.4f}")

    # ── Summary ────────────────────────────────────────────────
    avg_score = sum(task_scores.values()) / 3
    print(f"\nEpisode Summary:")
    print(f"   Task 1 (Intent):     {task_scores['task_1']:.4f}")
    print(f"   Task 2 (Extraction): {task_scores['task_2']:.4f}")
    print(f"   Task 3 (Response):   {task_scores['task_3']:.4f}")
    print(f"   Average Score:       {avg_score:.4f}")
    print(f"   Total Time:          {t1_time + t2_time + t3_time:.2f}s")

    return task_scores


def main():
    parser = argparse.ArgumentParser(description="EmailOps-Env Baseline Agent (OpenAI/Groq)")
    parser.add_argument("--base-url", default="http://localhost:7860", help="Environment server URL")
    parser.add_argument("--num-episodes", type=int, default=5, help="Number of episodes to run")
    parser.add_argument("--email-ids", nargs="*", default=None, help="Specific email IDs to evaluate")
    args = parser.parse_args()

    openai_client, model_name = get_openai_client()
    http_client = httpx.Client(timeout=60.0)

    # Check server health
    try:
        health = http_client.get(f"{args.base_url}/health")
        health.raise_for_status()
        print(f"Connected to server: {health.json()}")
    except Exception as e:
        print(f"Cannot connect to server at {args.base_url}: {e}")
        print("   Start the server first: uvicorn emailops_env.server.app:app --port 7860")
        sys.exit(1)

    # Get available emails
    emails_resp = http_client.get(f"{args.base_url}/emails")
    available_emails = emails_resp.json()["email_ids"]
    print(f"Available emails: {len(available_emails)}")

    # Select emails to evaluate
    if args.email_ids:
        email_ids = args.email_ids
    else:
        email_ids = available_emails[:args.num_episodes]

    # Run episodes
    all_scores = []
    for i, eid in enumerate(email_ids):
        print(f"\n{'#'*70}")
        print(f"# Episode {i+1}/{len(email_ids)}")
        print(f"{'#'*70}")
        scores = run_episode(openai_client, model_name, http_client, args.base_url, eid)
        all_scores.append(scores)

    # ── Final Report ─────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"BASELINE RESULTS — {len(all_scores)} episodes")
    print(f"{'='*70}")

    avg_t1 = sum(s["task_1"] for s in all_scores) / len(all_scores)
    avg_t2 = sum(s["task_2"] for s in all_scores) / len(all_scores)
    avg_t3 = sum(s["task_3"] for s in all_scores) / len(all_scores)
    avg_total = (avg_t1 + avg_t2 + avg_t3) / 3

    print(f"  Task 1 — Intent Classification:  {avg_t1:.4f}")
    print(f"  Task 2 — Information Extraction:  {avg_t2:.4f}")
    print(f"  Task 3 — Response Generation:     {avg_t3:.4f}")
    print(f"  ─────────────────────────────────────")
    print(f"  Overall Average:                  {avg_total:.4f}")
    print(f"{'='*70}")

    # Save results
    results = {
        "model": model_name,
        "num_episodes": len(all_scores),
        "avg_task_1": round(avg_t1, 4),
        "avg_task_2": round(avg_t2, 4),
        "avg_task_3": round(avg_t3, 4),
        "avg_overall": round(avg_total, 4),
        "per_episode": all_scores,
    }

    os.makedirs("outputs/evals", exist_ok=True)
    results_path = "outputs/evals/baseline_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {results_path}")

    http_client.close()


if __name__ == "__main__":
    main()
