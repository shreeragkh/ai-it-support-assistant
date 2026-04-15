import asyncio
from playwright.async_api import async_playwright

async def test_playwright():
    try:
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=True)
            print("Browser launched successfully!")
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto("http://example.com")
            print(f"Page title: {await page.title()}")
            await browser.close()
            print("Browser closed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_playwright())
