#!/usr/bin/env python3
"""
Personality & Interests Scraper - Local Version
Saves JSON files in the current directory
"""
import asyncio
import json
import re
from typing import Dict, List, Any
from datetime import datetime
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

class PersonalityScraper:
    def __init__(self, save_directory="."):
        self.browser_manager = None
        self.save_directory = save_directory
        
        # Personality indicators keywords
        self.personality_keywords = {
            'analytical': ['analysis', 'data', 'research', 'statistics', 'metrics', 'insights'],
            'creative': ['design', 'creative', 'art', 'innovation', 'imagination', 'artistic'],
            'leadership': ['lead', 'manage', 'team', 'mentor', 'guide', 'director', 'supervise'],
            'technical': ['code', 'programming', 'development', 'engineering', 'technical', 'system'],
            'social': ['community', 'network', 'collaborate', 'connect', 'relationship', 'teamwork'],
            'entrepreneurial': ['startup', 'founder', 'entrepreneur', 'business', 'venture', 'initiative'],
            'academic': ['research', 'study', 'academic', 'university', 'education', 'learning'],
            'strategic': ['strategy', 'planning', 'vision', 'roadmap', 'goals', 'objectives']
        }
        
        # Interest categories
        self.interest_categories = {
            'technology': ['software', 'ai', 'machine learning', 'cloud', 'programming', 'tech'],
            'sports': ['sport', 'fitness', 'gym', 'running', 'swimming', 'basketball', 'soccer'],
            'arts': ['art', 'music', 'painting', 'photography', 'design', 'creative'],
            'travel': ['travel', 'explore', 'adventure', 'culture', 'international', 'global'],
            'reading': ['book', 'read', 'author', 'literature', 'novel', 'writing'],
            'food': ['food', 'cooking', 'culinary', 'restaurant', 'chef', 'recipe'],
            'gaming': ['game', 'gaming', 'esports', 'play', 'gamer', 'console'],
            'nature': ['nature', 'outdoor', 'hiking', 'environment', 'wildlife', 'sustainability'],
            'business': ['business', 'startup', 'entrepreneurship', 'investment', 'finance'],
            'education': ['learning', 'education', 'teaching', 'knowledge', 'study', 'academic']
        }
        
        # Hobby indicators
        self.hobby_indicators = {
            'photography': ['photo', 'camera', 'photography', 'capture', 'shoot'],
            'writing': ['write', 'blog', 'author', 'content', 'article', 'story'],
            'music': ['music', 'instrument', 'play', 'sing', 'compose', 'band'],
            'fitness': ['fitness', 'workout', 'gym', 'exercise', 'training', 'health'],
            'gaming': ['gaming', 'games', 'play', 'esports', 'gamer'],
            'cooking': ['cook', 'cooking', 'food', 'culinary', 'recipe', 'bake'],
            'reading': ['read', 'books', 'literature', 'novel', 'author'],
            'traveling': ['travel', 'trip', 'journey', 'explore', 'adventure'],
            'gardening': ['garden', 'plants', 'nature', 'outdoor', 'landscape'],
            'volunteering': ['volunteer', 'charity', 'community', 'help', 'cause']
        }
        
    async def __aenter__(self):
        self.browser_manager = BrowserManager(headless=True)
        await self.browser_manager.__aenter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser_manager:
            await self.browser_manager.__aexit__(exc_type, exc_val, exc_tb)
    
    async def extract_personality_profile(self, profile_url: str) -> Dict[str, Any]:
        """Extract comprehensive personality and interests profile"""
        print(f"🧠 Extracting personality profile: {profile_url}")
        
        # Load LinkedIn session
        try:
            await self.browser_manager.load_session("linkedin_session.json")
            print("✓ LinkedIn session loaded")
        except Exception as e:
            print(f"❌ Failed to load LinkedIn session: {e}")
            return None
        
        # Get basic profile data
        print("👤 Extracting LinkedIn profile...")
        scraper = PersonScraper(self.browser_manager.page)
        
        try:
            linkedin_person = await scraper.scrape(profile_url)
            profile_data = linkedin_person.model_dump()
            person_name = profile_data.get('name', 'Unknown')
            print(f"✓ Profile data: {person_name}")
        except Exception as e:
            print(f"❌ Profile scraping failed: {e}")
            return None
        
        # Extract personality traits
        print("🎭 Analyzing personality traits...")
        personality_analysis = self.analyze_personality_traits(profile_data)
        
        # Extract interests
        print("❤️ Extracting interests...")
        interests_analysis = self.extract_interests(profile_data)
        
        # Extract hobbies
        print("🎨 Identifying hobbies...")
        hobbies_analysis = self.identify_hobbies(profile_data)
        
        # Analyze communication style
        print("💬 Analyzing communication style...")
        communication_analysis = self.analyze_communication_style(profile_data)
        
        # Extract values and beliefs
        print("🌍 Extracting values and beliefs...")
        values_analysis = self.extract_values_beliefs(profile_data)
        
        # Predict social preferences
        print("👥 Predicting social preferences...")
        social_analysis = self.predict_social_preferences(profile_data)
        
        # Compile comprehensive personality profile
        personality_profile = {
            'person_name': person_name,
            'scraped_at': datetime.now().isoformat(),
            'profile_data': profile_data,
            'personality_traits': personality_analysis,
            'interests': interests_analysis,
            'hobbies': hobbies_analysis,
            'communication_style': communication_analysis,
            'values_beliefs': values_analysis,
            'social_preferences': social_analysis,
            'personality_summary': self.generate_personality_summary(
                personality_analysis, interests_analysis, hobbies_analysis
            )
        }
        
        return personality_profile
    
    def analyze_personality_traits(self, profile_data: Dict) -> Dict[str, Any]:
        """Analyze personality traits from profile data"""
        traits = {
            'dominant_traits': [],
            'trait_scores': {},
            'work_style': '',
            'leadership_style': '',
            'creativity_level': '',
            'analytical_level': ''
        }
        
        # Collect all text content
        all_text = self.collect_all_text(profile_data)
        
        # Score personality traits
        trait_scores = {}
        for trait, keywords in self.personality_keywords.items():
            score = 0
            for keyword in keywords:
                score += all_text.lower().count(keyword.lower())
            trait_scores[trait] = score
        
        # Sort traits by score
        sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Determine dominant traits (top 3 with scores > 0)
        dominant_traits = [trait for trait, score in sorted_traits[:3] if score > 0]
        traits['dominant_traits'] = dominant_traits
        traits['trait_scores'] = dict(sorted_traits)
        
        # Determine work style
        if trait_scores.get('leadership', 0) > trait_scores.get('analytical', 0):
            traits['work_style'] = 'Leadership-oriented'
        elif trait_scores.get('analytical', 0) > trait_scores.get('creative', 0):
            traits['work_style'] = 'Analytical'
        elif trait_scores.get('creative', 0) > 0:
            traits['work_style'] = 'Creative'
        else:
            traits['work_style'] = 'Balanced'
        
        # Determine leadership style
        if trait_scores.get('leadership', 0) > 2:
            traits['leadership_style'] = 'Strong Leader'
        elif trait_scores.get('leadership', 0) > 0:
            traits['leadership_style'] = 'Emerging Leader'
        else:
            traits['leadership_style'] = 'Individual Contributor'
        
        # Determine creativity level
        if trait_scores.get('creative', 0) > 2:
            traits['creativity_level'] = 'Highly Creative'
        elif trait_scores.get('creative', 0) > 0:
            traits['creativity_level'] = 'Creative'
        else:
            traits['creativity_level'] = 'Analytical/Structured'
        
        # Determine analytical level
        if trait_scores.get('analytical', 0) > 2:
            traits['analytical_level'] = 'Highly Analytical'
        elif trait_scores.get('analytical', 0) > 0:
            traits['analytical_level'] = 'Analytical'
        else:
            traits['analytical_level'] = 'Intuitive/Creative'
        
        return traits
    
    def extract_interests(self, profile_data: Dict) -> Dict[str, Any]:
        """Extract interests from profile data"""
        interests = {
            'primary_interests': [],
            'interest_categories': {},
            'passion_indicators': [],
            'learning_interests': []
        }
        
        all_text = self.collect_all_text(profile_data)
        
        # Score interest categories
        category_scores = {}
        for category, keywords in self.interest_categories.items():
            score = 0
            for keyword in keywords:
                score += all_text.lower().count(keyword.lower())
            if score > 0:
                category_scores[category] = score
        
        interests['interest_categories'] = category_scores
        
        # Determine primary interests (top categories)
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        interests['primary_interests'] = [cat for cat, score in sorted_categories[:3] if score > 0]
        
        # Look for passion indicators
        passion_words = ['passionate', 'love', 'enjoy', 'excited', 'dedicated', 'committed']
        for word in passion_words:
            if word in all_text.lower():
                interests['passion_indicators'].append(word)
        
        # Look for learning interests
        learning_words = ['learn', 'study', 'research', 'explore', 'discover', 'curious']
        for word in learning_words:
            if word in all_text.lower():
                interests['learning_interests'].append(word)
        
        return interests
    
    def identify_hobbies(self, profile_data: Dict) -> Dict[str, Any]:
        """Identify hobbies from profile data"""
        hobbies = {
            'detected_hobbies': [],
            'hobby_categories': {},
            'recreation_activities': [],
            'creative_pursuits': []
        }
        
        all_text = self.collect_all_text(profile_data)
        
        # Score hobby categories
        hobby_scores = {}
        for hobby, keywords in self.hobby_indicators.items():
            score = 0
            for keyword in keywords:
                score += all_text.lower().count(keyword.lower())
            if score > 0:
                hobby_scores[hobby] = score
        
        hobbies['hobby_categories'] = hobby_scores
        
        # Determine detected hobbies
        detected = [hobby for hobby, score in hobby_scores.items() if score > 0]
        hobbies['detected_hobbies'] = detected
        
        # Categorize hobbies
        creative_hobbies = ['photography', 'writing', 'music', 'art']
        recreation_hobbies = ['gaming', 'fitness', 'traveling', 'sports']
        
        hobbies['creative_pursuits'] = [h for h in detected if h in creative_hobbies]
        hobbies['recreation_activities'] = [h for h in detected if h in recreation_hobbies]
        
        return hobbies
    
    def analyze_communication_style(self, profile_data: Dict) -> Dict[str, Any]:
        """Analyze communication style from profile data"""
        communication = {
            'style': '',
            'formality_level': '',
            'detail_orientation': '',
            'emotional_tone': '',
            'professional_vs_personal': ''
        }
        
        all_text = self.collect_all_text(profile_data)
        
        # Analyze formality
        formal_words = ['professional', 'expert', 'specialist', 'experienced', 'skilled']
        informal_words = ['love', 'passion', 'enjoy', 'fun', 'excited']
        
        formal_score = sum(all_text.lower().count(word) for word in formal_words)
        informal_score = sum(all_text.lower().count(word) for word in informal_words)
        
        if formal_score > informal_score:
            communication['formality_level'] = 'Formal'
        elif informal_score > formal_score:
            communication['formality_level'] = 'Informal'
        else:
            communication['formality_level'] = 'Balanced'
        
        # Analyze detail orientation
        if len(all_text) > 500:
            communication['detail_orientation'] = 'Detailed'
        elif len(all_text) > 200:
            communication['detail_orientation'] = 'Moderate'
        else:
            communication['detail_orientation'] = 'Concise'
        
        # Analyze emotional tone
        emotional_words = ['passionate', 'excited', 'love', 'enthusiastic', 'inspired']
        neutral_words = ['professional', 'experienced', 'skilled', 'expert']
        
        emotional_score = sum(all_text.lower().count(word) for word in emotional_words)
        neutral_score = sum(all_text.lower().count(word) for word in neutral_words)
        
        if emotional_score > neutral_score:
            communication['emotional_tone'] = 'Expressive'
        elif neutral_score > emotional_score:
            communication['emotional_tone'] = 'Professional'
        else:
            communication['emotional_tone'] = 'Balanced'
        
        # Determine overall style
        if communication['formality_level'] == 'Formal' and communication['emotional_tone'] == 'Professional':
            communication['style'] = 'Corporate Professional'
        elif communication['formality_level'] == 'Informal' and communication['emotional_tone'] == 'Expressive':
            communication['style'] = 'Casual Expressive'
        else:
            communication['style'] = 'Balanced Professional'
        
        return communication
    
    def extract_values_beliefs(self, profile_data: Dict) -> Dict[str, Any]:
        """Extract values and beliefs from profile data"""
        values = {
            'core_values': [],
            'work_values': [],
            'personal_values': [],
            'social_values': []
        }
        
        all_text = self.collect_all_text(profile_data)
        
        # Core values indicators
        value_indicators = {
            'innovation': ['innovation', 'create', 'innovate', 'new', 'breakthrough'],
            'integrity': ['integrity', 'honest', 'ethical', 'transparent', 'authentic'],
            'growth': ['growth', 'learn', 'develop', 'improve', 'progress'],
            'collaboration': ['collaborate', 'teamwork', 'partnership', 'together'],
            'excellence': ['excellence', 'quality', 'best', 'outstanding', 'premium'],
            'social_impact': ['impact', 'community', 'social', 'help', 'make difference'],
            'leadership': ['lead', 'guide', 'mentor', 'inspire', 'vision'],
            'creativity': ['creative', 'innovate', 'design', 'artistic', 'imagination']
        }
        
        for value, keywords in value_indicators.items():
            score = sum(all_text.lower().count(keyword) for keyword in keywords)
            if score > 0:
                values['core_values'].append(value)
        
        # Categorize values
        work_related = ['innovation', 'excellence', 'leadership', 'growth']
        personal_related = ['integrity', 'creativity']
        social_related = ['collaboration', 'social_impact']
        
        values['work_values'] = [v for v in values['core_values'] if v in work_related]
        values['personal_values'] = [v for v in values['core_values'] if v in personal_related]
        values['social_values'] = [v for v in values['core_values'] if v in social_related]
        
        return values
    
    def predict_social_preferences(self, profile_data: Dict) -> Dict[str, Any]:
        """Predict social preferences from profile data"""
        social = {
            'social_style': '',
            'team_preference': '',
            'networking_style': '',
            'communication_preference': '',
            'group_size_preference': ''
        }
        
        all_text = self.collect_all_text(profile_data)
        
        # Analyze social indicators
        team_words = ['team', 'collaborate', 'together', 'group', 'partnership']
        individual_words = ['individual', 'solo', 'independent', 'autonomous']
        
        team_score = sum(all_text.lower().count(word) for word in team_words)
        individual_score = sum(all_text.lower().count(word) for word in individual_words)
        
        if team_score > individual_score:
            social['team_preference'] = 'Team-oriented'
            social['group_size_preference'] = 'Large Groups'
        elif individual_score > team_score:
            social['team_preference'] = 'Individual contributor'
            social['group_size_preference'] = 'Small Groups/Solo'
        else:
            social['team_preference'] = 'Flexible'
            social['group_size_preference'] = 'Variable'
        
        # Determine social style
        if social['team_preference'] == 'Team-oriented':
            social['social_style'] = 'Collaborative'
            social['networking_style'] = 'Active Networker'
        else:
            social['social_style'] = 'Independent'
            social['networking_style'] = 'Selective Networker'
        
        # Communication preference
        if len(all_text) > 300:
            social['communication_preference'] = 'Detailed Communicator'
        else:
            social['communication_preference'] = 'Concise Communicator'
        
        return social
    
    def collect_all_text(self, profile_data: Dict) -> str:
        """Collect all text content from profile data"""
        text_parts = []
        
        # Add about section
        if profile_data.get('about'):
            text_parts.append(profile_data['about'])
        
        # Add experience descriptions
        for exp in profile_data.get('experiences', []):
            if exp.get('description'):
                text_parts.append(exp['description'])
            if exp.get('position_title'):
                text_parts.append(exp['position_title'])
        
        # Add education descriptions
        for edu in profile_data.get('educations', []):
            if edu.get('description'):
                text_parts.append(edu['description'])
        
        # Add interests
        if profile_data.get('interests'):
            text_parts.extend(profile_data['interests'])
        
        return ' '.join(text_parts).lower()
    
    def generate_personality_summary(self, personality: Dict, interests: Dict, hobbies: Dict) -> Dict[str, Any]:
        """Generate a comprehensive personality summary"""
        summary = {
            'overall_personality': '',
            'key_strengths': [],
            'potential_interests': [],
            'compatibility_notes': [],
            'conversation_starters': []
        }
        
        # Determine overall personality
        if personality['dominant_traits']:
            primary_trait = personality['dominant_traits'][0]
            summary['overall_personality'] = f"{primary_trait.title()} personality with {personality['work_style'].lower()} approach"
        else:
            summary['overall_personality'] = "Balanced professional personality"
        
        # Key strengths
        if 'leadership' in personality['dominant_traits']:
            summary['key_strengths'].append('Natural leadership ability')
        if 'analytical' in personality['dominant_traits']:
            summary['key_strengths'].append('Strong analytical skills')
        if 'creative' in personality['dominant_traits']:
            summary['key_strengths'].append('Creative problem-solving')
        if 'technical' in personality['dominant_traits']:
            summary['key_strengths'].append('Technical expertise')
        
        # Potential interests based on personality
        if interests['primary_interests']:
            summary['potential_interests'].extend(interests['primary_interests'])
        
        # Conversation starters
        if hobbies['detected_hobbies']:
            summary['conversation_starters'].append(f"Ask about their hobbies: {', '.join(hobbies['detected_hobbies'][:2])}")
        
        if interests['primary_interests']:
            summary['conversation_starters'].append(f"Discuss interests in {', '.join(interests['primary_interests'][:2])}")
        
        if personality['work_style']:
            summary['conversation_starters'].append(f"Talk about {personality['work_style'].lower()} work approaches")
        
        return summary
    
    async def save_personality_profile(self, profile: Dict[str, Any]) -> str:
        """Save personality profile to JSON file in specified directory"""
        person_name = profile['person_name']
        filename = f"{self.save_directory}/{person_name.replace(' ', '_')}_personality_profile.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Personality profile saved to: {filename}")
        return filename

