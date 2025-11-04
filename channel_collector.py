"""
Channel Collection Module for YouTube, Instagram, and TikTok
"""
import requests
import json
from typing import List, Dict, Optional
from config import YOUTUBE_API_KEY


class ChannelCollector:
    """Collects channels from YouTube, Instagram, and TikTok"""
    
    def __init__(self):
        self.youtube_api_key = YOUTUBE_API_KEY
        
    def collect_youtube_channels(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Collect YouTube channels based on search query
        Returns list of channel information
        """
        channels = []
        try:
            # Search for channels
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'channel',
                'maxResults': min(max_results, 50),
                'key': self.youtube_api_key
            }
            
            response = requests.get(search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    channel_id = item['snippet']['channelId']
                    channel_info = self._get_youtube_channel_details(channel_id)
                    if channel_info:
                        channels.append(channel_info)
        except Exception as e:
            print(f"Error collecting YouTube channels: {e}")
            
        return channels
    
    def _get_youtube_channel_details(self, channel_id: str) -> Optional[Dict]:
        """Get detailed information about a YouTube channel"""
        try:
            url = "https://www.googleapis.com/youtube/v3/channels"
            params = {
                'part': 'snippet,statistics,contentDetails',
                'id': channel_id,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    channel = data['items'][0]
                    return {
                        'platform': 'youtube',
                        'channel_id': channel_id,
                        'username': channel['snippet']['title'],
                        'description': channel['snippet'].get('description', ''),
                        'subscriber_count': int(channel['statistics'].get('subscriberCount', 0)),
                        'video_count': int(channel['statistics'].get('videoCount', 0)),
                        'url': f"https://www.youtube.com/channel/{channel_id}",
                        'thumbnail': channel['snippet']['thumbnails']['default']['url']
                    }
        except Exception as e:
            print(f"Error getting YouTube channel details: {e}")
        return None
    
    def collect_instagram_channels(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Collect Instagram profiles based on search query
        Note: Instagram API requires authentication, this is a simplified version
        """
        channels = []
        try:
            # Using web scraping approach (simplified)
            # In production, you'd use Instagram Basic Display API or Graph API
            search_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'user' in data['data']:
                    user = data['data']['user']
                    channels.append({
                        'platform': 'instagram',
                        'channel_id': user.get('id', ''),
                        'username': user.get('username', query),
                        'description': user.get('biography', ''),
                        'follower_count': user.get('edge_followed_by', {}).get('count', 0),
                        'post_count': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                        'url': f"https://www.instagram.com/{user.get('username', query)}/",
                        'thumbnail': user.get('profile_pic_url', '')
                    })
        except Exception as e:
            print(f"Error collecting Instagram channels: {e}")
            # Fallback: return mock data structure
            channels.append({
                'platform': 'instagram',
                'channel_id': f"ig_{query}",
                'username': query,
                'description': '',
                'follower_count': 0,
                'post_count': 0,
                'url': f"https://www.instagram.com/{query}/",
                'thumbnail': ''
            })
            
        return channels
    
    def collect_tiktok_channels(self, query: str, max_results: int = 50) -> List[Dict]:
        """
        Collect TikTok profiles based on search query
        Note: TikTok API requires authentication, this is a simplified version
        """
        channels = []
        try:
            # Using web scraping approach (simplified)
            # In production, you'd use TikTok API
            search_url = f"https://www.tiktok.com/@{query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                # Parse response to extract channel info
                # This is a simplified version
                channels.append({
                    'platform': 'tiktok',
                    'channel_id': f"tt_{query}",
                    'username': query,
                    'description': '',
                    'follower_count': 0,
                    'post_count': 0,
                    'url': f"https://www.tiktok.com/@{query}",
                    'thumbnail': ''
                })
        except Exception as e:
            print(f"Error collecting TikTok channels: {e}")
            # Fallback: return mock data structure
            channels.append({
                'platform': 'tiktok',
                'channel_id': f"tt_{query}",
                'username': query,
                'description': '',
                'follower_count': 0,
                'post_count': 0,
                'url': f"https://www.tiktok.com/@{query}",
                'thumbnail': ''
            })
            
        return channels
    
    def collect_all_channels(self, query: str, platforms: List[str] = None) -> List[Dict]:
        """Collect channels from all specified platforms"""
        if platforms is None:
            platforms = ['youtube', 'instagram', 'tiktok']
        
        all_channels = []
        
        if 'youtube' in platforms:
            all_channels.extend(self.collect_youtube_channels(query))
        
        if 'instagram' in platforms:
            all_channels.extend(self.collect_instagram_channels(query))
        
        if 'tiktok' in platforms:
            all_channels.extend(self.collect_tiktok_channels(query))
        
        return all_channels
