#!/usr/bin/env python3
"""
Flexible LinkedIn Profile Scraper
Scrape any LinkedIn profile in headless mode
"""
import asyncio
import json
import sys
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
        interests_text = ", ".join(person.interests[:20])
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
        for i, contact in enumerate(person.contacts[:10], 1):
            print(f"  {i}. {contact.name}")
            if contact.occupation:
                print(f"     {contact.occupation}")
            if contact.url:
                print(f"     {contact.url}")
        if len(person.contacts) > 10:
            print(f"  ... and {len(person.contacts) - 10} more contacts")
    
    print("="*80)

async def scrape_profile(profile_url, save_to_file=True):
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
                    person_dict = person.model_dump()
                    json.dump(person_dict, f, indent=2, ensure_ascii=False, default=str)
                print(f"\n💾 Data saved to: {filename}")
            
            return person
            
        except Exception as e:
            print(f"❌ Scraping failed: {e}")
            return None

def main():
    """Main function with command line argument or interactive input"""
    if len(sys.argv) > 1:
        # Use command line argument if provided
        profile_url = sys.argv[1]
    else:
        # Interactive mode
        print("🎯 LinkedIn Profile Scraper")
        print("Running in headless mode for efficiency\n")
        
        # Example profiles
        print("Example profiles you can scrape:")
        print("1. https://www.linkedin.com/in/williamhgates/")
        print("2. https://www.linkedin.com/in/satyanadella/")
        print("3. https://www.linkedin.com/in/elonmusk/")
        print()
        
        profile_url = input("Enter LinkedIn profile URL (or press Enter for Bill Gates): ").strip()
        
        if not profile_url:
            profile_url = "https://www.linkedin.com/in/williamhgates/"
        
        # Validate URL
        if "linkedin.com/in/" not in profile_url:
            print("❌ Invalid LinkedIn profile URL. Must contain 'linkedin.com/in/'")
            return
    
    # Run the scraper
    person = asyncio.run(scrape_profile(profile_url))
    
    if person:
        print(f"\n✅ Successfully scraped {person.name}")
    else:
        print(f"\n❌ Failed to scrape {profile_url}")

if __name__ == "__main__":
    main()
