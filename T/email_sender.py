"""
Email Sending Module - Sends cold emails via Gmail API with SMTP fallback
"""
import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from dotenv import load_dotenv
from config import GMAIL_SCOPES, GMAIL_CREDENTIALS_FILE, GMAIL_TOKEN_FILE, SENDER_EMAIL, SENDER_NAME

load_dotenv()

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_API_AVAILABLE = True
except ImportError:
    GMAIL_API_AVAILABLE = False


class EmailSender:
    """Handles sending emails via Gmail API"""
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        if not GMAIL_API_AVAILABLE:
            print("Gmail API not available. Using SMTP fallback.")
            return
            
        creds = None
        
        # Load existing token
        if os.path.exists(GMAIL_TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_FILE, GMAIL_SCOPES)
            except Exception as e:
                print(f"Error loading token: {e}")
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                if os.path.exists(GMAIL_CREDENTIALS_FILE):
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            GMAIL_CREDENTIALS_FILE, GMAIL_SCOPES)
                        creds = flow.run_local_server(port=0)
                    except Exception as e:
                        print(f"Error during OAuth flow: {e}")
                        print(f"Warning: {GMAIL_CREDENTIALS_FILE} found but authentication failed. Using SMTP fallback.")
                        return
                else:
                    print(f"Warning: {GMAIL_CREDENTIALS_FILE} not found. Using SMTP fallback.")
                    return
            
            # Save credentials for next run
            try:
                with open(GMAIL_TOKEN_FILE, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Error saving token: {e}")
        
        self.credentials = creds
        
        # Build Gmail service
        if creds:
            try:
                self.service = build('gmail', 'v1', credentials=creds)
            except Exception as e:
                print(f"Error building Gmail service: {e}")
                self.service = None
    
    def create_email_message(self, to_email: str, subject: str, body_html: str, 
                            body_text: str = None) -> Dict:
        """Create an email message"""
        message = MIMEMultipart('alternative')
        message['to'] = to_email
        message['from'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message['subject'] = subject
        
        # Add text and HTML parts
        if body_text:
            part1 = MIMEText(body_text, 'plain')
            message.attach(part1)
        
        part2 = MIMEText(body_html, 'html')
        message.attach(part2)
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}
    
    def generate_cold_email_html(self, lead: Dict, channel_info: Dict) -> str:
        """Generate HTML email with black and pink theme"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #1a1a1a;
                    color: #ffffff;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #000000;
                    border: 2px solid #FF1493;
                    border-radius: 10px;
                    padding: 30px;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #FF1493;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .header h1 {{
                    color: #FF1493;
                    margin: 0;
                }}
                .content {{
                    line-height: 1.6;
                    color: #ffffff;
                }}
                .highlight {{
                    color: #FF69B4;
                    font-weight: bold;
                }}
                .button {{
                    display: inline-block;
                    background-color: #FF1493;
                    color: #000000;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #333333;
                    text-align: center;
                    color: #999999;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Video Editing Services</h1>
                </div>
                <div class="content">
                    <p>Hi there!</p>
                    
                    <p>I noticed your amazing <span class="highlight">{channel_info.get('platform', '').upper()}</span> channel 
                    <span class="highlight">@{channel_info.get('username', '')}</span> with 
                    <span class="highlight">{channel_info.get('subscriber_count', 0):,}</span> followers!</p>
                    
                    <p>Your content is impressive, and I can help take it to the next level with professional video editing services.</p>
                    
                    <p>I specialize in:</p>
                    <ul>
                        <li>Fast turnaround times</li>
                        <li>High-quality editing</li>
                        <li>Engaging transitions and effects</li>
                        <li>Optimized for social media platforms</li>
                    </ul>
                    
                    <p>Would you be interested in discussing how I can help elevate your content?</p>
                    
                    <div style="text-align: center;">
                        <a href="mailto:{SENDER_EMAIL}" class="button">Let's Talk</a>
                    </div>
                    
                    <p>Looking forward to hearing from you!</p>
                    
                    <p>Best regards,<br>
                    <span class="highlight">{SENDER_NAME}</span></p>
                </div>
                <div class="footer">
                    <p>This email was sent to {lead.get('email', 'you')}</p>
                    <p>If you'd like to unsubscribe, please reply with "UNSUBSCRIBE"</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def generate_cold_email_text(self, lead: Dict, channel_info: Dict) -> str:
        """Generate plain text version of email"""
        text = f"""
Hi there!

I noticed your amazing {channel_info.get('platform', '').upper()} channel @{channel_info.get('username', '')} with {channel_info.get('subscriber_count', 0):,} followers!

Your content is impressive, and I can help take it to the next level with professional video editing services.

I specialize in:
- Fast turnaround times
- High-quality editing
- Engaging transitions and effects
- Optimized for social media platforms

Would you be interested in discussing how I can help elevate your content?

Looking forward to hearing from you!

Best regards,
{SENDER_NAME}
        """
        return text
    
    def send_email(self, to_email: str, subject: str, body_html: str, 
                   body_text: str = None) -> bool:
        """Send an email via Gmail API with SMTP fallback"""
        # Try Gmail API first
        if self.service:
            try:
                message = self.create_email_message(to_email, subject, body_html, body_text)
                sent_message = self.service.users().messages().send(
                    userId='me', body=message).execute()
                print(f"Email sent successfully to {to_email} via Gmail API. Message ID: {sent_message['id']}")
                return True
            except Exception as e:
                print(f"Gmail API error: {e}. Trying SMTP fallback...")
        
        # Fallback to SMTP
        return self._send_email_smtp(to_email, subject, body_html, body_text)
    
    def _send_email_smtp(self, to_email: str, subject: str, body_html: str, 
                         body_text: str = None) -> bool:
        """Send email using SMTP as fallback"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = SENDER_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if body_text:
                part1 = MIMEText(body_text, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(body_html, 'html')
            msg.attach(part2)
            
            # Send via SMTP
            # Note: You'll need to set up App Password for Gmail
            # Go to: https://myaccount.google.com/apppasswords
            app_password = os.getenv('GMAIL_APP_PASSWORD', '')
            if not app_password:
                print("GMAIL_APP_PASSWORD not set in .env file. Cannot send via SMTP.")
                return False
            
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login(SENDER_EMAIL, app_password)
            smtp_server.send_message(msg)
            smtp_server.quit()
            
            print(f"Email sent successfully to {to_email} via SMTP")
            return True
        except Exception as e:
            print(f"Error sending email via SMTP to {to_email}: {e}")
            print("Note: For SMTP, you need to set GMAIL_APP_PASSWORD in .env file")
            return False
    
    def send_cold_email(self, lead: Dict, channel_info: Dict) -> bool:
        """Send a cold email to a lead"""
        email = lead.get('email')
        if not email:
            print(f"No email found for lead {lead.get('username', '')}")
            return False
        
        subject = f"Professional Video Editing Services for Your {channel_info.get('platform', '').upper()} Channel"
        body_html = self.generate_cold_email_html(lead, channel_info)
        body_text = self.generate_cold_email_text(lead, channel_info)
        
        return self.send_email(email, subject, body_html, body_text)
    
    def send_batch_emails(self, leads: List[Dict], channel_info_map: Dict) -> Dict:
        """Send emails to multiple leads"""
        results = {
            'sent': 0,
            'failed': 0,
            'details': []
        }
        
        for lead in leads:
            channel_id = lead.get('channel_id', '')
            channel_info = channel_info_map.get(channel_id, {})
            
            if self.send_cold_email(lead, channel_info):
                results['sent'] += 1
                results['details'].append({
                    'email': lead.get('email'),
                    'status': 'sent'
                })
            else:
                results['failed'] += 1
                results['details'].append({
                    'email': lead.get('email'),
                    'status': 'failed'
                })
        
        return results