async def main():
    """Main function"""
    print("🧠 Personality & Interests Scraper - Local Version")
    print("Saves JSON files in the current directory\n")
    
    # Get input
    profile_url = input("Enter LinkedIn profile URL (or press Enter for Kiko Chen): ").strip()
    
    if not profile_url:
        profile_url = "https://www.linkedin.com/in/kikotchen/"
    
    if "linkedin.com/in/" not in profile_url:
        print("❌ Invalid LinkedIn profile URL")
        return
    
    # Create scraper with current directory save location
    async with PersonalityScraper(save_directory=".") as scraper:
        profile = await scraper.extract_personality_profile(profile_url)
        
        if profile:
            filename = await scraper.save_personality_profile(profile)
            
            # Print personality summary
            personality = profile['personality_traits']
            interests = profile['interests']
            hobbies = profile['hobbies']
            communication = profile['communication_style']
            values = profile['values_beliefs']
            social = profile['social_preferences']
            summary = profile['personality_summary']
            
            print(f"\n🧠 PERSONALITY PROFILE:")
            print(f"  Name: {profile['person_name']}")
            print(f"  Overall Personality: {summary['overall_personality']}")
            print(f"  Work Style: {personality['work_style']}")
            print(f"  Leadership Style: {personality['leadership_style']}")
            print(f"  Creativity Level: {personality['creativity_level']}")
            print(f"  Analytical Level: {personality['analytical_level']}")
            
            print(f"\n🎭 DOMINANT TRAITS:")
            for trait in personality['dominant_traits']:
                score = personality['trait_scores'].get(trait, 0)
                print(f"  • {trait.title()} (score: {score})")
            
            print(f"\n❤️ INTERESTS:")
            if interests['primary_interests']:
                print(f"  Primary: {', '.join(interests['primary_interests'])}")
            else:
                print(f"  No strong interests detected")
            
            print(f"\n🎨 HOBBIES:")
            if hobbies['detected_hobbies']:
                print(f"  Detected: {', '.join(hobbies['detected_hobbies'])}")
            else:
                print(f"  No specific hobbies detected")
            
            print(f"\n💬 COMMUNICATION STYLE:")
            print(f"  Style: {communication['style']}")
            print(f"  Formality: {communication['formality_level']}")
            print(f"  Detail Orientation: {communication['detail_orientation']}")
            print(f"  Emotional Tone: {communication['emotional_tone']}")
            
            print(f"\n🌍 VALUES:")
            if values['core_values']:
                print(f"  Core: {', '.join(values['core_values'])}")
            else:
                print(f"  No specific values detected")
            
            print(f"\n👥 SOCIAL PREFERENCES:")
            print(f"  Social Style: {social['social_style']}")
            print(f"  Team Preference: {social['team_preference']}")
            print(f"  Networking: {social['networking_style']}")
            
            print(f"\n🎯 KEY STRENGTHS:")
            for strength in summary['key_strengths']:
                print(f"  • {strength}")
            
            print(f"\n💡 CONVERSATION STARTERS:")
            for starter in summary['conversation_starters']:
                print(f"  • {starter}")
            
            print(f"\n✅ Personality profile saved to: {filename}")
            
        else:
            print("❌ Failed to extract personality profile")

if __name__ == "__main__":
    asyncio.run(main())
