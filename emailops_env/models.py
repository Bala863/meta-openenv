"""
EmailOps-Env: Type-safe data models for the email operations environment.
Defines Action, Observation, and State dataclasses used across client and server.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EmailAction:
    """Action submitted by the agent at each step."""

    # Task 1: Intent Classification
    # One of: "billing", "technical_support", "complaint", "general_query",
    #         "account_issue", "shipping", "refund_request", "feedback"
    intent: str = ""

    # Task 2: Information Extraction (structured fields)
    order_id: str = ""
    customer_name: str = ""
    issue_description: str = ""
    product_name: str = ""
    requested_resolution: str = ""
    urgency_level: str = ""  # "low", "medium", "high", "critical"
    email_address: str = ""

    # Task 3: Full Response Generation
    response_text: str = ""


@dataclass
class EmailObservation:
    """Observation returned to the agent after each step or reset."""

    # The raw email content the agent must process
    email_subject: str = ""
    email_body: str = ""
    email_from: str = ""
    email_date: str = ""

    # Current task instruction
    task_id: int = 0  # 1, 2, or 3
    task_name: str = ""
    task_instruction: str = ""

    # Feedback from the grader (after a step)
    score: float = 0.0
    feedback: str = ""
    done: bool = False

    # Episode metadata
    episode_id: str = ""
    step_count: int = 0
    email_id: str = ""


@dataclass
class EmailState:
    """Internal state of the environment for a given episode."""

    episode_id: str = ""
    email_id: str = ""
    current_task_id: int = 0
    step_count: int = 0
    total_score: float = 0.0
    task_scores: dict = field(default_factory=dict)
    done: bool = False
    max_steps: int = 10
