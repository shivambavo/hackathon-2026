#!/usr/bin/env python3
"""
Test script to verify the LinkedIn scraper setup
"""
import asyncio
from linkedin_scraper import BrowserManager

async def test_browser():
    """Test that Playwright browser works correctly"""
    print("🔧 Testing browser setup...")
    
    try:
        # Test browser initialization
        async with BrowserManager(headless=True) as browser:
            # Test navigation to a simple page
            await browser.page.goto("https://httpbin.org/html")
            title = await browser.page.title()
            print(f"✓ Browser working! Page title: {title}")
            
        print("✅ Setup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_browser())
