from strands import Agent, tool
import boto3
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager


AWS_DEFAULT_REGION= "<region>"
AWS_ACCESS_KEY_ID= "<access_key>"
AWS_SECRET_ACCESS_KEY= "<secret_key>"
AWS_SESSION_TOKEN="<access_token>"
# Create a custom boto3 session
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,  # If using temporary credentials
    region_name=AWS_DEFAULT_REGION,
)

# Create a Bedrock model with the custom session
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    boto_session=session,
    temperature=0.3,
    top_p=0.8,
)


# Mock catalogs
SOFTWARE_PORTAL = ["Zoom", "Slack", "VSCode"]
SOFTWARE_LICENSE = ["Tableau", "MATLAB"]
SOFTWARE_ADMIN = ["Docker", "VirtualBox"]
#software_name (optional, string): Name of the software that User is requesting.

@tool
def handle_software_request(
        request_text: str
) -> dict:
    """
    Handle software installation request.Categorize requests into: self-install (company portal), requires admin access, requires license, or ambiguous.

    Arguments:
       request_text (optional, string): User's software request in natural language

    Returns:
        - dict with category, ticket status, and details
    """

    combined_text = ""

    # Process text input
    if request_text:
        combined_text += request_text + " "

    # Process image input if available
    # if image_path:
    #     try:
    #         img = Image.open(image_path)
    #         # extracted_text = pytesseract.image_to_string(img)
    #         # combined_text += extracted_text
    #     except Exception as e:
    #         return {"error": f"Image processing failed: {str(e)}"}

    # If still empty, can't proceed
    if not combined_text.strip():
        return {"error": "No valid input provided"}

    # Simple categorization logic (could be LLM powered later)
    for sw in SOFTWARE_PORTAL:
        if sw.lower() in combined_text.lower():
            return {
                "software": sw,
                "category": "Company Portal Install",
                "ticket_needed": False,
                "response": f"{sw} can be installed from the company portal"
            }

    for sw in SOFTWARE_LICENSE:
        if sw.lower() in combined_text.lower():
            return {
                "software": sw,
                "category": "Requires License",
                "ticket_needed": True,
                "response": f"{sw} requires a paid license. Ticket will be created."
            }

    for sw in SOFTWARE_ADMIN:
        if sw.lower() in combined_text.lower():
            return {
                "software": sw,
                "category": "Needs Admin Access",
                "ticket_needed": True,
                "response": f"{sw} requires admin access. Ticket will be created."
            }

    return {
        "software": None,
        "category": "Unknown/Ambiguous",
        "ticket_needed": True,
        "response": "Software request not recognized, escalating to IT team."
    }

# Mock Data
CLOUD_SERVICES = ["AWS", "GCP", "Azure"]

PROJECT_APPROVERS = {
    "PROJ123": "Alice",
    "PROJ456": "Bob",
    "PROJ789": "Charlie"
}

@tool
def handle_cloud_request(cloud_service: str, project_code: str, approver_name: str) -> dict:
    """
    Handles AWS/GCP/Azure service requests.  
   - Checks if project code and approver information are provided.  
   - If approvals are missing, ask the user to confirm. Once complete, create a ticket.

    Inputs:
        - cloud_service (str): Name of cloud provider (AWS, GCP, etc.)
        - project_code (str): Project identifier
        - approver_name (str): Name of the approver


    Returns:
        - dict with status, ticket info, and response
    """

    # Validate cloud service
    if cloud_service not in CLOUD_SERVICES:
        return {
            "status": "rejected",
            "ticket_needed": False,
            "response": f"Cloud service '{cloud_service}' is not supported."
        }

    # Validate project
    if project_code not in PROJECT_APPROVERS:
        return {
            "status": "rejected",
            "ticket_needed": False,
            "response": f"Project '{project_code}' not found. Please provide valid project code."
        }

    # Validate approver
    expected_approver = PROJECT_APPROVERS[project_code]
    if approver_name.lower() != expected_approver.lower():
        return {
            "status": "pending_approval",
            "ticket_needed": False,
            "response": f"Approval needed from '{expected_approver}' for project {project_code}. Provided approver '{approver_name}' does not match."
        }

    # If all checks pass
    return {
        "status": "approved",
        "ticket_needed": True,
        "response": f"Request approved for {cloud_service} under project {project_code} with approver {approver_name}. Ticket will be created."
    }


# Mock Project Configuration
PROJECT_CONFIG = {
    "PROJ123": {
        "team": "Data Science",
        "required_software": ["Python", "Jupyter", "Tableau"],
        "cloud_access": ["AWS"],
        "urls": ["git.company.com/project123", "wiki.company.com/project123"],
        "ip_whitelist": ["10.0.0.5/32", "10.0.0.6/32"]
    },
    "PROJ456": {
        "team": "DevOps",
        "required_software": ["Terraform", "Docker", "Kubernetes"],
        "cloud_access": ["GCP"],
        "urls": ["git.company.com/project456", "wiki.company.com/project456"],
        "ip_whitelist": ["10.0.1.10/32"]
    }
}

