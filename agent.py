import os
import asyncio
from browser_use import Agent, Browser, ChatGoogle
from dotenv import load_dotenv

load_dotenv()

async def run_agent(task_description: str):
    # Configure the browser to be visible so we can "see" what's happening (optional)
    browser = Browser(headless=True)

    # Initialize Gemini
    llm = ChatGoogle(
        model="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    # Define the agent
    agent = Agent(
        task=f"Go to http://127.0.0.1:5051. Login with username 'admin' and password 'admin'. Then: {task_description}",
        llm=llm,
        browser=browser,
        # Optimizations to reduce API calls and tokens
        use_vision='auto',
        vision_detail_level='low',
        include_attributes=['id', 'name', 'type', 'role', 'value', 'placeholder', 'title'],
        llm_screenshot_size=(1280, 720),
        max_actions_per_step=5
    )

    # Execute the task
    result = await agent.run()
    print(f"\nFinal Result: {result}")
    
    await browser.stop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python agent.py '[task description]'")
        sys.exit(1)
    
    task = sys.argv[1]
    asyncio.run(run_agent(task))
