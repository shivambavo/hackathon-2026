#!/usr/bin/env python3
"""
LinkedIn Activity Scraper
Extracts posts, articles, and activity from LinkedIn profiles
"""
import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

class LinkedInActivityScraper:
    def __init__(self):
        self.browser_manager = None
        
    async def __aenter__(self):
        self.browser_manager = BrowserManager(headless=True)
        await self.browser_manager.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser_manager:
            await self.browser_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    async def extract_posts(self, profile_url: str) -> List[Dict[str, Any]]:
        """Extract posts from LinkedIn profile activity section"""
        try:
            print("📝 Extracting posts and activity...")
            
            # Navigate to profile
            await self.browser_manager.page.goto(profile_url)
            await self.browser_manager.page.wait_for_load_state('networkidle')
            
            # Try to find activity/posts section
            posts = []
            
            # Method 1: Look for posts in the main feed area
            post_selectors = [
                '[data-test-id="feed-shared-update-v2"]',
                '.feed-shared-update-v2',
                '[data-urn*="post"]',
                '.occludable-update'
            ]
            
            for selector in post_selectors:
                try:
                    post_elements = await self.browser_manager.page.query_selector_all(selector)
                    if post_elements:
                        print(f"  Found {len(post_elements)} posts with selector: {selector}")
                        
                        for i, post_element in enumerate(post_elements[:10]):  # Limit to 10 posts
                            post_data = await self.extract_post_data(post_element, i)
                            if post_data:
                                posts.append(post_data)
                        
                        if posts:
                            break
                except Exception as e:
                    print(f"  Selector {selector} failed: {e}")
                    continue
            
            # Method 2: Try to click on posts section
            if not posts:
                try:
                    # Look for posts tab or link
                    posts_tab_selectors = [
                        'a[href*="posts"]',
                        'button:has-text("Posts")',
                        '[data-test-id="nav-posts"]',
                        'a:has-text("Posts")'
                    ]
                    
                    for tab_selector in posts_tab_selectors:
                        try:
                            tab = await self.browser_manager.page.wait_for_selector(tab_selector, timeout=5000)
                            if tab:
                                await tab.click()
                                await self.browser_manager.page.wait_for_load_state('networkidle')
                                await asyncio.sleep(2)
                                
                                # Try extracting posts again
                                post_elements = await self.browser_manager.page.query_selector_all('[data-test-id="feed-shared-update-v2"]')
                                for i, post_element in enumerate(post_elements[:10]):
                                    post_data = await self.extract_post_data(post_element, i)
                                    if post_data:
                                        posts.append(post_data)
                                
                                if posts:
                                    break
                        except:
                            continue
                except Exception as e:
                    print(f"  Posts tab navigation failed: {e}")
            
            # Method 3: Try articles section
            articles = await self.extract_articles(profile_url)
            
            return {
                'posts': posts,
                'articles': articles,
                'total_posts': len(posts),
                'total_articles': len(articles)
            }
            
        except Exception as e:
            print(f"❌ Post extraction failed: {e}")
            return {'posts': [], 'articles': [], 'total_posts': 0, 'total_articles': 0}
    
    async def extract_post_data(self, post_element, index: int) -> Dict[str, Any]:
        """Extract data from a single post element"""
        try:
            post_data = {
                'index': index,
                'type': 'post',
                'text': '',
                'date': '',
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'media_urls': []
            }
            
            # Extract post text
            text_selectors = [
                '[data-test-id="feed-shared-text"]',
                '.feed-shared-text',
                '.feed-shared-mini-update-v2__text',
                'span[aria-label*="post"]'
            ]
            
            for selector in text_selectors:
                try:
                    text_element = await post_element.query_selector(selector)
                    if text_element:
                        text = await text_element.inner_text()
                        if text and len(text.strip()) > 0:
                            post_data['text'] = text.strip()
                            break
                except:
                    continue
            
            # Extract date/time
            date_selectors = [
                '[data-test-id="feed-shared-time"]',
                '.feed-shared-time',
                'time',
                'span:has-text("ago")'
            ]
            
            for selector in date_selectors:
                try:
                    date_element = await post_element.query_selector(selector)
                    if date_element:
                        date_text = await date_element.inner_text()
                        if date_text:
                            post_data['date'] = date_text.strip()
                            break
                except:
                    continue
            
            # Extract engagement metrics
            engagement_selectors = [
                ('likes', '[data-test-id="social-actions__reaction-count"]'),
                ('comments', '[data-test-id="social-actions__comment-count"]'),
                ('shares', '[data-test-id="social-actions__share-count"]')
            ]
            
            for metric, selector in engagement_selectors:
                try:
                    element = await post_element.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        # Extract number from text
                        import re
                        number = re.search(r'(\d+)', text.replace(',', ''))
                        if number:
                            post_data[metric] = int(number.group(1))
                except:
                    continue
            
            # Extract media URLs
            try:
                img_elements = await post_element.query_selector_all('img')
                for img in img_elements:
                    src = await img.get_attribute('src')
                    if src and 'media' in src:
                        post_data['media_urls'].append(src)
            except:
                pass
            
            # Only return if we have meaningful content
            if post_data['text'] or post_data['date']:
                return post_data
            
        except Exception as e:
            print(f"    Error extracting post {index}: {e}")
        
        return None
    
    async def extract_articles(self, profile_url: str) -> List[Dict[str, Any]]:
        """Extract articles from LinkedIn profile"""
        try:
            print("📄 Extracting articles...")
            
            # Look for articles section
            articles_tab_selectors = [
                'a[href*="articles"]',
                'button:has-text("Articles")',
                '[data-test-id="nav-articles"]'
            ]
            
            for tab_selector in articles_tab_selectors:
                try:
                    tab = await self.browser_manager.page.wait_for_selector(tab_selector, timeout=5000)
                    if tab:
                        await tab.click()
                        await self.browser_manager.page.wait_for_load_state('networkidle')
                        await asyncio.sleep(2)
                        
                        # Extract articles
                        article_selectors = [
                            '[data-test-id="article-item"]',
                            '.article-item',
                            'a[href*="/article/"]'
                        ]
                        
                        for selector in article_selectors:
                            try:
                                article_elements = await self.browser_manager.page.query_selector_all(selector)
                                articles = []
                                
                                for i, article_element in enumerate(article_elements[:5]):  # Limit to 5 articles
                                    article_data = await self.extract_article_data(article_element, i)
                                    if article_data:
                                        articles.append(article_data)
                                
                                if articles:
                                    return articles
                            except:
                                continue
                        
                        break
                except:
                    continue
            
            return []
            
        except Exception as e:
            print(f"❌ Article extraction failed: {e}")
            return []
    
    async def extract_article_data(self, article_element, index: int) -> Dict[str, Any]:
        """Extract data from a single article element"""
        try:
            article_data = {
                'index': index,
                'type': 'article',
                'title': '',
                'description': '',
                'url': '',
                'date': '',
                'read_time': '',
                'image_url': ''
            }
            
            # Extract title
            try:
                title_element = await article_element.query_selector('h3, .article-title, a')
                if title_element:
                    title = await title_element.inner_text()
                    article_data['title'] = title.strip()
                    
                    # Try to get URL from link
                    url = await title_element.get_attribute('href')
                    if url:
                        article_data['url'] = url
            except:
                pass
            
            # Extract description
            try:
                desc_element = await article_element.query_selector('.article-description, p')
                if desc_element:
                    desc = await desc_element.inner_text()
                    article_data['description'] = desc.strip()
            except:
                pass
            
            # Extract date
            try:
                date_element = await article_element.query_selector('time, .article-date')
                if date_element:
                    date = await date_element.inner_text()
                    article_data['date'] = date.strip()
            except:
                pass
            
            # Extract image
            try:
                img_element = await article_element.query_selector('img')
                if img_element:
                    src = await img_element.get_attribute('src')
                    if src:
                        article_data['image_url'] = src
            except:
                pass
            
            # Only return if we have meaningful content
            if article_data['title']:
                return article_data
            
        except Exception as e:
            print(f"    Error extracting article {index}: {e}")
        
        return None
    
    async def get_complete_profile_with_activity(self, profile_url: str) -> Dict[str, Any]:
        """Get complete profile including activity"""
        print(f"📊 Complete profile analysis with activity: {profile_url}")
        
        # Load LinkedIn session
        try:
            await self.browser_manager.load_session("linkedin_session.json")
            print("✓ LinkedIn session loaded")
        except Exception as e:
            print(f"❌ Failed to load LinkedIn session: {e}")
            return None
        
        # Get basic profile data
        print("👤 Step 1: Extracting basic profile data...")
        scraper = PersonScraper(self.browser_manager.page)
        
        try:
            linkedin_person = await scraper.scrape(profile_url)
            profile_data = linkedin_person.model_dump()
            person_name = profile_data.get('name', 'Unknown')
            print(f"✓ Profile data: {person_name}")
        except Exception as e:
            print(f"❌ Profile scraping failed: {e}")
            return None
        
        # Get activity data
        print("📝 Step 2: Extracting posts and articles...")
        activity_data = await self.extract_posts(profile_url)
        
        # Compile complete profile
        complete_profile = {
            'person_name': person_name,
            'scraped_at': datetime.now().isoformat(),
            'profile_data': profile_data,
            'activity_data': activity_data,
            'activity_summary': {
                'total_posts': activity_data['total_posts'],
                'total_articles': activity_data['total_articles'],
                'has_recent_activity': activity_data['total_posts'] > 0 or activity_data['total_articles'] > 0,
                'content_types': []
            }
        }
        
        # Determine content types
        if activity_data['total_posts'] > 0:
            complete_profile['activity_summary']['content_types'].append('posts')
        if activity_data['total_articles'] > 0:
            complete_profile['activity_summary']['content_types'].append('articles')
        
        return complete_profile
    
    async def save_complete_profile(self, profile: Dict[str, Any]) -> str:
        """Save complete profile with activity to JSON file"""
        person_name = profile['person_name']
        filename = f"extracted/{person_name.replace(' ', '_')}_complete_profile.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Complete profile with activity saved to: {filename}")
        return filename

