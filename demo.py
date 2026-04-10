from emailops_env.server.email_environment import EmailEnvironment
from emailops_env.models import EmailAction
import json

def run_demo():
    print("="*60)
    print("🚀 EMAILOPS-ENV DEMONSTRATION")
    print("="*60)
    
    # Initialize environment
    env = EmailEnvironment(seed=42)
    
    # Reset to start a new episode
    print("\n[1] RESETTING ENVIRONMENT...")
    obs = env.reset("email_001")
    
    print(f"📧 Email ID: {obs.email_id}")
    print(f"📧 Subject:  {obs.email_subject}")
    print(f"📧 From:     {obs.email_from}")
    print(f"📝 Task {obs.task_id}:   {obs.task_name}")
    print(f"👉 Instruction: {obs.task_instruction}")
    
    # Task 1: Intent Classification
    print("\n" + "-"*60)
    print("[2] PERFORMING TASK 1: INTENT CLASSIFICATION")
    
    # Agent decides intent is "billing"
    action1 = EmailAction(intent="billing")
    print(f"🤖 Agent Action: {json.dumps({'intent': action1.intent})}")
    
    # Step environment
    res1 = env.step(action1)
    
    print(f"⭐️ Reward: {res1['reward']}")
    print(f"💬 Feedback: {res1['observation'].feedback.splitlines()[0]}")
    
    # Task 2: Information Extraction
    print("\n" + "-"*60)
    print(f"[3] PERFORMING TASK 2: {res1['observation'].task_name}")
    
    # Agent extracts fields
    extracted_data = {
        "order_id": "INV-2026-4471",
        "customer_name": "Sarah Johnson",
        "issue_description": "Billing discrepancy - charged $349.99 for Enterprise Plan instead of $199.99 for Professional Plan after downgrade on February 28, 2026",
        "product_name": "Professional Plan",
        "requested_resolution": "Issue a credit for the $150.00 overcharge",
        "urgency_level": "medium",
        "email_address": "sarah.johnson@techcorp.com"
    }
    action2 = EmailAction(**extracted_data)
    print(f"🤖 Agent Action: Extracted {len(extracted_data)} fields (e.g., order_id={action2.order_id})")
    
    res2 = env.step(action2)
    print(f"⭐️ Reward: {res2['reward']}")
    print("💬 Feedback snippet:")
    for line in res2['observation'].feedback.splitlines()[:5]:
        print(f"    {line}")
    
    # Task 3: Response Generation
    print("\n" + "-"*60)
    print(f"[4] PERFORMING TASK 3: {res2['observation'].task_name}")
    
    # Agent generates response
    response = (
        "Dear Sarah Johnson,\n\n"
        "Thank you for reaching out regarding the billing discrepancy on your recent "
        "invoice (INV-2026-4471). We sincerely apologize for this error.\n\n"
        "We have reviewed your account and can confirm you successfully downgraded "
        "to the Professional Plan on February 28. We are processing a credit of "
        "$150.00 to your account to resolve the overcharge immediately.\n\n"
        "Please let us know if you have any questions.\n\n"
        "Best regards,\n"
        "TechCorp Support Team"
    )
    action3 = EmailAction(response_text=response)
    print(f"🤖 Agent Action: Generated response ({len(response.split())} words)")
    
    res3 = env.step(action3)
    print(f"⭐️ Reward: {res3['reward']}")
    print(f"✅ Episode Done: {res3['done']}")
    
    print("\n" + "="*60)
    print("📊 EPISODE SUMMARY")
    print("="*60)
    
    state = env.state()
    print(f"Final Average Score: {state.total_score:.4f}")
    for task, score in state.task_scores.items():
        print(f" - {task.replace('_', ' ').title()}: {score:.4f}")

if __name__ == "__main__":
    run_demo()
