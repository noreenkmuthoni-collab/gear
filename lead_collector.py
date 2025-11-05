"""
Lead Collection Module - Extracts emails and contact information
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from email_validator import validate_email, EmailNotValidError


class LeadCollector:
    """Collects leads and email addresses from channels"""
    
    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    def collect_lead_from_channel(self, channel_info: Dict) -> Dict:
        """
        Collect lead information from a channel
        Returns lead data with email if found
        """
        lead = {
            'channel_id': channel_info.get('channel_id', ''),
            'platform': channel_info.get('platform', ''),
            'username': channel_info.get('username', ''),
            'email': None,
            'contact_info': {},
            'url': channel_info.get('url', ''),
            'subscriber_count': channel_info.get('subscriber_count', 0),
            'description': channel_info.get('description', '')
        }
        
        # Try to extract email from channel description
        description = channel_info.get('description', '')
        emails = self._extract_emails_from_text(description)
        if emails:
            lead['email'] = emails[0]
        
        # Try to get email / contact links from channel page
        channel_url = channel_info.get('url', '')
        if channel_url:
            contact_data = self._extract_contacts_from_url(channel_url)
            page_emails = contact_data.get('emails', [])
            if page_emails and not lead['email']:
                lead['email'] = page_emails[0]
            # Prefer discord/contact links if present
            contact_links = contact_data.get('links', [])
            if contact_links:
                lead['contact_info']['links'] = contact_links
        
        # Try to extract email from About page
        if channel_info.get('platform') == 'youtube':
            about_emails = self._get_youtube_about_email(channel_info)
            if about_emails and not lead['email']:
                lead['email'] = about_emails
        
        return lead
    
    def _extract_emails_from_text(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        emails = []
        matches = self.email_pattern.findall(text)
        
        for email in matches:
            try:
                # Validate email
                validation = validate_email(email)
                emails.append(validation.email)
            except EmailNotValidError:
                continue
        
        return emails
    
    def _extract_emails_from_url(self, url: str) -> List[str]:
        """Extract email addresses from a webpage"""
        emails = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                emails = self._extract_emails_from_text(text)
        except Exception as e:
            print(f"Error extracting emails from URL {url}: {e}")
        
        return emails

    def _extract_contacts_from_url(self, url: str) -> Dict[str, List[str]]:
        """Extract emails and likely contact links (discord/contact/business) from a webpage."""
        emails: List[str] = []
        links: List[str] = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                emails = self._extract_emails_from_text(text)
                for a in soup.find_all('a'):
                    href = (a.get('href') or '').strip()
                    label = (a.get_text() or '').strip().lower()
                    if not href:
                        continue
                    # Normalize
                    href_lower = href.lower()
                    candidates = [href_lower, label]
                    # Heuristics: discord, contact, business, email
                    if any(s in c for c in candidates for s in ['discord.gg', 'discord.com/invite']):
                        links.append(href)
                    elif any(s in c for c in candidates for s in ['contact', 'business', 'hire me', 'work with me', 'email']):
                        links.append(href)
        except Exception as e:
            print(f"Error extracting contacts from URL {url}: {e}")
        return {'emails': emails, 'links': list(dict.fromkeys(links))}
    
    def _get_youtube_about_email(self, channel_info: Dict) -> Optional[str]:
        """Get email from YouTube channel's About page"""
        try:
            channel_id = channel_info.get('channel_id', '')
            if not channel_id:
                return None
            
            # YouTube About page URL
            about_url = f"https://www.youtube.com/channel/{channel_id}/about"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(about_url, headers=headers, timeout=10)
            if response.status_code == 200:
                emails = self._extract_emails_from_text(response.text)
                if emails:
                    return emails[0]
        except Exception as e:
            print(f"Error getting YouTube about email: {e}")
        
        return None
    
    def generate_contact_email(self, channel_info: Dict) -> Optional[str]:
        """
        Generate a potential contact email based on channel username
        Common patterns: business@username.com, contact@username.com, etc.
        """
        username = channel_info.get('username', '').lower()
        if not username:
            return None
        
        # Common email patterns to try
        patterns = [
            f"contact@{username}.com",
            f"info@{username}.com",
            f"business@{username}.com",
            f"{username}@gmail.com",
            f"hello@{username}.com"
        ]
        
        # Return first pattern (in production, you'd verify these)
        return patterns[0] if patterns else None
    
    def collect_leads_batch(self, channels: List[Dict]) -> List[Dict]:
        """Collect leads from multiple channels"""
        leads = []
        for channel in channels:
            lead = self.collect_lead_from_channel(channel)
            leads.append(lead)
        return leads
    
    def enrich_lead(self, lead: Dict) -> Dict:
        """Enrich lead with additional information"""
        # If no email found, try to generate one
        if not lead.get('email'):
            generated_email = self.generate_contact_email({
                'username': lead.get('username', '')
            })
            lead['email'] = generated_email
            lead['email_source'] = 'generated'
        else:
            lead['email_source'] = 'extracted'
        
        return lead
