#!/usr/bin/env python3
"""
Simple LinkedIn Activity Checker
Checks for posts and provides manual verification
"""
import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

class SimpleActivityChecker:
    def __init__(self):
        self.browser_manager = None
        
    async def __aenter__(self):
        self.browser_manager = BrowserManager(headless=False)  # Use visible browser for manual checking
        await self.browser_manager.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser_manager:
            await self.browser_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    async def check_profile_activity(self, profile_url: str) -> Dict[str, Any]:
        """Check profile for activity indicators"""
        print(f"🔍 Checking activity for: {profile_url}")
        
        # Load LinkedIn session
        try:
            await self.browser_manager.load_session("linkedin_session.json")
            print("✓ LinkedIn session loaded")
        except Exception as e:
            print(f"❌ Failed to load LinkedIn session: {e}")
            return None
        
        # Navigate to profile
        print("🌐 Opening profile...")
        await self.browser_manager.page.goto(profile_url)
        await self.browser_manager.page.wait_for_load_state('networkidle')
        
        # Get basic profile data
        print("👤 Extracting profile data...")
        scraper = PersonScraper(self.browser_manager.page)
        
        try:
            linkedin_person = await scraper.scrape(profile_url)
            profile_data = linkedin_person.model_dump()
            person_name = profile_data.get('name', 'Unknown')
            print(f"✓ Profile data: {person_name}")
        except Exception as e:
            print(f"❌ Profile scraping failed: {e}")
            return None
        
        # Check for activity indicators
        print("🔍 Looking for activity indicators...")
        activity_indicators = await self.check_activity_indicators()
        
        # Try to find posts section
        print("📝 Attempting to find posts section...")
        posts_info = await self.try_find_posts_section()
        
        # Try to find articles section
        print("📄 Attempting to find articles section...")
        articles_info = await self.try_find_articles_section()
        
        # Compile activity report
        activity_report = {
            'person_name': person_name,
            'scraped_at': datetime.now().isoformat(),
            'profile_data': profile_data,
            'activity_indicators': activity_indicators,
            'posts_section': posts_info,
            'articles_section': articles_info,
            'manual_check_required': True,
            'recommendations': self.generate_recommendations(activity_indicators, posts_info, articles_info)
        }
        
        return activity_report
    
    async def check_activity_indicators(self) -> Dict[str, Any]:
        """Check for various activity indicators on the profile"""
        indicators = {
            'has_posts_tab': False,
            'has_articles_tab': False,
            'has_activity_section': False,
            'has_recent_updates': False,
            'profile_completeness': 0,
            'visible_elements': []
        }
        
        try:
            # Check for posts tab
            posts_selectors = [
                'a[href*="posts"]',
                'button:has-text("Posts")',
                '[data-test-id="nav-posts"]'
            ]
            
            for selector in posts_selectors:
                try:
                    element = await self.browser_manager.page.query_selector(selector)
                    if element:
                        indicators['has_posts_tab'] = True
                        indicators['visible_elements'].append('posts_tab')
                        break
                except:
                    continue
            
            # Check for articles tab
            articles_selectors = [
                'a[href*="articles"]',
                'button:has-text("Articles")',
                '[data-test-id="nav-articles"]'
            ]
            
            for selector in articles_selectors:
                try:
                    element = await self.browser_manager.page.query_selector(selector)
                    if element:
                        indicators['has_articles_tab'] = True
                        indicators['visible_elements'].append('articles_tab')
                        break
                except:
                    continue
            
            # Check for activity section
            activity_selectors = [
                '[data-test-id="activity-section"]',
                '.activity-section',
                '[data-test-id="feed-shared-update-v2"]'
            ]
            
            for selector in activity_selectors:
                try:
                    elements = await self.browser_manager.page.query_selector_all(selector)
                    if elements:
                        indicators['has_activity_section'] = True
                        indicators['visible_elements'].append('activity_section')
                        break
                except:
                    continue
            
            # Calculate profile completeness
            page_text = await self.browser_manager.page.evaluate('() => document.body.innerText')
            if page_text:
                text_length = len(page_text)
                if text_length > 1000:
                    indicators['profile_completeness'] = min(100, text_length / 50)
                    indicators['has_recent_updates'] = True
            
        except Exception as e:
            print(f"    Error checking indicators: {e}")
        
        return indicators
    
    async def try_find_posts_section(self) -> Dict[str, Any]:
        """Try to navigate to and analyze posts section"""
        posts_info = {
            'accessible': False,
            'posts_found': 0,
            'error_message': '',
            'manual_steps': []
        }
        
        try:
            # Look for posts navigation
            posts_nav_selectors = [
                'a[href*="posts"]',
                'button:has-text("Posts")',
                'a:has-text("Posts")'
            ]
            
            for selector in posts_nav_selectors:
                try:
                    nav_element = await self.browser_manager.page.query_selector(selector)
                    if nav_element:
                        await nav_element.click()
                        await self.browser_manager.page.wait_for_load_state('networkidle')
                        await asyncio.sleep(2)
                        
                        posts_info['accessible'] = True
                        posts_info['manual_steps'].append(f"Clicked on posts navigation using: {selector}")
                        
                        # Try to count posts
                        post_selectors = [
                            '[data-test-id="feed-shared-update-v2"]',
                            '.feed-shared-update-v2',
                            '[data-urn*="post"]'
                        ]
                        
                        for post_selector in post_selectors:
                            try:
                                posts = await self.browser_manager.page.query_selector_all(post_selector)
                                posts_info['posts_found'] = len(posts)
                                if posts_info['posts_found'] > 0:
                                    posts_info['manual_steps'].append(f"Found {len(posts)} posts using: {post_selector}")
                                    break
                            except:
                                continue
                        
                        break
                except Exception as e:
                    posts_info['error_message'] = str(e)
                    continue
            
        except Exception as e:
            posts_info['error_message'] = str(e)
        
        return posts_info
    
    async def try_find_articles_section(self) -> Dict[str, Any]:
        """Try to navigate to and analyze articles section"""
        articles_info = {
            'accessible': False,
            'articles_found': 0,
            'error_message': '',
            'manual_steps': []
        }
        
        try:
            # Look for articles navigation
            articles_nav_selectors = [
                'a[href*="articles"]',
                'button:has-text("Articles")',
                'a:has-text("Articles")'
            ]
            
            for selector in articles_nav_selectors:
                try:
                    nav_element = await self.browser_manager.page.query_selector(selector)
                    if nav_element:
                        await nav_element.click()
                        await self.browser_manager.page.wait_for_load_state('networkidle')
                        await asyncio.sleep(2)
                        
                        articles_info['accessible'] = True
                        articles_info['manual_steps'].append(f"Clicked on articles navigation using: {selector}")
                        
                        # Try to count articles
                        article_selectors = [
                            '[data-test-id="article-item"]',
                            '.article-item',
                            'a[href*="/article/"]'
                        ]
                        
                        for article_selector in article_selectors:
                            try:
                                articles = await self.browser_manager.page.query_selector_all(article_selector)
                                articles_info['articles_found'] = len(articles)
                                if articles_info['articles_found'] > 0:
                                    articles_info['manual_steps'].append(f"Found {len(articles)} articles using: {article_selector}")
                                    break
                            except:
                                continue
                        
                        break
                except Exception as e:
                    articles_info['error_message'] = str(e)
                    continue
            
        except Exception as e:
            articles_info['error_message'] = str(e)
        
        return articles_info
    
    def generate_recommendations(self, indicators: Dict, posts_info: Dict, articles_info: Dict) -> List[str]:
        """Generate recommendations based on findings"""
        recommendations = []
        
        if indicators['has_posts_tab']:
            recommendations.append("✅ Posts tab is available - navigate manually to view posts")
        else:
            recommendations.append("❌ Posts tab not found - user may not have public posts")
        
        if indicators['has_articles_tab']:
            recommendations.append("✅ Articles tab is available - navigate manually to view articles")
        else:
            recommendations.append("❌ Articles tab not found - user may not have published articles")
        
        if posts_info['accessible'] and posts_info['posts_found'] > 0:
            recommendations.append(f"✅ Found {posts_info['posts_found']} posts - check browser for content")
        elif posts_info['accessible']:
            recommendations.append("⚠️  Posts section accessible but no posts found - may be empty or private")
        
        if articles_info['accessible'] and articles_info['articles_found'] > 0:
            recommendations.append(f"✅ Found {articles_info['articles_found']} articles - check browser for content")
        elif articles_info['accessible']:
            recommendations.append("⚠️  Articles section accessible but no articles found - may be empty")
        
        if not indicators['has_posts_tab'] and not indicators['has_articles_tab']:
            recommendations.append("ℹ️  Profile may have limited public activity or privacy settings")
        
        if indicators['profile_completeness'] > 50:
            recommendations.append("✅ Profile appears complete with substantial content")
        else:
            recommendations.append("⚠️  Profile appears incomplete - limited public information")
        
        return recommendations
    
    async def save_activity_report(self, report: Dict[str, Any]) -> str:
        """Save activity report to JSON file"""
        person_name = report['person_name']
        filename = f"extracted/{person_name.replace(' ', '_')}_activity_report.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Activity report saved to: {filename}")
        return filename

