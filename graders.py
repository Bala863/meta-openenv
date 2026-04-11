"""
EmailOps-Env: Deterministic grading functions for all three tasks.
Each grader returns a score strictly between 0.01 and 0.99 with detailed feedback.
"""

import re
from difflib import SequenceMatcher


def _normalize(text: str) -> str:
    """Normalize text for comparison: lowercase, strip, collapse whitespace."""
    return re.sub(r"\s+", " ", text.strip().lower())


def _similarity(a: str, b: str) -> float:
    """Compute string similarity ratio between two strings."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()


# ─────────────────────────────────────────────────────────────────────────────
# Task 1: Intent Classification Grader
# ─────────────────────────────────────────────────────────────────────────────

VALID_INTENTS = {
    "billing",
    "technical_support",
    "complaint",
    "general_query",
    "account_issue",
    "shipping",
    "refund_request",
    "feedback",
}

# Partial-credit mapping: some misclassifications are "closer" than others
INTENT_SIMILARITY = {
    ("billing", "refund_request"): 0.4,
    ("refund_request", "billing"): 0.4,
    ("complaint", "feedback"): 0.2,
    ("feedback", "complaint"): 0.2,
    ("technical_support", "general_query"): 0.2,
    ("general_query", "technical_support"): 0.2,
    ("complaint", "refund_request"): 0.3,
    ("refund_request", "complaint"): 0.3,
    ("account_issue", "technical_support"): 0.3,
    ("technical_support", "account_issue"): 0.3,
    ("shipping", "complaint"): 0.2,
    ("complaint", "shipping"): 0.2,
    ("billing", "account_issue"): 0.2,
    ("account_issue", "billing"): 0.2,
}


def grade_intent(predicted: str, ground_truth: str) -> tuple[float, str]:
    """
    Grade intent classification.
    Returns (score, feedback) where score is strictly 0.01–0.99.
    """
    predicted = _normalize(predicted)
    ground_truth_norm = _normalize(ground_truth)

    if predicted not in VALID_INTENTS:
        return 0.01, f"Invalid intent '{predicted}'. Valid intents: {sorted(VALID_INTENTS)}"

    if predicted == ground_truth_norm:
        return 0.99, f"Correct! Intent '{predicted}' matches exactly."

    # Check for partial credit
    pair = (predicted, ground_truth_norm)
    if pair in INTENT_SIMILARITY:
        score = INTENT_SIMILARITY[pair]
        return score, (
            f"Partial credit ({score:.1f}): '{predicted}' is related to the correct "
            f"intent '{ground_truth}', but not exact."
        )

    return 0.01, f"Incorrect. Predicted '{predicted}', expected '{ground_truth}'."


# ─────────────────────────────────────────────────────────────────────────────
# Task 2: Information Extraction Grader
# ─────────────────────────────────────────────────────────────────────────────

EXTRACTION_FIELDS = [
    ("order_id", 0.20),
    ("customer_name", 0.15),
    ("issue_description", 0.25),
    ("product_name", 0.10),
    ("requested_resolution", 0.15),
    ("urgency_level", 0.10),
    ("email_address", 0.05),
]


def grade_extraction(predicted: dict, ground_truth: dict) -> tuple[float, str]:
    """
    Grade information extraction across all fields.
    Returns (score, feedback) where score is strictly 0.01–0.99.
    """
    total_score = 0.0
    feedback_parts = []

    for field, weight in EXTRACTION_FIELDS:
        pred_val = str(predicted.get(field, "")).strip()
        gt_val = str(ground_truth.get(field, "")).strip()

        if not gt_val:
            # Ground truth is empty
            if not pred_val:
                field_score = 1.0
            else:
                field_score = 0.8
            total_score += field_score * weight
            feedback_parts.append(f"  {field}: {field_score:.2f} (gt empty)")
            continue

        if not pred_val:
            field_score = 0.0
            total_score += 0.0
            feedback_parts.append(f"  {field}: 0.00 (missing)")
            continue

        # For urgency_level, exact match only
        if field == "urgency_level":
            if _normalize(pred_val) == _normalize(gt_val):
                field_score = 1.0
            else:
                field_score = 0.0
            total_score += field_score * weight
            feedback_parts.append(
                f"  {field}: {field_score:.2f} (pred='{pred_val}', gt='{gt_val}')"
            )
            continue

        # For order_id / email, exact-ish match
        if field in ("order_id", "email_address"):
            if _normalize(pred_val) == _normalize(gt_val):
                field_score = 1.0
            elif _normalize(gt_val) in _normalize(pred_val):
                field_score = 0.8
            else:
                field_score = 0.0
            total_score += field_score * weight
            feedback_parts.append(
                f"  {field}: {field_score:.2f} (pred='{pred_val}', gt='{gt_val}')"
            )
            continue

        # For text fields, use similarity
        sim = _similarity(pred_val, gt_val)
        gt_words = set(_normalize(gt_val).split())
        pred_words = set(_normalize(pred_val).split())
        keyword_overlap = len(gt_words & pred_words) / max(len(gt_words), 1)

        field_score = 0.6 * sim + 0.4 * keyword_overlap
        field_score = min(field_score, 1.0)
        total_score += field_score * weight
        feedback_parts.append(
            f"  {field}: {field_score:.2f} (similarity={sim:.2f}, keyword_overlap={keyword_overlap:.2f})"
        )

    # Restrict total_score strictly to (0, 1) bounds
    total_score = max(0.01, min(total_score, 0.99))
    total_score = round(total_score, 4)
    feedback = "Extraction scores by field:\n" + "\n".join(feedback_parts)
    feedback += f"\n  TOTAL: {total_score:.4f}"
    return total_score, feedback


# ─────────────────────────────────────────────────────────────────────────────
# Task 3: Response Generation Grader
# ─────────────────────────────────────────────────────────────────────────────

UNSAFE_PATTERNS = [
    r"social\s*security\s*(number|#|no\.?)",
    r"credit\s*card\s*(number|#|no\.?|full)",
    r"password\s*is\s*\w+",
    r"(kill|die|harm)\s+(yourself|themselves|himself|herself)",
    r"(stupid|idiot|moron|dumb)\s+(customer|user|you)",
]


def grade_response(response: str, ground_truth: dict, email: dict) -> tuple[float, str]:
    """
    Grade a generated email response.
    Returns (score, feedback) where score is strictly 0.01–0.99.
    """
    if not response or not response.strip():
        return 0.01, "Empty response."

    response_lower = _normalize(response)
    feedback_parts = []

    # ── Safety Check (0.15) ──────────────────────────────────────────────
    safety_score = 1.0
    safety_issues = []
    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, response_lower):
            safety_score = 0.0
            safety_issues.append(f"Unsafe pattern detected: {pattern}")

    # Check must_not_include
    must_not = ground_truth.get("response_must_not_include", [])
    for phrase in must_not:
        if _normalize(phrase) in response_lower:
            safety_score = max(safety_score - 0.5, 0.0)
            safety_issues.append(f"Contains prohibited phrase: '{phrase}'")

    if safety_issues:
        feedback_parts.append(f"  Safety: {safety_score:.2f} — " + "; ".join(safety_issues))
    else:
        feedback_parts.append(f"  Safety: {safety_score:.2f} — No issues detected")

    # ── Relevance (0.25) ─────────────────────────────────────────────────
    relevance_score = 0.0
    keywords = ground_truth.get("response_keywords", [])
    if keywords:
        matches = sum(1 for kw in keywords if _normalize(kw) in response_lower)
        relevance_score = matches / len(keywords)
    feedback_parts.append(
        f"  Relevance: {relevance_score:.2f} — {int(relevance_score * len(keywords))}/{len(keywords)} keywords found"
    )

    # ── Completeness (0.25) ──────────────────────────────────────────────
    completeness_score = 0.0
    must_include = ground_truth.get("response_must_include", [])
    if must_include:
        mi_matches = sum(1 for phrase in must_include if _normalize(phrase) in response_lower)
        completeness_score = mi_matches / len(must_include)
    feedback_parts.append(
        f"  Completeness: {completeness_score:.2f} — {int(completeness_score * len(must_include))}/{len(must_include)} required elements found"
    )

    # ── Professionalism (0.20) ───────────────────────────────────────────
    prof_score = 0.0
    prof_checks = {
        "has_greeting": bool(re.search(r"(dear|hello|hi |good\s+(morning|afternoon|evening))", response_lower)),
        "has_closing": bool(re.search(r"(regards|sincerely|best|thank|cheers|warm)", response_lower)),
        "adequate_length": 50 <= len(response.split()) <= 500,
        "has_paragraphs": response.count("\n") >= 2,
        "no_all_caps": sum(1 for c in response if c.isupper()) / max(len(response), 1) < 0.4,
    }
    prof_score = sum(prof_checks.values()) / len(prof_checks)
    prof_details = ", ".join(f"{k}={'Y' if v else 'N'}" for k, v in prof_checks.items())
    feedback_parts.append(f"  Professionalism: {prof_score:.2f} — {prof_details}")

    # ── Accuracy (0.15) ──────────────────────────────────────────────────
    accuracy_score = 0.0
    # Check if order ID is referenced correctly
    gt_order = ground_truth.get("order_id", "") or email.get("ground_truth", {}).get("order_id", "")
    if gt_order:
        if _normalize(gt_order) in response_lower:
            accuracy_score += 0.5
    else:
        accuracy_score += 0.5  # No order to check

    # Check if customer name is used
    gt_name = ground_truth.get("customer_name", "") or email.get("ground_truth", {}).get("customer_name", "")
    if gt_name:
        name_parts = gt_name.lower().split()
        if any(part in response_lower for part in name_parts):
            accuracy_score += 0.5
    else:
        accuracy_score += 0.5

    feedback_parts.append(f"  Accuracy: {accuracy_score:.2f}")

    # ── Final Score ──────────────────────────────────────────────────────
    final_score = (
        0.25 * relevance_score
        + 0.25 * completeness_score
        + 0.20 * prof_score
        + 0.15 * safety_score
        + 0.15 * accuracy_score
    )
    
    # Restrict final_score strictly to (0, 1) bounds
    final_score = max(0.01, min(final_score, 0.99))
    final_score = round(final_score, 4)

    feedback = "Response grading breakdown:\n" + "\n".join(feedback_parts)
    feedback += f"\n  FINAL SCORE: {final_score:.4f}"
    return final_score, feedback
