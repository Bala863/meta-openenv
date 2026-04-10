"""
EmailOps-Env: Core environment logic implementing the OpenEnv Environment interface.
Manages episodes, task progression, and grading for email operations.
"""

import uuid
import random as _random
from dataclasses import asdict

from emailops_env.models import EmailAction, EmailObservation, EmailState
from emailops_env.server.email_data import EMAILS, get_email_by_id
from emailops_env.server.graders import grade_intent, grade_extraction, grade_response


TASK_DEFINITIONS = {
    1: {
        "name": "Intent Classification",
        "instruction": (
            "Classify the intent of this email into exactly one category: "
            "billing, technical_support, complaint, general_query, account_issue, "
            "shipping, refund_request, or feedback. "
            "Set the 'intent' field in your action."
        ),
    },
    2: {
        "name": "Information Extraction",
        "instruction": (
            "Extract the following structured fields from the email: "
            "order_id, customer_name, issue_description, product_name, "
            "requested_resolution, urgency_level (low/medium/high/critical), "
            "and email_address. Set each field in your action."
        ),
    },
    3: {
        "name": "Full Response Generation",
        "instruction": (
            "Draft a complete, professional email response that: "
            "(1) addresses the customer by name, "
            "(2) acknowledges their specific issue, "
            "(3) provides a clear resolution or next steps, "
            "(4) maintains a professional and empathetic tone, "
            "(5) includes relevant reference numbers. "
            "Set the 'response_text' field in your action."
        ),
    },
}


class EmailEnvironment:
    """
    OpenEnv-compliant Environment for email operations.

    Supports three tasks of increasing difficulty:
      Task 1 — Intent Classification
      Task 2 — Information Extraction
      Task 3 — Full Response Generation

    The environment progresses through tasks sequentially within an episode:
      reset() → Task 1 → step() → Task 2 → step() → Task 3 → step() → done
    """

    def __init__(self, seed: int | None = None):
        self._rng = _random.Random(seed)
        self._state: EmailState | None = None
        self._current_email: dict | None = None
        self._task_order = [1, 2, 3]

    def reset(self, email_id: str | None = None) -> EmailObservation:
        """
        Initialize a new episode with a random or specified email.
        Returns the initial observation with the email content and Task 1 instructions.
        """
        # Select email
        if email_id and get_email_by_id(email_id):
            self._current_email = get_email_by_id(email_id)
        else:
            self._current_email = self._rng.choice(EMAILS)

        episode_id = str(uuid.uuid4())[:8]

        self._state = EmailState(
            episode_id=episode_id,
            email_id=self._current_email["id"],
            current_task_id=1,
            step_count=0,
            total_score=0.0,
            task_scores={},
            done=False,
            max_steps=10,
        )

        task_def = TASK_DEFINITIONS[1]

        return EmailObservation(
            email_subject=self._current_email["subject"],
            email_body=self._current_email["body"],
            email_from=self._current_email["from"],
            email_date=self._current_email["date"],
            task_id=1,
            task_name=task_def["name"],
            task_instruction=task_def["instruction"],
            score=0.0,
            feedback="Episode started. Complete Task 1: Intent Classification.",
            done=False,
            episode_id=episode_id,
            step_count=0,
            email_id=self._current_email["id"],
        )

    def step(self, action: EmailAction) -> dict:
        """
        Execute an action and return a StepResult dict with:
          - observation: EmailObservation
          - reward: float (0.0–1.0)
          - done: bool
          - info: dict with metadata
        """
        if self._state is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")

        if self._state.done:
            return {
                "observation": EmailObservation(
                    email_subject=self._current_email["subject"],
                    email_body=self._current_email["body"],
                    email_from=self._current_email["from"],
                    email_date=self._current_email["date"],
                    task_id=self._state.current_task_id,
                    task_name="Episode Complete",
                    task_instruction="This episode is complete. Call reset() to start a new one.",
                    score=self._state.total_score,
                    feedback="Episode already complete.",
                    done=True,
                    episode_id=self._state.episode_id,
                    step_count=self._state.step_count,
                    email_id=self._state.email_id,
                ),
                "reward": 0.0,
                "done": True,
                "info": {"task_scores": self._state.task_scores},
            }

        self._state.step_count += 1
        gt = self._current_email["ground_truth"]
        current_task = self._state.current_task_id

        # ── Grade based on current task ──────────────────────────────────
        if current_task == 1:
            score, feedback = grade_intent(action.intent, gt["intent"])
        elif current_task == 2:
            pred = {
                "order_id": action.order_id,
                "customer_name": action.customer_name,
                "issue_description": action.issue_description,
                "product_name": action.product_name,
                "requested_resolution": action.requested_resolution,
                "urgency_level": action.urgency_level,
                "email_address": action.email_address,
            }
            score, feedback = grade_extraction(pred, gt)
        elif current_task == 3:
            score, feedback = grade_response(action.response_text, gt, self._current_email)
        else:
            score, feedback = 0.0, "Unknown task."

        # Record score
        self._state.task_scores[f"task_{current_task}"] = score
        self._state.total_score += score

        # ── Advance to next task or finish ───────────────────────────────
        task_idx = self._task_order.index(current_task)
        if task_idx < len(self._task_order) - 1:
            next_task = self._task_order[task_idx + 1]
            self._state.current_task_id = next_task
            task_def = TASK_DEFINITIONS[next_task]
            done = False
            next_instruction = task_def["instruction"]
            next_task_name = task_def["name"]
            feedback += f"\n\nMoving to Task {next_task}: {next_task_name}."
        else:
            done = True
            self._state.done = True
            self._state.total_score = round(self._state.total_score / 3.0, 4)
            next_instruction = "All tasks complete. Episode finished."
            next_task_name = "Episode Complete"
            feedback += f"\n\nAll tasks complete! Final average score: {self._state.total_score:.4f}"

        observation = EmailObservation(
            email_subject=self._current_email["subject"],
            email_body=self._current_email["body"],
            email_from=self._current_email["from"],
            email_date=self._current_email["date"],
            task_id=self._state.current_task_id,
            task_name=next_task_name,
            task_instruction=next_instruction,
            score=score,
            feedback=feedback,
            done=done,
            episode_id=self._state.episode_id,
            step_count=self._state.step_count,
            email_id=self._state.email_id,
        )

        return {
            "observation": observation,
            "reward": score,
            "done": done,
            "info": {
                "task_scores": dict(self._state.task_scores),
                "average_score": self._state.total_score if done else None,
            },
        }

    def state(self) -> EmailState | None:
        """Return the current internal state of the environment."""
        return self._state
