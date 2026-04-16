from browser_use import Agent, Browser, ChatAnthropic
from dotenv import load_dotenv
import os
import asyncio
import requests
import re

load_dotenv()

def validate_user_creation_data(task_description: str):
    """Checks if required data is present for creation tasks before launching the browser."""
    task_lower = task_description.lower()
    
    # Only validate for creation tasks
    if any(word in task_lower for word in ["create", "add", "new", "register"]):
        missing = []
        
        # 1. Email Check
        if not re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", task_description):
            missing.append("Email")
            
        # 2. Password Check
        if "password" not in task_lower and not re.search(r"pass\w*", task_lower):
            missing.append("Password")
            
        # 3. Name Check (Stricter)
        name_match = False
        keywords = ["create", "user", "called", "name", "named", "with", "password", "email", "pass", "add", "new"]
        words = re.findall(r'\b\w+\b', task_description)
        for word in words:
            if word.lower() not in keywords and len(word) > 1:
                name_match = True
                break
        
        if not name_match:
            missing.append("Name")
            
        return missing
    return []

async def run_agent(task_description: str):
    # 1. Pre-Flight Validation (Instant)
    missing_fields = validate_user_creation_data(task_description)
    if missing_fields:
        error_msg = f"ERROR: Missing data! To create a user, I need: {', '.join(missing_fields)}. Please provide them."
        print(f"\n[Validation Failed] {error_msg}")
        try:
            requests.post("http://127.0.0.1:5050/agent/log_step", json={"message": error_msg}, timeout=2)
            requests.post("http://127.0.0.1:5050/agent/report", json={
                "task": task_description[:50],
                "success": False,
                "message": error_msg
            }, timeout=5)
        except:
            pass
        return 

    # 2. Ultra-Turbo Browser Config (Persistent Session)
    browser = Browser(
        headless=False,
        user_data_dir="./browser_session", 
        wait_for_network_idle_page_load_time=0.1,
        wait_between_actions=0,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-save-password-bubble",
            "--disable-infobars"
        ]
    )

    # 3. Model: Haiku 4.5 
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    def log_to_dashboard(msg):
        try:
            requests.post("http://127.0.0.1:5050/agent/log_step", json={"message": msg}, timeout=2)
        except:
            pass

    async def throttle(agent_instance: Agent):
        if agent_instance.history.history:
            last_step = agent_instance.history.history[-1]
            if last_step.model_output and last_step.model_output.action:
                for action in last_step.model_output.action:
                    action_data = action.model_dump()
                    action_name = next((k for k, v in action_data.items() if v is not None), "browser action")
                    log_to_dashboard(f"Action: {action_name.replace('_', ' ')}")
        pass

    # Ultra-Turbo Flash Prompt (Refined for Password Action Distinction)
    # Rules added for "Modify" vs "Reset Link"
    strict_task = (
        f"Goal: {task_description}\n\n"
        f"LAZY LOGIN: Go to http://127.0.0.1:5050. If the dashboard is visible, SKIP LOGIN.\n"
        f"DUPLICATE CHECK (Creation tasks): If creating a user, check if a user with same email exists.\n"
        f"  - IF EXISTS: STOP IMMEDIATELY and call 'done' with success=False and message 'Another user with same credentials already exists'.\n"
        f"  - IF NOT EXISTS: Proceed.\n"
        f"PASSWORD ACTION RULES:\n"
        f"  - COMMAND INCLUDES 'send' AND 'link' (e.g. 'send password reset link'): Click the 'Reset Password' button in the User Directory table.\n"
        f"  - COMMAND INCLUDES 'reset' OR 'change' OR 'modify' AND context is data (e.g. 'reset password to 123'): Click 'Edit', enter new password in form, and Update User.\n"
        f"  - DEFAULT: ALWAYS click 'Edit' to update data unless 'link' is specifically requested.\n"
        f"ONE-STEP: Fill forms and click Save in ONE turn.\n"
        f"STRICT RULES: NEVER use the 'wait' tool. No password bubbles."
    )

    log_to_dashboard("Initializing Agent. Pre-flight validation passed.")
    
    success = False
    message = ""

    try:
        agent = Agent(
            task=strict_task,
            llm=llm,
            browser=browser,
            use_vision=True, 
            include_attributes=['id', 'name', 'type', 'placeholder', 'text'],
            llm_screenshot_size=(800, 600),
            max_actions_per_step=15, 
            max_failures=1,
            use_thinking=False,
            flash_mode=True
        )

        history = await agent.run(max_steps=8, on_step_end=throttle) 
        
        if history.is_done() and history.is_successful():
            # Safely extract the final message from the 'done' action
            final_msg = ""
            if history.history and history.history[-1].model_output:
                for action in history.history[-1].model_output.action:
                    # Use getattr to safely check for 'done' attribute (Pydantic model)
                    done_act = getattr(action, 'done', None)
                    if done_act:
                        final_msg = getattr(done_act, 'text', "")
                        break
            
            if "already exists" in final_msg.lower():
                success = False
                message = "Aborted: Another user with same credentials already exists."
            else:
                success = True
                message = "Saved successfully"
            
            log_to_dashboard(f"{message}")
        else:
            errors = []
            for h in history.history:
                for r in h.result:
                    if r.error:
                        errors.append(r.error)
            message = errors[-1] if errors else "Task stopped."
            log_to_dashboard(f"Stopped: {message[:30]}")

    except Exception as e:
        message = f"Exception: {str(e)}"
        log_to_dashboard(f"Error: {str(e)[:30]}")
    finally:
        try:
            await browser.stop()
        except:
            pass

    try:
        requests.post("http://127.0.0.1:5050/agent/report", json={
            "task": task_description[:50],
            "success": success,
            "message": message[:100]
        }, timeout=5)
    except:
        pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.exit(1)
    task = sys.argv[1]
    asyncio.run(run_agent(task))
