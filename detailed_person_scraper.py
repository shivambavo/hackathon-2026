#!/usr/bin/env python3
"""
Detailed LinkedIn Person Scraper
Runs in headless mode for efficient scraping
"""
import asyncio
import json
from linkedin_scraper.scrapers.person import PersonScraper
from linkedin_scraper.core.browser import BrowserManager

def print_person_details(person):
    """Print detailed person information"""
    print("\n" + "="*80)
    print(f"👤 PROFILE: {person.name}")
    print("="*80)
    
    # Basic Info
    print(f"\n📋 BASIC INFORMATION:")
    print(f"  Name: {person.name}")
    print(f"  Job Title: {person.job_title or 'N/A'}")
    print(f"  Company: {person.company or 'N/A'}")
    print(f"  Location: {person.location or 'N/A'}")
    print(f"  LinkedIn URL: {person.linkedin_url}")
    print(f"  Open to Work: {person.open_to_work}")
    
    # About Section
    if person.about:
        print(f"\n📝 ABOUT:")
        print(f"  {person.about}")
    
    # Experience
    print(f"\n💼 EXPERIENCE ({len(person.experiences)}):")
    for i, exp in enumerate(person.experiences, 1):
        print(f"  {i}. {exp.position_title}")
        print(f"     Company: {exp.institution_name}")
        print(f"     Duration: {exp.duration}")
        print(f"     Location: {exp.location}")
        if exp.description:
            desc = exp.description[:200] + "..." if len(exp.description) > 200 else exp.description
            print(f"     Description: {desc}")
        print()
    
    # Education
    print(f"\n🎓 EDUCATION ({len(person.educations)}):")
    for i, edu in enumerate(person.educations, 1):
        print(f"  {i}. {edu.degree}")
        print(f"     School: {edu.institution_name}")
        if edu.from_date and edu.to_date:
            print(f"     Duration: {edu.from_date} - {edu.to_date}")
        elif edu.from_date:
            print(f"     Started: {edu.from_date}")
        if edu.description:
            print(f"     Description: {edu.description}")
        print()
    
    # Interests
    if person.interests:
        print(f"\n❤️  INTERESTS ({len(person.interests)}):")
        interests_text = ", ".join(person.interests[:20])  # Show first 20 interests
        print(f"  {interests_text}")
        if len(person.interests) > 20:
            print(f"  ... and {len(person.interests) - 20} more interests")
    
    # Accomplishments
    if person.accomplishments:
        print(f"\n🏆 ACCOMPLISHMENTS ({len(person.accomplishments)}):")
        for acc in person.accomplishments:
            print(f"  • {acc.category}: {acc.title}")
    
    # Contacts
    if person.contacts:
        print(f"\n👥 CONTACTS ({len(person.contacts)}):")
        for i, contact in enumerate(person.contacts[:10], 1):  # Show first 10 contacts
            print(f"  {i}. {contact.name}")
            if contact.occupation:
                print(f"     {contact.occupation}")
            if contact.url:
                print(f"     {contact.url}")
        if len(person.contacts) > 10:
            print(f"  ... and {len(person.contacts) - 10} more contacts")
    
    print("="*80)

async def scrape_detailed_person(profile_url, save_to_file=False):
    """Scrape detailed person information"""
    print(f"🚀 Starting detailed scrape of: {profile_url}")
    
    # Use headless mode for efficient scraping
    async with BrowserManager(headless=True) as browser:
        # Load existing session
        try:
            await browser.load_session("linkedin_session.json")
            print("✓ Session loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            print("Please run simple_session.py first to create a session")
            return None
        
        # Initialize scraper
        scraper = PersonScraper(browser.page)
        
        try:
            # Scrape the profile
            person = await scraper.scrape(profile_url)
            
            # Display detailed information
            print_person_details(person)
            
            # Save to file if requested
            if save_to_file:
                filename = f"extracted/{person.name.replace(' ', '_')}_profile.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    # Convert to dict for JSON serialization
                    person_dict = person.model_dump() if hasattr(person, 'model_dump') else person.__dict__
                    json.dump(person_dict, f, indent=2, ensure_ascii=False, default=str)
                print(f"\n💾 Data saved to: {filename}")
            
            return person
            
        except Exception as e:
            print(f"❌ Scraping failed: {e}")
            return None

async def main():
    """Main function with example profiles"""
    # Example profiles you can scrape
    profiles = [
        "https://www.linkedin.com/in/williamhgates/",
        # Add more profiles here
        # "https://www.linkedin.com/in/satyanadella/",
        # "https://www.linkedin.com/in/elonmusk/",
    ]
    
    print("🎯 Detailed LinkedIn Person Scraper")
    print("Running in headless mode for efficiency\n")
    
    for profile_url in profiles:
        person = await scrape_detailed_person(profile_url, save_to_file=True)
        
        if person:
            print(f"\n✅ Successfully scraped {person.name}")
        else:
            print(f"\n❌ Failed to scrape {profile_url}")
        
        # Add delay between requests to be respectful
        if profile_url != profiles[-1]:  # Don't delay after last profile
            print("⏳ Waiting 3 seconds before next request...")
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())
