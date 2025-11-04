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
from config import THEME_COLORS

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
