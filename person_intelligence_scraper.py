#!/usr/bin/env python3
"""
Person Intelligence Scraper
Extracts and analyzes LinkedIn data with intelligent insights
"""
import asyncio
import json
import re
from typing import Dict, List, Any
from datetime import datetime
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

class PersonIntelligenceScraper:
    def __init__(self):
        self.browser_manager = None
        
    async def __aenter__(self):
        self.browser_manager = BrowserManager(headless=True)
        await self.browser_manager.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser_manager:
            await self.browser_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    def analyze_experience(self, experiences: List[Dict]) -> Dict[str, Any]:
        """Analyze work experience for insights"""
        if not experiences:
            return {}
        
        analysis = {
            'total_positions': len(experiences),
            'current_position': experiences[0] if experiences else None,
            'career_progression': [],
            'companies_worked': [],
            'total_experience_years': 0,
            'skills_mentioned': [],
            'industries': []
        }
        
        # Extract companies
        for exp in experiences:
            if exp.get('institution_name'):
                analysis['companies_worked'].append(exp['institution_name'])
            
            # Extract skills from descriptions
            description = exp.get('description', '')
            if description:
                # Common tech/professional skills
                skill_patterns = [
                    r'\b(Python|Java|JavaScript|C\+\+|SQL|React|Node\.js|AWS|Azure|GCP)\b',
                    r'\b(Leadership|Management|Strategy|Marketing|Sales|Finance)\b',
                    r'\b(Machine Learning|AI|Data Science|Analytics|DevOps)\b',
                    r'\b(Project Management|Agile|Scrum|Kanban)\b'
                ]
                
                for pattern in skill_patterns:
                    matches = re.findall(pattern, description, re.IGNORECASE)
                    analysis['skills_mentioned'].extend(matches)
        
        # Calculate total experience
        for exp in experiences:
            duration = exp.get('duration', '')
            if 'yr' in duration:
                years = re.search(r'(\d+)\s*yr', duration)
                if years:
                    analysis['total_experience_years'] += int(years.group(1))
        
        # Remove duplicates
        analysis['companies_worked'] = list(set(analysis['companies_worked']))
        analysis['skills_mentioned'] = list(set(analysis['skills_mentioned']))
        
        return analysis
    
    def analyze_education(self, educations: List[Dict]) -> Dict[str, Any]:
        """Analyze education for insights"""
        if not educations:
            return {}
        
        analysis = {
            'total_institutions': len(educations),
            'institutions': [],
            'degrees': [],
            'education_span': {},
            'academic_achievements': []
        }
        
        for edu in educations:
            if edu.get('institution_name'):
                analysis['institutions'].append(edu['institution_name'])
            
            if edu.get('degree'):
                analysis['degrees'].append(edu['degree'])
            
            # Look for achievements in descriptions
            description = edu.get('description', '')
            if description:
                if any(word in description.lower() for word in ['honor', 'dean', 'scholarship', 'award', 'gpa']):
                    analysis['academic_achievements'].append(description)
        
        return analysis
    
    def generate_person_summary(self, linkedin_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive person summary"""
        name = linkedin_data.get('name', 'Unknown')
        location = linkedin_data.get('location', 'Unknown')
        
        # Analyze experience
        exp_analysis = self.analyze_experience(linkedin_data.get('experiences', []))
        
        # Analyze education
        edu_analysis = self.analyze_education(linkedin_data.get('educations', []))
        
        # Generate career insights
        current_role = exp_analysis.get('current_position', {})
        career_summary = {
            'current_title': current_role.get('position_title', 'Unknown'),
            'current_company': current_role.get('institution_name', 'Unknown'),
            'years_experience': exp_analysis.get('total_experience_years', 0),
            'companies_count': len(exp_analysis.get('companies_worked', [])),
            'education_level': self.determine_education_level(edu_analysis.get('degrees', [])),
            'skills_count': len(exp_analysis.get('skills_mentioned', []))
        }
        
        # Generate insights
        insights = {
            'career_trajectory': self.analyze_career_trajectory(linkedin_data.get('experiences', [])),
            'industry_focus': self.infer_industry_focus(exp_analysis.get('companies_worked', [])),
            'skill_categories': self.categorize_skills(exp_analysis.get('skills_mentioned', [])),
            'network_indicators': {
                'has_contacts': len(linkedin_data.get('contacts', [])) > 0,
                'has_interests': len(linkedin_data.get('interests', [])) > 0,
                'has_accomplishments': len(linkedin_data.get('accomplishments', [])) > 0
            }
        }
        
        return {
            'basic_info': {
                'name': name,
                'location': location,
                'linkedin_url': linkedin_data.get('linkedin_url', ''),
                'open_to_work': linkedin_data.get('open_to_work', False)
            },
            'career_summary': career_summary,
            'experience_analysis': exp_analysis,
            'education_analysis': edu_analysis,
            'insights': insights,
            'about_summary': linkedin_data.get('about', ''),
            'interests': linkedin_data.get('interests', []),
            'contacts_count': len(linkedin_data.get('contacts', [])),
            'accomplishments_count': len(linkedin_data.get('accomplishments', []))
        }
    
    def determine_education_level(self, degrees: List[str]) -> str:
        """Determine highest education level"""
        if not degrees:
            return 'Unknown'
        
        degree_str = ' '.join(degrees).lower()
        
        if any(word in degree_str for word in ['phd', 'doctor', 'doctorate']):
            return 'PhD/Doctorate'
        elif any(word in degree_str for word in ['master', 'm.s', 'm.a']):
            return 'Masters'
        elif any(word in degree_str for word in ['bachelor', 'b.s', 'b.a', 'undergraduate']):
            return 'Bachelors'
        elif any(word in degree_str for word in ['associate', 'diploma']):
            return 'Associate/Diploma'
        else:
            return 'Other'
    
    def analyze_career_trajectory(self, experiences: List[Dict]) -> str:
        """Analyze career progression"""
        if len(experiences) < 2:
            return 'Limited career history'
        
        # Simple trajectory analysis
        positions = [exp.get('position_title', '').lower() for exp in experiences if exp.get('position_title')]
        
        leadership_keywords = ['lead', 'manager', 'director', 'head', 'chief', 'vp', 'president']
        senior_keywords = ['senior', 'principal', 'staff', 'lead']
        
        has_leadership = any(any(keyword in pos for keyword in leadership_keywords) for pos in positions)
        has_senior = any(any(keyword in pos for keyword in senior_keywords) for pos in positions)
        
        if has_leadership:
            return 'Leadership track'
        elif has_senior:
            return 'Senior professional'
        else:
            return 'Early/mid-career professional'
    
    def infer_industry_focus(self, companies: List[str]) -> List[str]:
        """Infer industry focus from companies"""
        if not companies:
            return []
        
        company_str = ' '.join(companies).lower()
        
        industry_keywords = {
            'Technology': ['tech', 'software', 'computer', 'data', 'ai', 'cloud'],
            'Finance': ['bank', 'financial', 'investment', 'finance'],
            'Healthcare': ['health', 'medical', 'pharma', 'hospital'],
            'Education': ['university', 'school', 'education', 'academic'],
            'Consulting': ['consulting', 'advisory', 'solutions'],
            'Media': ['media', 'advertising', 'marketing', 'content']
        }
        
        industries = []
        for industry, keywords in industry_keywords.items():
            if any(keyword in company_str for keyword in keywords):
                industries.append(industry)
        
        return industries if industries else ['General']
    
    def categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into groups"""
        if not skills:
            return {}
        
        categories = {
            'Programming': ['python', 'java', 'javascript', 'c++', 'sql', 'react', 'node.js'],
            'Cloud/DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'devops'],
            'Data Science': ['machine learning', 'ai', 'data science', 'analytics', 'statistics'],
            'Business': ['leadership', 'management', 'strategy', 'marketing', 'sales', 'finance'],
            'Project Management': ['project management', 'agile', 'scrum', 'kanban']
        }
        
        categorized = {category: [] for category in categories}
        categorized['Other'] = []
        
        for skill in skills:
            skill_lower = skill.lower()
            categorized_skill = False
            
            for category, keywords in categories.items():
                if any(keyword in skill_lower for keyword in keywords):
                    categorized[category].append(skill)
                    categorized_skill = True
                    break
            
            if not categorized_skill:
                categorized['Other'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    async def get_intelligence_profile(self, linkedin_url: str) -> Dict[str, Any]:
        """Get comprehensive intelligence profile"""
        print(f"🧠 Intelligence analysis for: {linkedin_url}")
        
        # Load LinkedIn session
        try:
            await self.browser_manager.load_session("linkedin_session.json")
            print("✓ LinkedIn session loaded")
        except Exception as e:
            print(f"❌ Failed to load LinkedIn session: {e}")
            return None
        
        # Get LinkedIn data
        print("📊 Extracting LinkedIn data...")
        scraper = PersonScraper(self.browser_manager.page)
        
        try:
            linkedin_person = await scraper.scrape(linkedin_url)
            linkedin_data = linkedin_person.model_dump()
            person_name = linkedin_person.name
            print(f"✓ Data extracted: {person_name}")
        except Exception as e:
            print(f"❌ LinkedIn scraping failed: {e}")
            return None
        
        # Generate intelligence analysis
        print("🧠 Generating intelligence insights...")
        intelligence = self.generate_person_summary(linkedin_data)
        
        # Add metadata
        intelligence['metadata'] = {
            'scraped_at': datetime.now().isoformat(),
            'source': 'linkedin_intelligence_analysis',
            'data_completeness': self.assess_data_completeness(linkedin_data)
        }
        
        return intelligence
    
    def assess_data_completeness(self, linkedin_data: Dict) -> Dict[str, Any]:
        """Assess completeness of scraped data"""
        completeness = {
            'has_about': bool(linkedin_data.get('about')),
            'has_experiences': len(linkedin_data.get('experiences', [])) > 0,
            'has_education': len(linkedin_data.get('educations', [])) > 0,
            'has_interests': len(linkedin_data.get('interests', [])) > 0,
            'has_contacts': len(linkedin_data.get('contacts', [])) > 0,
            'has_accomplishments': len(linkedin_data.get('accomplishments', [])) > 0,
            'experience_count': len(linkedin_data.get('experiences', [])),
            'education_count': len(linkedin_data.get('educations', [])),
            'completeness_score': 0
        }
        
        # Calculate completeness score
        fields = ['has_about', 'has_experiences', 'has_education', 'has_interests', 'has_contacts', 'has_accomplishments']
        completeness['completeness_score'] = sum(completeness[field] for field in fields) / len(fields) * 100
        
        return completeness
    
    async def save_intelligence_profile(self, profile: Dict[str, Any]) -> str:
        """Save intelligence profile to JSON file"""
        person_name = profile['basic_info']['name']
        filename = f"extracted/{person_name.replace(' ', '_')}_intelligence_profile.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Intelligence profile saved to: {filename}")
        return filename

async def main():
    """Main function"""
    print("🧠 Person Intelligence Scraper")
    print("Advanced analysis of LinkedIn profiles\n")
    
    # Get input
    profile_url = input("Enter LinkedIn profile URL (or press Enter for Kiko Chen): ").strip()
    
    if not profile_url:
        profile_url = "https://www.linkedin.com/in/kikotchen/"
    
    if "linkedin.com/in/" not in profile_url:
        print("❌ Invalid LinkedIn profile URL")
        return
    
    async with PersonIntelligenceScraper() as scraper:
        profile = await scraper.get_intelligence_profile(profile_url)
        
        if profile:
            filename = await scraper.save_intelligence_profile(profile)
            
            # Print intelligence summary
            basic = profile['basic_info']
            career = profile['career_summary']
            insights = profile['insights']
            completeness = profile['metadata']['data_completeness']
            
            print(f"\n🧠 INTELLIGENCE SUMMARY:")
            print(f"  Name: {basic['name']}")
            print(f"  Location: {basic['location']}")
            print(f"  Current Role: {career['current_title']} at {career['current_company']}")
            print(f"  Experience: {career['years_experience']} years, {career['companies_count']} companies")
            print(f"  Education: {career['education_level']}")
            print(f"  Career Trajectory: {insights['career_trajectory']}")
            print(f"  Industry Focus: {', '.join(insights['industry_focus'])}")
            print(f"  Data Completeness: {completeness['completeness_score']:.1f}%")
            
            if insights['skill_categories']:
                print(f"  Skill Categories: {', '.join(insights['skill_categories'].keys())}")
            
            print(f"\n✅ Intelligence profile saved to: {filename}")
        else:
            print("❌ Failed to create intelligence profile")

if __name__ == "__main__":
    asyncio.run(main())
