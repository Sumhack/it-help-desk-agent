# IT Helpdesk Agent – AI Powered Support  

## 📌 Overview  
This project is a proof-of-concept for an **AI-powered IT Helpdesk Agent**.  
The agent leverages the **Strands framework** to orchestrate tools and workflows, and integrates with **Anthropic’s Claude models** (via **Amazon Bedrock**) to process requests, understand context, and automate IT support tasks.  

The goal is to **reduce manual workload** for IT teams by automating repetitive queries and enabling intelligent assistance for employees.  

---

## 🚀 Use Cases & Tools  
The agent comes with a suite of IT Helpdesk tools, including:  

- **`handle_password_reset`** – Guides users through secure password reset workflows.  
- **`handle_software_request`** – Automates software access/license requests.  
- **`handle_hardware_request`** – Manages hardware provisioning requests.  
- **`handle_cloud_request`** – Automates the cloud service request by clarifying the project code and owner name.
- **`handle_onboarding_request`** – Automates the onboarding of an employee to a new project by providing access to all the resources, and listing softwares required for the new project
- **`ambiguous_query_handler`** – Handles vague/unclear queries by asking clarifying questions.  

👉 These tools can be extended to connect with external APIs like **Jira** and **ServiceNow** for ticket management and workflow automation.  

---

## 🛠 Tech Stack  
- **Framework**: [Strands](https://github.com/strands-framework) – for agent and tool orchestration  
- **LLM**: [Anthropic Claude](https://www.anthropic.com/) via **Amazon Bedrock**  
- **Cloud**: AWS (planned deployment on **AgentCore** for scalable hosting)  
- **Languages**: Python  

---

## 📂 Repository Structure  
