"""
EmailOps-Env: Realistic email dataset with ground-truth annotations.
Contains 20 diverse customer/internal emails spanning multiple intent categories,
each with full ground-truth for classification, extraction, and response grading.
"""

EMAILS = [
    {
        "id": "email_001",
        "from": "sarah.johnson@techcorp.com",
        "date": "2026-03-15 09:23:00",
        "subject": "Billing discrepancy on Invoice #INV-2026-4471",
        "body": (
            "Dear Support Team,\n\n"
            "I'm writing to report a billing discrepancy on my latest invoice. "
            "My Invoice #INV-2026-4471 dated March 10, 2026 shows a charge of $349.99 "
            "for the Enterprise Plan, but I downgraded to the Professional Plan ($199.99/month) "
            "on February 28, 2026. My account ID is ACC-88921.\n\n"
            "Could you please review this and issue a credit for the $150.00 overcharge? "
            "I have attached a screenshot of my plan change confirmation.\n\n"
            "Thank you for your prompt attention to this matter.\n\n"
            "Best regards,\n"
            "Sarah Johnson\n"
            "Finance Manager, TechCorp Inc.\n"
            "sarah.johnson@techcorp.com"
        ),
        "ground_truth": {
            "intent": "billing",
            "order_id": "INV-2026-4471",
            "customer_name": "Sarah Johnson",
            "issue_description": "Billing discrepancy - charged $349.99 for Enterprise Plan instead of $199.99 for Professional Plan after downgrade on February 28, 2026",
            "product_name": "Professional Plan",
            "requested_resolution": "Issue a credit for the $150.00 overcharge",
            "urgency_level": "medium",
            "email_address": "sarah.johnson@techcorp.com",
            "response_keywords": ["invoice", "credit", "overcharge", "reviewed", "apolog"],
            "response_tone": "professional",
            "response_must_include": ["INV-2026-4471", "credit", "$150"],
            "response_must_not_include": ["unfortunately we cannot", "denied"],
        },
    },
    {
        "id": "email_002",
        "from": "mike.chen@startup.io",
        "date": "2026-03-14 14:05:00",
        "subject": "URGENT: Production API returning 500 errors",
        "body": (
            "Hi Support,\n\n"
            "Our production environment has been experiencing intermittent 500 Internal Server "
            "Errors from your API since approximately 2:00 PM EST today. This is critically "
            "impacting our live customers.\n\n"
            "Details:\n"
            "- API Endpoint: /v2/payments/process\n"
            "- Error Rate: ~30% of requests failing\n"
            "- Account ID: API-KEY-7823\n"
            "- Region: us-east-1\n\n"
            "We need this resolved ASAP as we're losing transactions. Please escalate immediately.\n\n"
            "Thanks,\n"
            "Mike Chen\n"
            "CTO, Startup.io\n"
            "mike.chen@startup.io"
        ),
        "ground_truth": {
            "intent": "technical_support",
            "order_id": "API-KEY-7823",
            "customer_name": "Mike Chen",
            "issue_description": "Production API returning intermittent 500 Internal Server Errors on /v2/payments/process endpoint, ~30% failure rate since 2:00 PM EST, affecting live customers",
            "product_name": "Payments API v2",
            "requested_resolution": "Immediate resolution and escalation of the 500 errors on the payments API",
            "urgency_level": "critical",
            "email_address": "mike.chen@startup.io",
            "response_keywords": ["escalat", "engineer", "investigating", "priority", "status"],
            "response_tone": "professional",
            "response_must_include": ["escalat", "investigating"],
            "response_must_not_include": ["low priority", "queue"],
        },
    },
    {
        "id": "email_003",
        "from": "jessica.williams@gmail.com",
        "date": "2026-03-13 11:30:00",
        "subject": "Extremely disappointed with customer service",
        "body": (
            "To Whom It May Concern,\n\n"
            "I am writing to express my extreme disappointment with the level of service "
            "I have received over the past two weeks regarding my order #ORD-55123.\n\n"
            "I ordered a Premium Wireless Headset on February 27, and it arrived damaged on "
            "March 5. I called your support line three times (March 6, 8, and 11) and was "
            "promised a replacement each time, but nothing has been shipped.\n\n"
            "Each call required me to wait over 45 minutes, and the last representative "
            "was rude and dismissive. I'm a loyal customer who has spent over $2,000 with "
            "your company in the past year.\n\n"
            "If this is not resolved within 48 hours, I will be filing a complaint with the "
            "BBB and sharing my experience on social media.\n\n"
            "Disappointed,\n"
            "Jessica Williams\n"
            "jessica.williams@gmail.com"
        ),
        "ground_truth": {
            "intent": "complaint",
            "order_id": "ORD-55123",
            "customer_name": "Jessica Williams",
            "issue_description": "Received damaged Premium Wireless Headset, called support three times over two weeks with no replacement shipped, experienced long wait times and rude representative",
            "product_name": "Premium Wireless Headset",
            "requested_resolution": "Ship replacement within 48 hours",
            "urgency_level": "high",
            "email_address": "jessica.williams@gmail.com",
            "response_keywords": ["apolog", "replacement", "ship", "escalat", "experience"],
            "response_tone": "empathetic",
            "response_must_include": ["apolog", "replacement", "ORD-55123"],
            "response_must_not_include": ["policy does not allow", "your fault"],
        },
    },
    {
        "id": "email_004",
        "from": "david.park@enterprise.com",
        "date": "2026-03-12 16:45:00",
        "subject": "Question about enterprise pricing and features",
        "body": (
            "Hello,\n\n"
            "I'm evaluating your platform for our organization (500+ employees) and have "
            "a few questions:\n\n"
            "1. Do you offer volume discounts for teams over 500 users?\n"
            "2. Is SSO (SAML 2.0) included in the Enterprise plan?\n"
            "3. What is your data residency policy for EU customers?\n"
            "4. Can we get a dedicated account manager?\n\n"
            "We're currently using CompetitorX but our contract ends in June 2026. "
            "We'd like to schedule a demo if possible.\n\n"
            "Best,\n"
            "David Park\n"
            "VP of Engineering\n"
            "Enterprise Solutions Corp.\n"
            "david.park@enterprise.com"
        ),
        "ground_truth": {
            "intent": "general_query",
            "order_id": "",
            "customer_name": "David Park",
            "issue_description": "Inquiry about enterprise pricing, volume discounts for 500+ users, SSO support, EU data residency, and dedicated account manager availability",
            "product_name": "Enterprise Plan",
            "requested_resolution": "Provide pricing information and schedule a demo",
            "urgency_level": "low",
            "email_address": "david.park@enterprise.com",
            "response_keywords": ["demo", "enterprise", "pricing", "SSO", "account manager"],
            "response_tone": "professional",
            "response_must_include": ["demo", "enterprise"],
            "response_must_not_include": ["cannot help", "not available"],
        },
    },
    {
        "id": "email_005",
        "from": "anna.kowalski@retailco.com",
        "date": "2026-03-11 08:15:00",
        "subject": "Cannot access my account - password reset not working",
        "body": (
            "Hi,\n\n"
            "I've been locked out of my account (username: anna.k_retail) for the past "
            "3 days. I've tried the password reset link multiple times but the emails "
            "never arrive. I've checked my spam folder.\n\n"
            "My account email is anna.kowalski@retailco.com and my account number is "
            "ACCT-34521. I need access urgently as I have pending orders to manage.\n\n"
            "Can you please reset my password manually or provide an alternative way "
            "to regain access?\n\n"
            "Thank you,\n"
            "Anna Kowalski\n"
            "anna.kowalski@retailco.com"
        ),
        "ground_truth": {
            "intent": "account_issue",
            "order_id": "ACCT-34521",
            "customer_name": "Anna Kowalski",
            "issue_description": "Locked out of account for 3 days, password reset emails not arriving, username anna.k_retail",
            "product_name": "",
            "requested_resolution": "Manual password reset or alternative access method",
            "urgency_level": "high",
            "email_address": "anna.kowalski@retailco.com",
            "response_keywords": ["password", "reset", "access", "account", "security"],
            "response_tone": "professional",
            "response_must_include": ["password", "reset", "ACCT-34521"],
            "response_must_not_include": ["create a new account", "nothing we can do"],
        },
    },
    {
        "id": "email_006",
        "from": "robert.martinez@logistics.net",
        "date": "2026-03-10 13:20:00",
        "subject": "Where is my shipment? Order #SHP-99281",
        "body": (
            "Hello,\n\n"
            "I placed an order (#SHP-99281) on March 1st with express shipping (2-day delivery). "
            "It's now March 10th and I still haven't received my package.\n\n"
            "The tracking number TRK-482716 shows the package has been 'In Transit' since "
            "March 3rd with no updates. I paid an extra $25 for express shipping.\n\n"
            "I need the items (Industrial Grade Sensor Kit) for a project deadline on March 15th. "
            "Please either locate my package or send a replacement with overnight shipping.\n\n"
            "Robert Martinez\n"
            "robert.martinez@logistics.net"
        ),
        "ground_truth": {
            "intent": "shipping",
            "order_id": "SHP-99281",
            "customer_name": "Robert Martinez",
            "issue_description": "Express shipping order placed March 1st not received by March 10th, tracking TRK-482716 stuck at 'In Transit' since March 3rd, paid extra $25 for 2-day delivery",
            "product_name": "Industrial Grade Sensor Kit",
            "requested_resolution": "Locate package or send replacement with overnight shipping",
            "urgency_level": "high",
            "email_address": "robert.martinez@logistics.net",
            "response_keywords": ["tracking", "shipment", "shipping", "investigat", "delivery"],
            "response_tone": "professional",
            "response_must_include": ["SHP-99281", "tracking"],
            "response_must_not_include": ["your problem", "no refund"],
        },
    },
    {
        "id": "email_007",
        "from": "emily.nguyen@design.co",
        "date": "2026-03-09 10:00:00",
        "subject": "Request full refund for subscription - REF-20261",
        "body": (
            "Dear Billing Department,\n\n"
            "I am requesting a full refund for my annual subscription (Reference: REF-20261). "
            "I purchased the Creative Suite Pro annual plan on February 1, 2026 for $599.88.\n\n"
            "The software has been unusable due to constant crashes on macOS Ventura (14.3), "
            "and your tech support has been unable to resolve the issue after 4 support tickets "
            "(#TS-1102, #TS-1145, #TS-1189, #TS-1201).\n\n"
            "Per your 30-day satisfaction guarantee, I am within the refund window and expect "
            "a full refund to my original payment method (Visa ending 4421).\n\n"
            "Please confirm the refund processing timeline.\n\n"
            "Emily Nguyen\n"
            "emily.nguyen@design.co"
        ),
        "ground_truth": {
            "intent": "refund_request",
            "order_id": "REF-20261",
            "customer_name": "Emily Nguyen",
            "issue_description": "Requesting full refund of $599.88 for Creative Suite Pro annual plan due to constant crashes on macOS Ventura 14.3, 4 unresolved support tickets",
            "product_name": "Creative Suite Pro",
            "requested_resolution": "Full refund of $599.88 to Visa ending 4421",
            "urgency_level": "medium",
            "email_address": "emily.nguyen@design.co",
            "response_keywords": ["refund", "process", "confirm", "apolog", "payment"],
            "response_tone": "professional",
            "response_must_include": ["refund", "REF-20261"],
            "response_must_not_include": ["non-refundable", "denied"],
        },
    },
    {
        "id": "email_008",
        "from": "tom.bradley@consulting.com",
        "date": "2026-03-08 15:30:00",
        "subject": "Great experience with your new dashboard!",
        "body": (
            "Hi Team,\n\n"
            "Just wanted to drop a note to say that the new analytics dashboard you "
            "released last week is fantastic! The real-time data visualization and the "
            "custom report builder have saved our team hours of work.\n\n"
            "A few suggestions for future updates:\n"
            "1. It would be great to have an export to PDF option\n"
            "2. Dark mode support would be appreciated\n"
            "3. The date range picker could use a 'Last 90 days' preset\n\n"
            "Keep up the great work! My account is PRO-44521.\n\n"
            "Cheers,\n"
            "Tom Bradley\n"
            "tom.bradley@consulting.com"
        ),
        "ground_truth": {
            "intent": "feedback",
            "order_id": "PRO-44521",
            "customer_name": "Tom Bradley",
            "issue_description": "Positive feedback on new analytics dashboard with three feature suggestions: PDF export, dark mode, and 90-day date range preset",
            "product_name": "Analytics Dashboard",
            "requested_resolution": "Consider implementing suggested features",
            "urgency_level": "low",
            "email_address": "tom.bradley@consulting.com",
            "response_keywords": ["thank", "feedback", "suggestion", "team", "feature"],
            "response_tone": "appreciative",
            "response_must_include": ["thank", "feedback"],
            "response_must_not_include": ["complaint", "sorry for the inconvenience"],
        },
    },
    {
        "id": "email_009",
        "from": "lisa.zhang@healthcare.org",
        "date": "2026-03-07 09:45:00",
        "subject": "HIPAA compliance documentation request",
        "body": (
            "Dear Compliance Team,\n\n"
            "Our organization is conducting a vendor security assessment and we need the "
            "following documentation for your platform:\n\n"
            "1. SOC 2 Type II audit report (most recent)\n"
            "2. HIPAA Business Associate Agreement (BAA) template\n"
            "3. Data encryption standards documentation\n"
            "4. Incident response plan summary\n"
            "5. Data retention and deletion policies\n\n"
            "Our vendor assessment deadline is March 25, 2026. Please send these to "
            "compliance@healthcare.org.\n\n"
            "Account reference: HLTH-8890\n\n"
            "Thank you,\n"
            "Lisa Zhang, CISO\n"
            "Healthcare Solutions Org.\n"
            "lisa.zhang@healthcare.org"
        ),
        "ground_truth": {
            "intent": "general_query",
            "order_id": "HLTH-8890",
            "customer_name": "Lisa Zhang",
            "issue_description": "Requesting HIPAA compliance documentation including SOC 2 Type II report, BAA template, encryption standards, incident response plan, and data retention policies for vendor assessment",
            "product_name": "",
            "requested_resolution": "Provide all 5 compliance documents by March 25, 2026",
            "urgency_level": "medium",
            "email_address": "lisa.zhang@healthcare.org",
            "response_keywords": ["compliance", "document", "HIPAA", "provide", "team"],
            "response_tone": "professional",
            "response_must_include": ["compliance", "document"],
            "response_must_not_include": ["we don't support", "unavailable"],
        },
    },
    {
        "id": "email_010",
        "from": "carlos.rivera@ecommerce.com",
        "date": "2026-03-06 17:00:00",
        "subject": "Double charged for order #EC-77341",
        "body": (
            "Support,\n\n"
            "I was charged twice for order #EC-77341. My credit card (Mastercard ending 3356) "
            "shows two identical charges of $89.95 on March 4, 2026.\n\n"
            "I only placed one order for the Ergonomic Keyboard Pro. Please refund the "
            "duplicate charge immediately.\n\n"
            "This is the second time this has happened to me. Last time was with order "
            "#EC-65102 in January.\n\n"
            "Carlos Rivera\n"
            "carlos.rivera@ecommerce.com"
        ),
        "ground_truth": {
            "intent": "billing",
            "order_id": "EC-77341",
            "customer_name": "Carlos Rivera",
            "issue_description": "Double charged $89.95 for single order, two identical charges on Mastercard ending 3356 on March 4, 2026, recurring issue (previous order EC-65102)",
            "product_name": "Ergonomic Keyboard Pro",
            "requested_resolution": "Refund the duplicate charge of $89.95 immediately",
            "urgency_level": "high",
            "email_address": "carlos.rivera@ecommerce.com",
            "response_keywords": ["refund", "duplicate", "charge", "apolog", "process"],
            "response_tone": "professional",
            "response_must_include": ["refund", "EC-77341", "duplicate"],
            "response_must_not_include": ["correct charge", "no error found"],
        },
    },
    {
        "id": "email_011",
        "from": "priya.sharma@fintech.co",
        "date": "2026-03-05 12:10:00",
        "subject": "Integration webhook failures - need technical help",
        "body": (
            "Hi Technical Support,\n\n"
            "We're experiencing issues with our webhook integration. Our endpoint "
            "(https://api.fintech.co/webhooks/payments) is not receiving event "
            "notifications for payment_success and payment_failed events.\n\n"
            "Configuration details:\n"
            "- Webhook ID: WH-5543\n"
            "- Events subscribed: payment_success, payment_failed, refund_completed\n"
            "- Our endpoint returns 200 OK (verified independently)\n"
            "- Started failing approximately 48 hours ago\n\n"
            "We've verified our SSL certificate is valid and our firewall rules allow "
            "traffic from your IP ranges. Could this be related to the API update "
            "mentioned in your changelog v3.2.1?\n\n"
            "Priya Sharma\n"
            "Lead Developer, FinTech Co.\n"
            "priya.sharma@fintech.co"
        ),
        "ground_truth": {
            "intent": "technical_support",
            "order_id": "WH-5543",
            "customer_name": "Priya Sharma",
            "issue_description": "Webhook integration not receiving payment_success and payment_failed event notifications for 48 hours, endpoint verified working, possible relation to API update v3.2.1",
            "product_name": "Webhook Integration / Payments API",
            "requested_resolution": "Diagnose and fix webhook delivery failures",
            "urgency_level": "high",
            "email_address": "priya.sharma@fintech.co",
            "response_keywords": ["webhook", "investigat", "engineer", "event", "delivery"],
            "response_tone": "professional",
            "response_must_include": ["webhook", "WH-5543"],
            "response_must_not_include": ["not our issue", "works on our end"],
        },
    },
    {
        "id": "email_012",
        "from": "james.wilson@school.edu",
        "date": "2026-03-04 08:30:00",
        "subject": "Requesting educational discount for 200 student licenses",
        "body": (
            "Hello Sales Team,\n\n"
            "I'm the IT Director at Westfield Academy and I'm interested in purchasing "
            "200 student licenses for your Learning Platform Pro.\n\n"
            "Questions:\n"
            "1. Do you offer educational institution pricing?\n"
            "2. Is there a minimum commitment period?\n"
            "3. Can we get a trial for 30 students first?\n"
            "4. Do you support LTI integration with our LMS (Canvas)?\n\n"
            "Our budget approval process requires a formal quote by March 20, 2026. "
            "School account reference: EDU-12045.\n\n"
            "Best regards,\n"
            "James Wilson\n"
            "IT Director, Westfield Academy\n"
            "james.wilson@school.edu"
        ),
        "ground_truth": {
            "intent": "general_query",
            "order_id": "EDU-12045",
            "customer_name": "James Wilson",
            "issue_description": "Inquiry about educational pricing for 200 student licenses, trial availability, LTI/Canvas integration, and formal quote needed by March 20",
            "product_name": "Learning Platform Pro",
            "requested_resolution": "Provide educational pricing quote and trial information",
            "urgency_level": "medium",
            "email_address": "james.wilson@school.edu",
            "response_keywords": ["educational", "pricing", "trial", "quote", "license"],
            "response_tone": "professional",
            "response_must_include": ["educational", "quote"],
            "response_must_not_include": ["no discounts", "not eligible"],
        },
    },
    {
        "id": "email_013",
        "from": "natalie.brown@media.com",
        "date": "2026-03-03 14:55:00",
        "subject": "RE: Still waiting for my refund - 3 weeks now",
        "body": (
            "This is my FOURTH email about this refund.\n\n"
            "Order #MED-33109 was returned on February 10, 2026, and I received a "
            "return confirmation (RET-33109-A) the same day. Your policy states refunds "
            "are processed within 5-7 business days.\n\n"
            "It has now been over 3 weeks and I have not received my $245.00 refund. "
            "Every time I contact support, I get a different answer:\n"
            "- Feb 18: 'Processing' \n"
            "- Feb 24: 'Escalated'\n"
            "- Mar 1: 'Under review'\n\n"
            "This is completely unacceptable. I want my refund processed TODAY or I will "
            "initiate a chargeback through my bank.\n\n"
            "Natalie Brown\n"
            "natalie.brown@media.com"
        ),
        "ground_truth": {
            "intent": "refund_request",
            "order_id": "MED-33109",
            "customer_name": "Natalie Brown",
            "issue_description": "Refund of $245.00 for returned order not processed after 3 weeks despite return confirmation RET-33109-A, multiple contacts with inconsistent responses, threatening chargeback",
            "product_name": "",
            "requested_resolution": "Process the $245.00 refund immediately",
            "urgency_level": "critical",
            "email_address": "natalie.brown@media.com",
            "response_keywords": ["refund", "apolog", "process", "immediately", "confirm"],
            "response_tone": "empathetic",
            "response_must_include": ["refund", "apolog", "MED-33109"],
            "response_must_not_include": ["patience", "normal processing time"],
        },
    },
    {
        "id": "email_014",
        "from": "kevin.ogrady@manufacturing.com",
        "date": "2026-03-02 11:20:00",
        "subject": "Shipping address change for order #MFG-44782",
        "body": (
            "Hi,\n\n"
            "I need to change the shipping address for my recent order #MFG-44782 "
            "(placed yesterday, March 1).\n\n"
            "Current address: 123 Oak Street, Suite 200, Portland, OR 97201\n"
            "New address: 456 Pine Avenue, Building C, Seattle, WA 98101\n\n"
            "The order contains 5 units of Industrial Control Panel (ICP-200) totaling $4,750.\n"
            "Please confirm if this change can be made before the order ships.\n\n"
            "Kevin O'Grady\n"
            "Procurement Manager\n"
            "kevin.ogrady@manufacturing.com"
        ),
        "ground_truth": {
            "intent": "shipping",
            "order_id": "MFG-44782",
            "customer_name": "Kevin O'Grady",
            "issue_description": "Request to change shipping address from Portland OR to Seattle WA for order placed March 1, 5 units of Industrial Control Panel totaling $4,750",
            "product_name": "Industrial Control Panel (ICP-200)",
            "requested_resolution": "Update shipping address before order ships",
            "urgency_level": "medium",
            "email_address": "kevin.ogrady@manufacturing.com",
            "response_keywords": ["address", "updated", "shipping", "confirm", "order"],
            "response_tone": "professional",
            "response_must_include": ["MFG-44782", "address"],
            "response_must_not_include": ["cannot change", "too late"],
        },
    },
    {
        "id": "email_015",
        "from": "rachel.kim@agency.com",
        "date": "2026-03-01 09:00:00",
        "subject": "Account compromised - unauthorized access detected",
        "body": (
            "URGENT SECURITY ISSUE\n\n"
            "I believe my account has been compromised. This morning I noticed:\n"
            "- Unknown login from IP 185.220.101.34 (Russia) at 3:47 AM EST\n"
            "- My account email was changed to an unknown address\n"
            "- Two unauthorized API keys were generated\n"
            "- $340 in unauthorized charges on my billing\n\n"
            "My account: AGN-22109\n"
            "Original email: rachel.kim@agency.com\n\n"
            "Please immediately:\n"
            "1. Lock my account\n"
            "2. Revoke all API keys\n"
            "3. Restore my original email\n"
            "4. Reverse the unauthorized charges\n\n"
            "Rachel Kim\n"
            "rachel.kim@agency.com\n"
            "Phone: (555) 891-2345"
        ),
        "ground_truth": {
            "intent": "account_issue",
            "order_id": "AGN-22109",
            "customer_name": "Rachel Kim",
            "issue_description": "Account compromised with unauthorized login from Russia, email changed, two unauthorized API keys generated, $340 in unauthorized charges",
            "product_name": "",
            "requested_resolution": "Lock account, revoke API keys, restore original email, reverse unauthorized charges",
            "urgency_level": "critical",
            "email_address": "rachel.kim@agency.com",
            "response_keywords": ["security", "lock", "account", "investigat", "immediately"],
            "response_tone": "professional",
            "response_must_include": ["security", "account", "AGN-22109"],
            "response_must_not_include": ["wait", "next business day"],
        },
    },
    {
        "id": "email_016",
        "from": "alex.thompson@devops.io",
        "date": "2026-02-28 16:40:00",
        "subject": "Feature request: Terraform provider for your infrastructure API",
        "body": (
            "Hey team,\n\n"
            "Love your infrastructure API! We manage 200+ cloud resources through it.\n\n"
            "Feature request: Would you consider building an official Terraform provider? "
            "Right now we're using custom REST API calls in our Terraform configs, which "
            "is fragile and hard to maintain.\n\n"
            "An official provider would let us:\n"
            "- Manage resources declaratively\n"
            "- Track state properly\n"
            "- Integrate with our CI/CD pipeline\n"
            "- Reduce custom scripting by ~60%\n\n"
            "Happy to contribute or beta test if you go this route. "
            "Account: DEVOPS-9921.\n\n"
            "Alex Thompson\n"
            "alex.thompson@devops.io"
        ),
        "ground_truth": {
            "intent": "feedback",
            "order_id": "DEVOPS-9921",
            "customer_name": "Alex Thompson",
            "issue_description": "Feature request for official Terraform provider for infrastructure API, currently using fragile custom REST API calls, willing to contribute or beta test",
            "product_name": "Infrastructure API",
            "requested_resolution": "Consider building official Terraform provider",
            "urgency_level": "low",
            "email_address": "alex.thompson@devops.io",
            "response_keywords": ["feature", "request", "terraform", "roadmap", "team"],
            "response_tone": "appreciative",
            "response_must_include": ["feature", "request", "team"],
            "response_must_not_include": ["not planned", "won't implement"],
        },
    },
    {
        "id": "email_017",
        "from": "maria.gonzalez@travel.com",
        "date": "2026-02-27 12:00:00",
        "subject": "Billing error - charged for cancelled booking #BK-91102",
        "body": (
            "Dear Support,\n\n"
            "I cancelled my hotel booking #BK-91102 on February 20, well within the "
            "free cancellation window (48 hours before check-in on February 25).\n\n"
            "Despite the cancellation confirmation email I received (CANC-91102), my "
            "AmEx card ending 7789 was charged $892.50 on February 25.\n\n"
            "Please process a full refund. I can forward the cancellation confirmation "
            "email if needed.\n\n"
            "Maria Gonzalez\n"
            "maria.gonzalez@travel.com"
        ),
        "ground_truth": {
            "intent": "billing",
            "order_id": "BK-91102",
            "customer_name": "Maria Gonzalez",
            "issue_description": "Charged $892.50 for hotel booking that was cancelled within free cancellation window on February 20, has cancellation confirmation CANC-91102",
            "product_name": "Hotel Booking",
            "requested_resolution": "Full refund of $892.50",
            "urgency_level": "high",
            "email_address": "maria.gonzalez@travel.com",
            "response_keywords": ["refund", "cancellation", "charge", "apolog", "process"],
            "response_tone": "professional",
            "response_must_include": ["refund", "BK-91102"],
            "response_must_not_include": ["non-refundable", "penalty"],
        },
    },
    {
        "id": "email_018",
        "from": "daniel.oconnor@law.com",
        "date": "2026-02-26 10:30:00",
        "subject": "Data export request under GDPR - Account LAW-56221",
        "body": (
            "Dear Data Protection Officer,\n\n"
            "Pursuant to Article 15 of the General Data Protection Regulation (GDPR), "
            "I am formally requesting a complete export of all personal data your "
            "organization holds about me and my account (LAW-56221).\n\n"
            "This includes but is not limited to:\n"
            "- Account profile information\n"
            "- Activity logs and usage history\n"
            "- Communication records\n"
            "- Billing and payment history\n"
            "- Any data shared with third parties\n\n"
            "Per GDPR Article 12, I expect a response within 30 days.\n\n"
            "Daniel O'Connor, Esq.\n"
            "O'Connor & Associates, LLP\n"
            "daniel.oconnor@law.com"
        ),
        "ground_truth": {
            "intent": "general_query",
            "order_id": "LAW-56221",
            "customer_name": "Daniel O'Connor",
            "issue_description": "Formal GDPR Article 15 data export request for all personal data held, including profile, logs, communications, billing, and third-party shared data",
            "product_name": "",
            "requested_resolution": "Complete data export within 30 days per GDPR Article 12",
            "urgency_level": "medium",
            "email_address": "daniel.oconnor@law.com",
            "response_keywords": ["GDPR", "data", "export", "request", "privacy"],
            "response_tone": "professional",
            "response_must_include": ["GDPR", "data", "LAW-56221"],
            "response_must_not_include": ["we don't comply", "not applicable"],
        },
    },
    {
        "id": "email_019",
        "from": "sophie.lee@fashion.com",
        "date": "2026-02-25 14:15:00",
        "subject": "Wrong items received - Order #FSH-82910",
        "body": (
            "Hi,\n\n"
            "I received my order #FSH-82910 today but the items are completely wrong.\n\n"
            "I ordered:\n"
            "- 2x Silk Blouse (Navy, Size M) - $79.99 each\n"
            "- 1x Cashmere Scarf (Burgundy) - $129.99\n\n"
            "I received:\n"
            "- 3x Cotton T-shirt (White, Size XL)\n"
            "- 1x Baseball Cap (Red)\n\n"
            "None of these items are what I ordered. I need the correct items sent "
            "immediately and a prepaid return label for the wrong items.\n\n"
            "This is very frustrating as I needed the blouses for an event this Saturday.\n\n"
            "Sophie Lee\n"
            "sophie.lee@fashion.com"
        ),
        "ground_truth": {
            "intent": "complaint",
            "order_id": "FSH-82910",
            "customer_name": "Sophie Lee",
            "issue_description": "Received completely wrong items - ordered silk blouses and cashmere scarf but received cotton t-shirts and baseball cap, needs correct items for event this Saturday",
            "product_name": "Silk Blouse, Cashmere Scarf",
            "requested_resolution": "Send correct items immediately and provide prepaid return label for wrong items",
            "urgency_level": "high",
            "email_address": "sophie.lee@fashion.com",
            "response_keywords": ["apolog", "correct items", "return label", "ship", "order"],
            "response_tone": "empathetic",
            "response_must_include": ["apolog", "FSH-82910", "return"],
            "response_must_not_include": ["you ordered wrong", "no exchange"],
        },
    },
    {
        "id": "email_020",
        "from": "mark.taylor@energy.com",
        "date": "2026-02-24 11:45:00",
        "subject": "API rate limit increase request - Account ENR-71150",
        "body": (
            "Hello API Team,\n\n"
            "We're hitting our API rate limits (currently 1,000 requests/minute) during "
            "peak hours (9 AM - 5 PM EST). Our usage has grown significantly since we "
            "onboarded 15 new client integrations last month.\n\n"
            "Current plan: Business Tier (ENR-71150)\n"
            "Current limit: 1,000 req/min\n"
            "Needed: 5,000 req/min\n\n"
            "We're willing to upgrade to a higher tier if needed. Could you also provide "
            "documentation on your burst rate handling?\n\n"
            "Best,\n"
            "Mark Taylor\n"
            "Engineering Manager\n"
            "mark.taylor@energy.com"
        ),
        "ground_truth": {
            "intent": "technical_support",
            "order_id": "ENR-71150",
            "customer_name": "Mark Taylor",
            "issue_description": "Hitting API rate limits of 1,000 req/min during peak hours, need increase to 5,000 req/min due to 15 new client integrations, willing to upgrade tier",
            "product_name": "Business Tier API",
            "requested_resolution": "Increase API rate limit to 5,000 req/min and provide burst rate documentation",
            "urgency_level": "medium",
            "email_address": "mark.taylor@energy.com",
            "response_keywords": ["rate limit", "upgrade", "tier", "documentation", "team"],
            "response_tone": "professional",
            "response_must_include": ["rate limit", "ENR-71150"],
            "response_must_not_include": ["cannot increase", "not possible"],
        },
    },
]


def get_email_by_id(email_id: str) -> dict | None:
    """Retrieve an email by its ID."""
    for email in EMAILS:
        if email["id"] == email_id:
            return email
    return None


def get_all_email_ids() -> list[str]:
    """Return all available email IDs."""
    return [e["id"] for e in EMAILS]


def get_random_email(rng=None) -> dict:
    """Return a random email from the dataset."""
    import random
    if rng is None:
        rng = random
    return rng.choice(EMAILS)