async def main():
    """Main function"""
    print("🔍 Simple LinkedIn Activity Checker")
    print("Checks for posts, articles, and provides manual verification\n")
    
    # Get input
    profile_url = input("Enter LinkedIn profile URL (or press Enter for Bill Gates): ").strip()
    
    if not profile_url:
        profile_url = "https://www.linkedin.com/in/williamhgates/"
    
    if "linkedin.com/in/" not in profile_url:
        print("❌ Invalid LinkedIn profile URL")
        return
    
    print("🌐 Opening browser for manual verification...")
    print("⚠️  Browser will remain open so you can manually check for posts/articles")
    
    async with SimpleActivityChecker() as checker:
        report = await checker.check_profile_activity(profile_url)
        
        if report:
            filename = await checker.save_activity_report(report)
            
            # Print summary
            indicators = report['activity_indicators']
            posts = report['posts_section']
            articles = report['articles_section']
            
            print(f"\n🔍 ACTIVITY CHECK SUMMARY:")
            print(f"  Person: {report['person_name']}")
            print(f"  Posts Tab Available: {indicators['has_posts_tab']}")
            print(f"  Articles Tab Available: {indicators['has_articles_tab']}")
            print(f"  Activity Section: {indicators['has_activity_section']}")
            print(f"  Profile Completeness: {indicators['profile_completeness']:.1f}%")
            
            print(f"\n📝 POSTS SECTION:")
            print(f"  Accessible: {posts['accessible']}")
            print(f"  Posts Found: {posts['posts_found']}")
            if posts['error_message']:
                print(f"  Error: {posts['error_message']}")
            
            print(f"\n📄 ARTICLES SECTION:")
            print(f"  Accessible: {articles['accessible']}")
            print(f"  Articles Found: {articles['articles_found']}")
            if articles['error_message']:
                print(f"  Error: {articles['error_message']}")
            
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                print(f"  {rec}")
            
            print(f"\n🌐 Browser remains open for manual verification")
            print(f"✅ Activity report saved to: {filename}")
            
            # Keep browser open for manual inspection
            input("\nPress Enter to close browser and finish...")
            
        else:
            print("❌ Failed to create activity report")

if __name__ == "__main__":
    asyncio.run(main())
