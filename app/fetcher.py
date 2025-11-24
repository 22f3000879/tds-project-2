from playwright.async_api import async_playwright

async def fetch_page(url: str) -> str:
    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Go to URL and wait for client-side rendering
        await page.goto(url)
        
        # Wait for the body to ensure content loads (adjust selector if needed)
        try:
            await page.wait_for_selector("body", timeout=5000)
        except:
            pass # Proceed even if timeout, in case page structure differs
            
        content = await page.content()
        await browser.close()
        return content
