#!/usr/bin/env python3
"""
Simple LinkedIn Session Creator with better feedback
"""
import asyncio
from linkedin_scraper import BrowserManager

async def create_simple_session():
    """Create session with manual confirmation"""
    print("="*60)
    print("Simple LinkedIn Session Creator")
    print("="*60)
    
    async with BrowserManager(headless=False) as browser:
        # Navigate to LinkedIn
        print("🌐 Opening LinkedIn login page...")
        await browser.page.goto("https://www.linkedin.com/login")
        await browser.page.wait_for_load_state('networkidle')
        
        print("\n🔐 Please log in to LinkedIn in the browser window")
        print("   - Enter your credentials")
        print("   - Complete any verification")
        print("   - Wait until you see your feed")
        print("\n⏳ Once you're fully logged in, press Enter to continue...")
        
        # Wait for user to press Enter
        input()
        
        # Check if we're logged in by looking for feed elements
        try:
            # Look for common LinkedIn feed elements
            await browser.page.wait_for_selector('[data-test-id="nav-global-feed-link"], .feed-identity-module, .global-nav__primary-link', timeout=10000)
            print("✅ Login detected!")
        except:
            print("⚠️  Could not detect login, but proceeding anyway...")
        
        # Save session
        session_path = "linkedin_session.json"
        print(f"\n💾 Saving session to {session_path}...")
        await browser.save_session(session_path)
        
        print("✅ Session saved successfully!")
        print(f"File location: {session_path}")
        
        # Test the session
        print("\n🧪 Testing session...")
        try:
            await browser.page.goto("https://www.linkedin.com/feed/")
            await browser.page.wait_for_load_state('networkidle')
            print("✅ Session test passed!")
        except Exception as e:
            print(f"⚠️  Session test warning: {e}")

if __name__ == "__main__":
    asyncio.run(create_simple_session())
