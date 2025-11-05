"""
Main Flask Application - Cold Email Automation AI
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from channel_collector import ChannelCollector
from post_analyzer import PostAnalyzer
from lead_collector import LeadCollector
from email_sender import EmailSender
from config import THEME_COLORS, SENDER_EMAIL

app = Flask(__name__)
CORS(app)

# Initialize modules
channel_collector = ChannelCollector()
post_analyzer = PostAnalyzer()
lead_collector = LeadCollector()
email_sender = EmailSender()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', colors=THEME_COLORS)

@app.route('/api/collect-channels', methods=['POST'])
def collect_channels():
    """Collect channels from platforms"""
    try:
        data = request.json
        query = data.get('query', '')
        platforms = data.get('platforms', ['youtube', 'instagram', 'tiktok'])
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        channels = channel_collector.collect_all_channels(query, platforms)
        
        return jsonify({
            'success': True,
            'channels': channels,
            'count': len(channels)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-channels', methods=['POST'])
def analyze_channels():
    """Analyze channels and their posts"""
    try:
        data = request.json
        channels = data.get('channels', [])
        
        if not channels:
            return jsonify({'error': 'Channels are required'}), 400
        
        results = []
        for channel in channels:
            # Get last post
            last_post = post_analyzer.get_last_post(channel)
            
            # Analyze if can hire editors
            if last_post:
                analysis = post_analyzer.analyze_post_for_editor_hire(last_post, channel)
            else:
                analysis = {
                    'can_hire_editors': False,
                    'confidence': 0.0,
                    'reasons': ['No post found'],
                    'analysis': 'No post available for analysis'
                }
            
            results.append({
                'channel': channel,
                'last_post': last_post,
                'analysis': analysis
            })
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/collect-leads', methods=['POST'])
def collect_leads():
    """Collect leads from channels"""
    try:
        data = request.json
        channels = data.get('channels', [])
        
        if not channels:
            return jsonify({'error': 'Channels are required'}), 400
        
        # Filter channels that can hire editors
        eligible_channels = []
        for channel_data in channels:
            if isinstance(channel_data, dict) and channel_data.get('analysis', {}).get('can_hire_editors', False):
                eligible_channels.append(channel_data.get('channel', {}))
        
        # Collect leads
        leads = lead_collector.collect_leads_batch(eligible_channels)
        
        # Enrich leads
        enriched_leads = [lead_collector.enrich_lead(lead) for lead in leads]
        
        return jsonify({
            'success': True,
            'leads': enriched_leads,
            'count': len(enriched_leads)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-emails', methods=['POST'])
def send_emails():
    """Send cold emails to leads"""
    try:
        data = request.json
        leads = data.get('leads', [])
        channels_map = {ch.get('channel_id', ''): ch for ch in data.get('channels', [])}
        
        if not leads:
            return jsonify({'error': 'Leads are required'}), 400
        
        # Send emails
        results = email_sender.send_batch_emails(leads, channels_map)
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/full-automation', methods=['POST'])
def full_automation():
    """Full automation: collect, analyze, get leads, send emails"""
    try:
        data = request.json
        query = data.get('query', '')
        platforms = data.get('platforms', ['youtube', 'instagram', 'tiktok'])
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Step 1: Collect channels
        channels = channel_collector.collect_all_channels(query, platforms)
        
        # Step 2: Analyze channels
        analyzed_channels = []
        for channel in channels:
            last_post = post_analyzer.get_last_post(channel)
            if last_post:
                analysis = post_analyzer.analyze_post_for_editor_hire(last_post, channel)
            else:
                analysis = {'can_hire_editors': False, 'confidence': 0.0, 'reasons': [], 'analysis': ''}
            
            analyzed_channels.append({
                'channel': channel,
                'last_post': last_post,
                'analysis': analysis
            })
        
        # Step 3: Filter and collect leads
        eligible_channels = [ac['channel'] for ac in analyzed_channels 
                            if ac['analysis'].get('can_hire_editors', False)]
        leads = lead_collector.collect_leads_batch(eligible_channels)
        enriched_leads = [lead_collector.enrich_lead(lead) for lead in leads]
        
        # Step 4: Send emails
        channels_map = {ch['channel_id']: ch for ch in eligible_channels}
        email_results = email_sender.send_batch_emails(enriched_leads, channels_map)
        
        return jsonify({
            'success': True,
            'channels_collected': len(channels),
            'channels_analyzed': len(analyzed_channels),
            'leads_collected': len(enriched_leads),
            'emails_sent': email_results['sent'],
            'emails_failed': email_results['failed'],
            'details': {
                'channels': analyzed_channels,
                'leads': enriched_leads,
                'email_results': email_results
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-channels', methods=['POST'])
def process_channels_bulk():
    """Process bulk-pasted channel names with selected platforms.
    For each name+platform, find last post and best contact, then return leads with a ready message template.
    """
    try:
        data = request.json or {}
        channels_text = data.get('channels_text', '')
        platforms = data.get('platforms', ['youtube', 'instagram', 'tiktok'])

        if not channels_text:
            return jsonify({'error': 'channels_text is required'}), 400

        # Parse names: split by newlines/commas
        raw_names = [x.strip() for x in channels_text.replace(',', '\n').split('\n')]
        names = [n for n in raw_names if n]

        processed = []
        leads = []

        for name in names:
            for platform in platforms:
                channel_obj = build_channel_stub(name, platform)
                # Last post (best effort)
                last_post = post_analyzer.get_last_post(channel_obj) or {}
                # Lead collection
                lead = lead_collector.collect_lead_from_channel(channel_obj)
                enriched = lead_collector.enrich_lead(lead)

                # Ready message template
                template = generate_message_template(channel_obj, last_post)

                # Contact link preference: Gmail compose if email, else discord/contact link, else channel URL
                gmail_link = build_gmail_compose_link(
                    to=enriched.get('email'),
                    subject=f"Quick edit proposal for @{channel_obj.get('username','')}",
                    body=template
                ) if enriched.get('email') else ''
                contact_link = (
                    gmail_link
                    or _pick_best_contact_link(lead.get('contact_info', {}).get('links', []))
                    or channel_obj.get('url', '')
                )

                item = {
                    'channel': channel_obj,
                    'last_post': last_post,
                    'lead': {
                        **enriched,
                        'contact_link': contact_link,
                        'message_template': template,
                    }
                }
                processed.append(item)
                leads.append({
                    'username': channel_obj.get('username'),
                    'platform': platform,
                    'email': enriched.get('email'),
                    'contact_link': contact_link,
                    'message_template': template,
                })

        return jsonify({
            'success': True,
            'count': len(processed),
            'processed': processed,
            'leads': leads
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-channel', methods=['POST'])
def process_channel_single():
    """Process a single channel name across selected platforms for progressive UI updates."""
    try:
        data = request.json or {}
        name = (data.get('name') or '').strip()
        platforms = data.get('platforms', ['youtube', 'instagram', 'tiktok'])
        if not name:
            return jsonify({'error': 'name is required'}), 400

        processed = []
        leads = []
        for platform in platforms:
            channel_obj = build_channel_stub(name, platform)
            last_post = post_analyzer.get_last_post(channel_obj) or {}
            lead = lead_collector.collect_lead_from_channel(channel_obj)
            enriched = lead_collector.enrich_lead(lead)
            template = generate_message_template(channel_obj, last_post)
            gmail_link = build_gmail_compose_link(
                to=enriched.get('email'),
                subject=f"Quick edit proposal for @{channel_obj.get('username','')}",
                body=template
            ) if enriched.get('email') else ''
            contact_link = (
                gmail_link
                or _pick_best_contact_link(lead.get('contact_info', {}).get('links', []))
                or channel_obj.get('url', '')
            )
            processed.append({
                'channel': channel_obj,
                'last_post': last_post,
                'lead': {**enriched, 'contact_link': contact_link, 'message_template': template}
            })
            leads.append({
                'username': channel_obj.get('username'),
                'platform': platform,
                'email': enriched.get('email'),
                'contact_link': contact_link,
                'message_template': template,
            })
        return jsonify({'success': True, 'count': len(processed), 'processed': processed, 'leads': leads})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def build_channel_stub(username: str, platform: str) -> dict:
    """Create a minimal channel object from a username and platform."""
    username_clean = username.lstrip('@')
    url = ''
    channel_id = ''
    if platform == 'youtube':
        # Without channel ID we can at least link to the handle page
        url = f"https://www.youtube.com/@{username_clean}"
    elif platform == 'instagram':
        url = f"https://www.instagram.com/{username_clean}/"
    elif platform == 'tiktok':
        url = f"https://www.tiktok.com/@{username_clean}"
    return {
        'platform': platform,
        'channel_id': channel_id,
        'username': username_clean,
        'description': '',
        'subscriber_count': 0,
        'video_count': 0,
        'url': url,
        'thumbnail': ''
    }

def generate_message_template(channel: dict, last_post: dict) -> str:
    """Generate a short outreach message template tailored to the channel."""
    handle = channel.get('username', '')
    platform = channel.get('platform', '')
    last_title = last_post.get('title', '') if last_post else ''
    return (
        f"Hi @{handle},\n\n"
        f"Loved your {platform} content"
        + (f" — especially '{last_title}'." if last_title else ".")
        + " I'm a video editor helping creators speed up production while keeping quality high.\n\n"
        "If you're open to it, I can share a quick sample edit tailored to your style."
        "\n\nCheers,\nYour Name"
    )

def build_gmail_compose_link(to: str, subject: str, body: str) -> str:
    """Create a Gmail compose URL with prefilled fields."""
    try:
        if not to:
            return ''
        import urllib.parse as _u
        params = {
            'view': 'cm',
            'to': to,
            'su': subject or '',
            'body': body or ''
        }
        return f"https://mail.google.com/mail/?{_u.urlencode(params)}"
    except Exception:
        return ''

def _pick_best_contact_link(links: list) -> str:
    """Pick the most promising contact link from a list (prefer Discord/invite, then contact pages)."""
    if not links:
        return ''
    # Prefer discord invites
    for link in links:
        l = (link or '').lower()
        if 'discord.gg' in l or 'discord.com/invite' in l:
            return link
    # Else first link
    return links[0]
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
