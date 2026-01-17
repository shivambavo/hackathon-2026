#!/usr/bin/env python3
"""
Enhanced Web Scraper for Person Information
Uses multiple sources to find comprehensive information
"""
import asyncio
import json
import re
from typing import Dict, List, Any
from urllib.parse import quote, urlparse
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

class EnhancedWebScraper:
    def __init__(self):
        self.browser_manager = None
        
    async def __aenter__(self):
        self.browser_manager = BrowserManager(headless=True)
        await self.browser_manager.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser_manager:
            await self.browser_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    async def search_duckduckgo(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """Search DuckDuckGo for better privacy and results"""
        try:
            search_url = f"https://duckduckgo.com/html/?q={quote(query)}"
            await self.browser_manager.page.goto(search_url)
            await self.browser_manager.page.wait_for_load_state('networkidle')
            
            results = []
            result_elements = await self.browser_manager.page.query_selector_all('.result')
            
            for result in result_elements[:num_results]:
                try:
                    # Extract title and URL
                    title_link = await result.query_selector('a.result__a')
                    if title_link:
                        title = await title_link.inner_text()
                        url = await title_link.get_attribute('href')
                        
                        # Extract description
                        desc_element = await result.query_selector('.result__snippet')
                        description = await desc_element.inner_text() if desc_element else ""
                        
                        if title and url and url.startswith('http'):
                            results.append({
                                'title': title,
                                'url': url,
                                'description': description,
                                'source': 'duckduckgo_search'
                            })
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return []
    
    async def scrape_webpage_content(self, url: str) -> Dict[str, Any]:
        """Scrape content from a specific webpage"""
        try:
            print(f"    Visiting: {url}")
            await self.browser_manager.page.goto(url, timeout=15000)
            await self.browser_manager.page.wait_for_load_state('networkidle', timeout=10000)
            
            # Extract page information
            title = await self.browser_manager.page.title()
            
            # Get page text content
            try:
                content = await self.browser_manager.page.evaluate('''
                    () => {
                        // Remove script and style elements
                        const scripts = document.querySelectorAll('script, style, nav, footer, header');
                        scripts.forEach(el => el.remove());
                        
                        // Try to find main content
                        const mainContent = document.querySelector('main, article, .content, .post-content, .entry-content') ||
                                         document.querySelector('[role="main"]') ||
                                         document.body;
                        
                        return mainContent ? mainContent.innerText : '';
                    }
                ''')
            except:
                content = ""
            
            # Extract metadata
            meta_info = {}
            try:
                meta_info['description'] = await self.browser_manager.page.evaluate('''
                    () => {
                        const meta = document.querySelector('meta[name="description"]');
                        return meta ? meta.getAttribute('content') : '';
                    }
                ''')
                
                meta_info['keywords'] = await self.browser_manager.page.evaluate('''
                    () => {
                        const meta = document.querySelector('meta[name="keywords"]');
                        return meta ? meta.getAttribute('content') : '';
                    }
                ''')
            except:
                pass
            
            return {
                'url': url,
                'title': title,
                'content': content[:3000] if content else "",  # Limit content length
                'meta_info': meta_info,
                'content_length': len(content) if content else 0,
                'source': 'web_scrape'
            }
            
        except Exception as e:
            print(f"    Error scraping {url}: {str(e)[:100]}")
            return {'url': url, 'error': str(e), 'source': 'web_scrape'}
    
    def extract_person_insights(self, content: str, person_name: str) -> Dict[str, Any]:
        """Extract insights about the person from content"""
        insights = {
            'personal_mentions': [],
            'professional_info': [],
            'achievements': [],
            'skills_keywords': [],
            'organizations': [],
            'contact_info': [],
            'social_media': []
        }
        
        if not content:
            return insights
        
        content_lower = content.lower()
        name_lower = person_name.lower()
        
        # Split into sentences for better analysis
        sentences = re.split(r'[.!?]+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 20:
                continue
            
            # Check if person is mentioned in this sentence
            if name_lower not in sentence.lower():
                continue
            
            # Look for achievements
            achievement_words = ['award', 'won', 'achieved', 'recognized', 'honored', 'published', 'founded', 'created', 'launched']
            if any(word in sentence.lower() for word in achievement_words):
                insights['achievements'].append(sentence)
            
            # Look for professional info
            professional_words = ['work', 'job', 'career', 'position', 'role', 'company', 'team', 'lead', 'manage']
            if any(word in sentence.lower() for word in professional_words):
                insights['professional_info'].append(sentence)
            
            # Look for skills
            skill_words = ['expert', 'skilled', 'proficient', 'experience', 'knowledge', 'specialist', 'certified']
            if any(word in sentence.lower() for word in skill_words):
                insights['skills_keywords'].append(sentence)
            
            # Look for organizations
            org_words = ['university', 'college', 'inc', 'corp', 'company', 'organization', 'foundation', 'institute']
            if any(word in sentence.lower() for word in org_words):
                insights['organizations'].append(sentence)
            
            # Look for contact info
            if any(word in sentence.lower() for word in ['email', 'phone', 'contact', 'reach']):
                insights['contact_info'].append(sentence)
            
            # Look for social media
            if any(word in sentence.lower() for word in ['twitter', 'facebook', 'instagram', 'linkedin', 'youtube', 'github']):
                insights['social_media'].append(sentence)
        
        return insights
    
    async def get_enhanced_profile(self, linkedin_url: str) -> Dict[str, Any]:
        """Get enhanced profile with multiple sources"""
        print(f"🔍 Enhanced analysis for: {linkedin_url}")
        
        # Load LinkedIn session
        try:
            await self.browser_manager.load_session("linkedin_session.json")
            print("✓ LinkedIn session loaded")
        except Exception as e:
            print(f"❌ Failed to load LinkedIn session: {e}")
            return None
        
        # Step 1: Get LinkedIn data
        print("📋 Step 1: Extracting LinkedIn profile...")
        scraper = PersonScraper(self.browser_manager.page)
        
        try:
            linkedin_person = await scraper.scrape(linkedin_url)
            linkedin_data = linkedin_person.model_dump()
            person_name = linkedin_person.name
            print(f"✓ LinkedIn data: {person_name}")
        except Exception as e:
            print(f"❌ LinkedIn scraping failed: {e}")
            return None
        
        # Step 2: Multiple search queries
        print("🔍 Step 2: Searching web sources...")
        search_queries = [
            f'"{person_name}"',
            f'"{person_name}" professional profile',
            f'"{person_name}" achievements awards',
            f'"{person_name}" news articles'
        ]
        
        all_results = []
        for query in search_queries:
            print(f"  Searching: {query}")
            results = await self.search_duckduckgo(query, num_results=5)
            all_results.extend(results)
            await asyncio.sleep(1)  # Respectful delay
        
        # Remove duplicates
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        print(f"✓ Found {len(unique_results)} unique sources")
        
        # Step 3: Scrape content from top sources
        print("📄 Step 3: Extracting detailed content...")
        web_content = []
        
        for i, result in enumerate(unique_results[:10]):  # Top 10 results
            print(f"  {i+1}. {result['title'][:60]}...")
            content = await self.scrape_webpage_content(result['url'])
            
            if 'error' not in content:
                # Extract person-specific insights
                insights = self.extract_person_insights(content['content'], person_name)
                content['person_insights'] = insights
                
                # Add search result info
                content['search_title'] = result['title']
                content['search_description'] = result['description']
            
            web_content.append(content)
            await asyncio.sleep(2)  # Respectful delay
        
        # Step 4: Compile comprehensive profile
        print("📊 Step 4: Compiling enhanced profile...")
        
        # Aggregate insights
        all_achievements = []
        all_professional = []
        all_skills = []
        all_organizations = []
        
        for content in web_content:
            if 'person_insights' in content:
                insights = content['person_insights']
                all_achievements.extend(insights.get('achievements', []))
                all_professional.extend(insights.get('professional_info', []))
                all_skills.extend(insights.get('skills_keywords', []))
                all_organizations.extend(insights.get('organizations', []))
        
        enhanced_profile = {
            'person_name': person_name,
            'scraped_at': str(asyncio.get_event_loop().time()),
            'linkedin_data': linkedin_data,
            'web_search_results': unique_results,
            'scraped_content': web_content,
            'aggregated_insights': {
                'achievements': list(set(all_achievements))[:10],  # Remove duplicates, limit to 10
                'professional_info': list(set(all_professional))[:10],
                'skills_mentioned': list(set(all_skills))[:10],
                'organizations_mentioned': list(set(all_organizations))[:10]
            },
            'statistics': {
                'total_sources': len(unique_results) + 1,
                'successful_scrapes': len([w for w in web_content if 'error' not in w]),
                'total_content_length': sum(w.get('content_length', 0) for w in web_content),
                'insights_found': len(all_achievements) + len(all_professional) + len(all_skills)
            }
        }
        
        return enhanced_profile
    
    async def save_enhanced_profile(self, profile: Dict[str, Any]) -> str:
        """Save enhanced profile to JSON file"""
        person_name = profile['person_name']
        filename = f"extracted/{person_name.replace(' ', '_')}_enhanced_profile.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Enhanced profile saved to: {filename}")
        return filename

async def main():
    """Main function"""
    print("🎯 Enhanced Web Scraper")
    print("LinkedIn + DuckDuckGo + Deep web scraping\n")
    
    # Get input
    profile_url = input("Enter LinkedIn profile URL (or press Enter for Kiko Chen): ").strip()
    
    if not profile_url:
        profile_url = "https://www.linkedin.com/in/kikotchen/"
    
    if "linkedin.com/in/" not in profile_url:
        print("❌ Invalid LinkedIn profile URL")
        return
    
    async with EnhancedWebScraper() as scraper:
        profile = await scraper.get_enhanced_profile(profile_url)
        
        if profile:
            filename = await scraper.save_enhanced_profile(profile)
            
            # Print summary
            stats = profile['statistics']
            insights = profile['aggregated_insights']
            
            print(f"\n📊 ENHANCED PROFILE SUMMARY:")
            print(f"  Person: {profile['person_name']}")
            print(f"  Total Sources: {stats['total_sources']}")
            print(f"  Successful Scrapes: {stats['successful_scrapes']}")
            print(f"  Content Length: {stats['total_content_length']:,} characters")
            print(f"  Achievements Found: {len(insights['achievements'])}")
            print(f"  Professional Info: {len(insights['professional_info'])}")
            print(f"  Skills Mentioned: {len(insights['skills_mentioned'])}")
            print(f"  Organizations: {len(insights['organizations_mentioned'])}")
            print(f"\n✅ Enhanced profile saved to: {filename}")
        else:
            print("❌ Failed to create enhanced profile")

if __name__ == "__main__":
    asyncio.run(main())
