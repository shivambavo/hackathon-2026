#!/usr/bin/env python3
"""
LinkedIn Post Analyzer
Analyzes profile for post potential and provides guidance
"""
import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

class PostAnalyzer:
    def __init__(self):
        self.browser_manager = None
        
    async def __aenter__(self):
        self.browser_manager = BrowserManager(headless=True)
        await self.browser_manager.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser_manager:
            await self.browser_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    async def analyze_post_potential(self, profile_url: str) -> Dict[str, Any]:
        """Analyze profile for post potential and provide guidance"""
        print(f"📊 Analyzing post potential for: {profile_url}")
        
        # Load LinkedIn session
        try:
            await self.browser_manager.load_session("linkedin_session.json")
            print("✓ LinkedIn session loaded")
        except Exception as e:
            print(f"❌ Failed to load LinkedIn session: {e}")
            return None
        
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
        
        # Analyze profile for post indicators
        print("🔍 Analyzing profile for post indicators...")
        post_analysis = self.analyze_profile_for_posts(profile_data)
        
        # Generate recommendations
        recommendations = self.generate_post_recommendations(profile_data, post_analysis)
        
        # Compile analysis
        analysis_report = {
            'person_name': person_name,
            'scraped_at': datetime.now().isoformat(),
            'profile_data': profile_data,
            'post_analysis': post_analysis,
            'recommendations': recommendations,
            'manual_checklist': self.generate_manual_checklist()
        }
        
        return analysis_report
    
    def analyze_profile_for_posts(self, profile_data: Dict) -> Dict[str, Any]:
        """Analyze profile data for post likelihood indicators"""
        analysis = {
            'profile_completeness': 0,
            'has_about_section': bool(profile_data.get('about')),
            'has_experiences': len(profile_data.get('experiences', [])) > 0,
            'has_education': len(profile_data.get('educations', [])) > 0,
            'has_interests': len(profile_data.get('interests', [])) > 0,
            'has_accomplishments': len(profile_data.get('accomplishments', [])) > 0,
            'has_contacts': len(profile_data.get('contacts', [])) > 0,
            'experience_count': len(profile_data.get('experiences', [])),
            'education_count': len(profile_data.get('educations', [])),
            'post_likelihood': 'Unknown'
        }
        
        # Calculate completeness
        fields = ['has_about_section', 'has_experiences', 'has_education', 'has_interests', 'has_accomplishments']
        analysis['profile_completeness'] = sum(analysis[field] for field in fields) / len(fields) * 100
        
        # Determine post likelihood
        if analysis['profile_completeness'] >= 80:
            analysis['post_likelihood'] = 'High'
        elif analysis['profile_completeness'] >= 60:
            analysis['post_likelihood'] = 'Medium'
        elif analysis['profile_completeness'] >= 40:
            analysis['post_likelihood'] = 'Low'
        else:
            analysis['post_likelihood'] = 'Very Low'
        
        return analysis
    
    def generate_post_recommendations(self, profile_data: Dict, analysis: Dict) -> List[str]:
        """Generate recommendations based on profile analysis"""
        recommendations = []
        
        # Based on profile completeness
        if analysis['profile_completeness'] >= 80:
            recommendations.append("✅ Profile is very complete - likely has public posts")
        elif analysis['profile_completeness'] >= 60:
            recommendations.append("⚠️  Profile is moderately complete - may have some posts")
        else:
            recommendations.append("❌ Profile is incomplete - unlikely to have many posts")
        
        # Based on specific sections
        if analysis['has_about_section']:
            recommendations.append("✅ About section present - indicates active profile management")
        else:
            recommendations.append("❌ No about section - profile may be inactive")
        
        if analysis['has_experiences']:
            exp_count = analysis['experience_count']
            if exp_count >= 3:
                recommendations.append(f"✅ {exp_count} work experiences - suggests active professional")
            else:
                recommendations.append(f"⚠️  Only {exp_count} work experience(s) - may be early career")
        
        if analysis['has_interests']:
            recommendations.append("✅ Has interests listed - indicates engaged user")
        else:
            recommendations.append("❌ No interests listed - may be private profile")
        
        if analysis['has_accomplishments']:
            recommendations.append("✅ Has accomplishments - likely active LinkedIn user")
        else:
            recommendations.append("❌ No accomplishments - may not be active")
        
        # Privacy indicators
        if not analysis['has_contacts']:
            recommendations.append("⚠️  No visible contacts - may have privacy settings")
        
        # General recommendations
        recommendations.append("💡 Manual check: Visit profile directly to see posts section")
        recommendations.append("💡 Manual check: Look for 'Posts' or 'Activity' tab")
        recommendations.append("💡 Manual check: Check if profile is public or private")
        
        return recommendations
    
    def generate_manual_checklist(self) -> List[str]:
        """Generate checklist for manual post checking"""
        return [
            "📋 MANUAL CHECKLIST:",
            "1. Visit the LinkedIn profile directly in browser",
            "2. Look for 'Posts' tab or link in profile navigation",
            "3. Look for 'Activity' section in profile",
            "4. Check if profile shows recent updates or posts",
            "5. Look for 'Articles' section if person writes articles",
            "6. Check if profile is set to private vs public",
            "7. Look for engagement metrics (likes, comments) on posts",
            "8. Check post frequency (daily, weekly, monthly)",
            "9. Note post topics and content types",
            "10. Check if posts are original content or shares"
        ]
    
    async def save_analysis_report(self, report: Dict[str, Any]) -> str:
        """Save analysis report to JSON file"""
        person_name = report['person_name']
        filename = f"extracted/{person_name.replace(' ', '_')}_post_analysis.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Post analysis saved to: {filename}")
        return filename