@tool
def handle_onboarding(new_member: str, project_code: str) -> dict:
    """
    Handle onboarding for a new project member. When a new member joins a project, automatically provision required software, cloud, and access.  
    Verify if the user is indeed a new member before proceeding. 

    Inputs:
        - new_member (str): Name or ID of new member
        - project_code (str): Project identifier

    Returns:
        - dict with required software, cloud access, urls, and tickets to create
    """

    if project_code not in PROJECT_CONFIG:
        return {
            "status": "error",
            "response": f"Project {project_code} not found. Please provide valid project code."
        }

    project_info = PROJECT_CONFIG[project_code]

    tickets = []
    tickets.append("Software installation for: " + ", ".join(project_info["required_software"]))
    tickets.append("Cloud access for: " + ", ".join(project_info["cloud_access"]))
    tickets.append("IP whitelist update for: " + ", ".join(project_info["ip_whitelist"]))
   
    response = f"Provisioning initiated for {new_member} in project {project_code} for and the following tickets have been created :{tickets}"
    return response


HARDWARE_FAQ = {
    "laptop not turning on": "Please check if the laptop is connected to power and hold the power button for 10 seconds.",
    "wifi not working": "Try restarting your router or reconnecting to the company WiFi. If issue persists, contact IT.",
    "screen flickering": "Update your graphics drivers from the company portal. If it continues, request hardware replacement.",
    "printer not working": "Ensure the printer is connected to the network and drivers are installed from the company portal."
}

@tool
def handle_hardware_issue(issue_text: str, user: str = "unknown_user") -> dict:
    """
    Handle hardware issues by first checking FAQ, then escalating if unresolved. Look up FAQ answers for common issues (e.g., printer not working, laptop overheating).  

    Inputs:
        - issue_text (str): Description of hardware problem
        - user (str): Requester's ID/email (optional)

    Returns:
        - dict with suggested response or escalation
    """

    # Normalize input
    normalized_issue = issue_text.lower().strip()

    # Check FAQ
    for problem, solution in HARDWARE_FAQ.items():
        if problem in normalized_issue:
            return {
                "status": "resolved_with_faq",
                "ticket_needed": False,
                "problem": problem,
                "suggested_solution": solution,
                "response": f"Found a matching FAQ for your issue: {solution}"
            }

    # No FAQ found → escalate
    return {
        "status": "unresolved",
        "ticket_needed": True,
        "response": f"No FAQ entry found for: {issue_text}. Escalating to IT support."
    }


# from PIL import Image
import random
import string

# Dummy user database
USER_DATABASE = {
    "alice": {"email": "alice@company.com", "password": "oldpass123"},
    "bob": {"email": "bob@company.com", "password": "secure456"},
}


def generate_temp_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@tool
def handle_password_reset(user: str) -> dict:
    """
    Handle password reset requests. Walk users through a secure reset process.  
   - If unsuccessful after self-service, escalate to IT with a ticket.  

    Inputs:
        - user (str): Username or email

    Returns:
        - dict with reset status and instructions
    """
    user = user.lower()
    if user not in USER_DATABASE:
        return {
            "status": "error",
            "response": f"User '{user}' not found in system."
        }

    # Simulate password reset by generating temporary password
    temp_password = generate_temp_password()
    USER_DATABASE[user]["password"] = temp_password

    return {
        "status": "password_reset",
        "user": user,
        "response": f"Password reset successful. A reset link or temporary password has been sent to {USER_DATABASE[user]['email']}.",
        "temporary_password": temp_password
    }

@tool
def handle_ambiguous_query(query: str, user: str = "unknown_user") -> dict:
    """
    Handle queries that don't map to any known IT helpdesk tool.

    Inputs:
        - query (str): User's raw query
        - user (str): User making the request (optional)

    Returns:
        - response (str): response with action needed for the same
    """

    response = "Ticket has been created for your issue."
    return response


# Create a conversation manager with custom window size
conversation_manager = SlidingWindowConversationManager(
    window_size=20,  # Maximum number of messages to keep
    should_truncate_results=True, # Enable truncating the tool result when a message is too large for the model's context window 
)



IT_SYSTEM_PROMPT = """You are an IT Helpdesk Agent for a large organization.  
Your goal is to help employees resolve IT issues quickly by either solving them directly or routing them to the correct workflow/tool.  



Additional Instructions:  
- Always ask clarifying questions if information is missing.  
- Be proactive: if a request needs approvals or licensing, check before creating a ticket.  
- Support multimodal input: if a user provides a screenshot/image, analyze it to better understand the problem.  
- Keep responses professional, concise, and friendly.  
- Escalate only when automation/self-service cannot resolve the issue.  
- Don't generate response on your own,for any query, just explain whatever the tool replies in concise manner. Don't mention Agent in the response just process the output.

Your objective is to reduce repetitive IT workload while keeping employees productive.  
"""

agent = Agent(
    model=bedrock_model,
    system_prompt=IT_SYSTEM_PROMPT,
    conversation_manager=conversation_manager,
    tools=[handle_software_request,handle_cloud_request,handle_onboarding,handle_hardware_issue,handle_password_reset,handle_ambiguous_query]
)

while True:
    user_input = input("👩‍🌾 IT Help Desk Agent: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    agent_response = agent(user_input)
    print(f"🤖 Agent: {agent_response}")


