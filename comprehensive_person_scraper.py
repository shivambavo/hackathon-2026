#!/usr/bin/env python3
"""
Comprehensive Person Scraper
Combines LinkedIn data with Google search results for complete profile
"""
import asyncio
import json
import re
from typing import Dict, List, Any
from urllib.parse import quote
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

class ComprehensivePersonScraper:
    def __init__(self):
        self.browser_manager = None
        
    async def __aenter__(self):
        self.browser_manager = BrowserManager(headless=True)
        await self.browser_manager.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser_manager:
            await self.browser_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    async def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search Google and return results"""
        try:
            # Navigate to Google
            await self.browser_manager.page.goto("https://www.google.com")
            await self.browser_manager.page.wait_for_load_state('networkidle')
            
            # Accept cookies if present
            try:
                await self.browser_manager.page.click('button:has-text("Accept all")', timeout=3000)
                await self.browser_manager.page.wait_for_timeout(1000)
            except:
                pass
            
            # Search for the person
            search_box = await self.browser_manager.page.wait_for_selector('textarea[name="q"]')
            await search_box.fill(query)
            await search_box.press("Enter")
            await self.browser_manager.page.wait_for_load_state('networkidle')
            
            # Extract search results
            results = []
            search_results = await self.browser_manager.page.query_selector_all('div.g')
            
            for i, result in enumerate(search_results[:num_results]):
                try:
                    # Extract title
                    title_element = await result.query_selector('h3')
                    title = await title_element.inner_text() if title_element else "No title"
                    
                    # Extract URL
                    link_element = await result.query_selector('a')
                    url = await link_element.get_attribute('href') if link_element else ""
                    
                    # Extract description
                    desc_element = await result.query_selector('[data-snf="nke08r"]')
                    description = await desc_element.inner_text() if desc_element else ""
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'description': description,
                            'source': 'google_search'
                        })
                        
                except Exception as e:
                    print(f"Error extracting result {i}: {e}")
                    continue
            
            return results
            
        except Exception as e:
            print(f"Google search error: {e}")
            return []
    
    async def scrape_webpage_content(self, url: str) -> Dict[str, Any]:
        """Scrape content from a specific webpage"""
        try:
            await self.browser_manager.page.goto(url, timeout=10000)
            await self.browser_manager.page.wait_for_load_state('networkidle', timeout=10000)
            
            # Extract page content
            title = await self.browser_manager.page.title()
            
            # Extract main content (try different selectors)
            content_selectors = [
                'main', 'article', '[role="main"]', '.content', '.post-content',
                '.entry-content', '.article-body', '.story-body'
            ]
            
            content = ""
            for selector in content_selectors:
                try:
                    element = await self.browser_manager.page.query_selector(selector)
                    if element:
                        content = await element.inner_text()
                        if len(content) > 100:  # Found substantial content
                            break
                except:
                    continue
            
            # Fallback to body content
            if not content or len(content) < 100:
                try:
                    body = await self.browser_manager.page.query_selector('body')
                    if body:
                        content = await body.inner_text()
                except:
                    pass
            
            # Extract metadata
            meta_description = ""
            try:
                meta_desc = await self.browser_manager.page.query_selector('meta[name="description"]')
                if meta_desc:
                    meta_description = await meta_desc.get_attribute('content')
            except:
                pass
            
            return {
                'url': url,
                'title': title,
                'content': content[:2000] if content else "",  # Limit content length
                'meta_description': meta_description,
                'source': 'web_scrape'
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {'url': url, 'error': str(e), 'source': 'web_scrape'}
    
    async def extract_person_info_from_content(self, content: str, person_name: str) -> Dict[str, Any]:
        """Extract person-specific information from web content"""
        info = {
            'mentions': [],
            'achievements': [],
            'skills_mentioned': [],
            'companies_mentioned': [],
            'education_mentioned': []
        }
        
        # Simple text analysis for person-related information
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
                
            # Look for achievement keywords
            achievement_keywords = ['award', 'won', 'achieved', 'recognized', 'honored', 'published', 'founded']
            if any(keyword in line.lower() for keyword in achievement_keywords):
                info['achievements'].append(line)
            
            # Look for skills
            skill_keywords = ['skilled in', 'expert in', 'proficient in', 'experience with', 'knowledge of']
            if any(keyword in line.lower() for keyword in skill_keywords):
                info['skills_mentioned'].append(line)
            
            # Look for company mentions
            if any(word in line for word in ['Inc', 'Corp', 'Company', 'LLC', 'Ltd']):
                info['companies_mentioned'].append(line)
            
            # Look for education mentions
            education_keywords = ['university', 'college', 'degree', 'graduated', 'studied']
            if any(keyword in line.lower() for keyword in education_keywords):
                info['education_mentioned'].append(line)
        
        return info
    
    async def get_comprehensive_profile(self, linkedin_url: str) -> Dict[str, Any]:
        """Get comprehensive profile combining LinkedIn and web data"""
        print(f"🔍 Starting comprehensive analysis for: {linkedin_url}")
        
        # Load LinkedIn session
        try:
            await self.browser_manager.load_session("linkedin_session.json")
            print("✓ LinkedIn session loaded")
        except Exception as e:
            print(f"❌ Failed to load LinkedIn session: {e}")
            return None
        
        # Step 1: Scrape LinkedIn profile
        print("📋 Step 1: Scraping LinkedIn profile...")
        scraper = PersonScraper(self.browser_manager.page)
        
        try:
            linkedin_person = await scraper.scrape(linkedin_url)
            linkedin_data = linkedin_person.model_dump()
            person_name = linkedin_person.name
            print(f"✓ LinkedIn data collected for {person_name}")
        except Exception as e:
            print(f"❌ LinkedIn scraping failed: {e}")
            return None
        
        # Step 2: Google search
        print("🔍 Step 2: Searching Google for additional information...")
        search_queries = [
            f'"{person_name}"',
            f'"{person_name}" professional',
            f'"{person_name}" achievements',
            f'"{person_name}" career'
        ]
        
        all_search_results = []
        for query in search_queries:
            results = await self.search_google(query, num_results=5)
            all_search_results.extend(results)
            await asyncio.sleep(1)  # Be respectful to Google
        
        # Remove duplicates
        seen_urls = set()
        unique_results = []
        for result in all_search_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        print(f"✓ Found {len(unique_results)} unique search results")
        
        # Step 3: Scrape top web pages
        print("📄 Step 3: Extracting detailed content from top sources...")
        web_content = []
        
        for i, result in enumerate(unique_results[:8]):  # Limit to top 8 results
            print(f"  Scraping: {result['title'][:50]}...")
            content = await self.scrape_webpage_content(result['url'])
            if 'error' not in content:
                person_info = await self.extract_person_info_from_content(content['content'], person_name)
                content.update(person_info)
            web_content.append(content)
            await asyncio.sleep(2)  # Be respectful to websites
        
        # Step 4: Compile comprehensive profile
        print("📊 Step 4: Compiling comprehensive profile...")
        
        comprehensive_profile = {
            'person_name': person_name,
            'scraped_at': str(asyncio.get_event_loop().time()),
            'linkedin_data': linkedin_data,
            'google_search_results': unique_results,
            'web_content': web_content,
            'summary': {
                'total_sources': len(unique_results) + 1,  # +1 for LinkedIn
                'web_pages_scraped': len([w for w in web_content if 'error' not in w]),
                'achievements_found': sum(len(w.get('achievements', [])) for w in web_content),
                'skills_mentioned': sum(len(w.get('skills_mentioned', [])) for w in web_content),
                'companies_mentioned': sum(len(w.get('companies_mentioned', [])) for w in web_content)
            }
        }
        
        return comprehensive_profile
    
    async def save_comprehensive_profile(self, profile: Dict[str, Any]) -> str:
        """Save comprehensive profile to JSON file"""
        person_name = profile['person_name']
        filename = f"extracted/{person_name.replace(' ', '_')}_comprehensive_profile.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Comprehensive profile saved to: {filename}")
        return filename

async def main():
    """Main function"""
    print("🎯 Comprehensive Person Scraper")
    print("Combining LinkedIn + Google search + Web scraping\n")
    
    # Example usage
    profile_url = input("Enter LinkedIn profile URL (or press Enter for Kiko Chen): ").strip()
    
    if not profile_url:
        profile_url = "https://www.linkedin.com/in/kikotchen/"
    
    if "linkedin.com/in/" not in profile_url:
        print("❌ Invalid LinkedIn profile URL")
        return
    
    async with ComprehensivePersonScraper() as scraper:
        profile = await scraper.get_comprehensive_profile(profile_url)
        
        if profile:
            filename = await scraper.save_comprehensive_profile(profile)
            
            # Print summary
            summary = profile['summary']
            print(f"\n📊 EXTRACTION SUMMARY:")
            print(f"  Person: {profile['person_name']}")
            print(f"  Total Sources: {summary['total_sources']}")
            print(f"  Web Pages Scraped: {summary['web_pages_scraped']}")
            print(f"  Achievements Found: {summary['achievements_found']}")
            print(f"  Skills Mentioned: {summary['skills_mentioned']}")
            print(f"  Companies Mentioned: {summary['companies_mentioned']}")
            print(f"\n✅ Comprehensive profile saved to: {filename}")
        else:
            print("❌ Failed to create comprehensive profile")

if __name__ == "__main__":
    asyncio.run(main())