async def main():
    """Main function"""
    print("📊 LinkedIn Post Analyzer")
    print("Analyzes profiles for post potential and provides guidance\n")
    
    # Get input
    profile_url = input("Enter LinkedIn profile URL (or press Enter for Bill Gates): ").strip()
    
    if not profile_url:
        profile_url = "https://www.linkedin.com/in/williamhgates/"
    
    if "linkedin.com/in/" not in profile_url:
        print("❌ Invalid LinkedIn profile URL")
        return
    
    async with PostAnalyzer() as analyzer:
        report = await analyzer.analyze_post_potential(profile_url)
        
        if report:
            filename = await analyzer.save_analysis_report(report)
            
            # Print analysis
            analysis = report['post_analysis']
            profile_data = report['profile_data']
            
            print(f"\n📊 POST POTENTIAL ANALYSIS:")
            print(f"  Person: {report['person_name']}")
            print(f"  Profile Completeness: {analysis['profile_completeness']:.1f}%")
            print(f"  Post Likelihood: {analysis['post_likelihood']}")
            print(f"  Has About Section: {analysis['has_about_section']}")
            print(f"  Work Experiences: {analysis['experience_count']}")
            print(f"  Education: {analysis['education_count']}")
            print(f"  Has Interests: {analysis['has_interests']}")
            print(f"  Has Accomplishments: {analysis['has_accomplishments']}")
            print(f"  Has Contacts: {analysis['has_contacts']}")
            
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                print(f"  {rec}")
            
            print(f"\n{report['manual_checklist'][0]}")
            for item in report['manual_checklist'][1:]:
                print(f"  {item}")
            
            print(f"\n✅ Post analysis saved to: {filename}")
            
            # Additional insights
            if profile_data.get('about'):
                about_length = len(profile_data['about'])
                print(f"\n📝 ABOUT SECTION ANALYSIS:")
                print(f"  Length: {about_length} characters")
                print(f"  Content: {profile_data['about'][:100]}...")
            
            if analysis['experience_count'] > 0:
                print(f"\n💼 EXPERIENCE ANALYSIS:")
                for i, exp in enumerate(profile_data['experiences'][:3]):
                    title = exp.get('position_title', 'Unknown')
                    company = exp.get('institution_name', 'Unknown')
                    duration = exp.get('duration', 'Unknown')
                    print(f"  {i+1}. {title} at {company} ({duration})")
            
        else:
            print("❌ Failed to analyze post potential")

if __name__ == "__main__":
    asyncio.run(main())