async def main():
    """Main function"""
    print("📊 LinkedIn Activity Scraper")
    print("Extracts posts, articles, and complete profile data\n")
    
    # Get input
    profile_url = input("Enter LinkedIn profile URL (or press Enter for Bill Gates): ").strip()
    
    if not profile_url:
        profile_url = "https://www.linkedin.com/in/williamhgates/"
    
    if "linkedin.com/in/" not in profile_url:
        print("❌ Invalid LinkedIn profile URL")
        return
    
    async with LinkedInActivityScraper() as scraper:
        profile = await scraper.get_complete_profile_with_activity(profile_url)
        
        if profile:
            filename = await scraper.save_complete_profile(profile)
            
            # Print summary
            activity = profile['activity_summary']
            print(f"\n📊 ACTIVITY SUMMARY:")
            print(f"  Person: {profile['person_name']}")
            print(f"  Posts Found: {activity['total_posts']}")
            print(f"  Articles Found: {activity['total_articles']}")
            print(f"  Recent Activity: {activity['has_recent_activity']}")
            print(f"  Content Types: {', '.join(activity['content_types']) if activity['content_types'] else 'None'}")
            
            # Show sample posts
            if activity['total_posts'] > 0:
                print(f"\n📝 SAMPLE POSTS:")
                for i, post in enumerate(profile['activity_data']['posts'][:3]):
                    print(f"  {i+1}. {post['date']}")
                    text = post['text'][:100] + "..." if len(post['text']) > 100 else post['text']
                    print(f"     {text}")
                    if post['likes'] > 0:
                        print(f"     👍 {post['likes']} likes")
            
            # Show sample articles
            if activity['total_articles'] > 0:
                print(f"\n📄 SAMPLE ARTICLES:")
                for i, article in enumerate(profile['activity_data']['articles'][:3]):
                    print(f"  {i+1}. {article['title']}")
                    if article['description']:
                        desc = article['description'][:100] + "..." if len(article['description']) > 100 else article['description']
                        print(f"     {desc}")
            
            print(f"\n✅ Complete profile saved to: {filename}")
        else:
            print("❌ Failed to create complete profile")

if __name__ == "__main__":
    asyncio.run(main())
