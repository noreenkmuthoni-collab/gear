"""
Post Analysis Module - Analyzes last posts from channels
"""
import requests
import json
from typing import Dict, Optional, List
from config import YOUTUBE_API_KEY, OPENAI_API_KEY

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class PostAnalyzer:
    """Analyzes posts from various platforms"""
    
    def __init__(self):
        self.youtube_api_key = YOUTUBE_API_KEY
        self.openai_api_key = OPENAI_API_KEY
        self.openai_client = None
        if self.openai_api_key and OPENAI_AVAILABLE:
            try:
                self.openai_client = OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.openai_client = None
    
    def get_last_post(self, channel_info: Dict) -> Optional[Dict]:
        """Get the last post from a channel"""
        platform = channel_info.get('platform', '')
        
        if platform == 'youtube':
            return self._get_youtube_last_video(channel_info)
        elif platform == 'instagram':
            return self._get_instagram_last_post(channel_info)
        elif platform == 'tiktok':
            return self._get_tiktok_last_video(channel_info)
        
        return None
    
    def _get_youtube_last_video(self, channel_info: Dict) -> Optional[Dict]:
        """Get the last video from a YouTube channel"""
        try:
            channel_id = channel_info.get('channel_id')
            if not channel_id:
                return None
            
            # Get uploads playlist
            url = "https://www.googleapis.com/youtube/v3/channels"
            params = {
                'part': 'contentDetails',
                'id': channel_id,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('items'):
                    uploads_playlist = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                    
                    # Get latest video
                    videos_url = "https://www.googleapis.com/youtube/v3/playlistItems"
                    videos_params = {
                        'part': 'snippet',
                        'playlistId': uploads_playlist,
                        'maxResults': 1,
                        'key': self.youtube_api_key
                    }
                    
                    videos_response = requests.get(videos_url, params=videos_params)
                    if videos_response.status_code == 200:
                        videos_data = videos_response.json()
                        if videos_data.get('items'):
                            video = videos_data['items'][0]
                            snippet = video['snippet']
                            return {
                                'platform': 'youtube',
                                'post_id': snippet['resourceId']['videoId'],
                                'title': snippet.get('title', ''),
                                'description': snippet.get('description', ''),
                                'published_at': snippet.get('publishedAt', ''),
                                'url': f"https://www.youtube.com/watch?v={snippet['resourceId']['videoId']}",
                                'thumbnail': snippet['thumbnails']['default']['url']
                            }
        except Exception as e:
            print(f"Error getting YouTube last video: {e}")
        
        return None
    
    def _get_instagram_last_post(self, channel_info: Dict) -> Optional[Dict]:
        """Get the last post from an Instagram profile"""
        try:
            username = channel_info.get('username', '')
            if not username:
                return None
            
            # Using web scraping approach (simplified)
            url = f"https://www.instagram.com/{username}/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Parse HTML to extract last post
                # This is simplified - in production use proper API
                return {
                    'platform': 'instagram',
                    'post_id': f"ig_post_{username}",
                    'title': '',
                    'description': f'Latest post from @{username}',
                    'published_at': '',
                    'url': url,
                    'thumbnail': ''
                }
        except Exception as e:
            print(f"Error getting Instagram last post: {e}")
        
        return None
    
    def _get_tiktok_last_video(self, channel_info: Dict) -> Optional[Dict]:
        """Get the last video from a TikTok profile"""
        try:
            username = channel_info.get('username', '')
            if not username:
                return None
            
            # Using web scraping approach (simplified)
            url = f"https://www.tiktok.com/@{username}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Parse HTML to extract last video
                # This is simplified - in production use proper API
                return {
                    'platform': 'tiktok',
                    'post_id': f"tt_video_{username}",
                    'title': '',
                    'description': f'Latest video from @{username}',
                    'published_at': '',
                    'url': url,
                    'thumbnail': ''
                }
        except Exception as e:
            print(f"Error getting TikTok last video: {e}")
        
        return None
    
    def analyze_post_for_editor_hire(self, post: Dict, channel_info: Dict) -> Dict:
        """
        Analyze if the channel/post indicates they can hire editors
        Uses AI to analyze content
        """
        analysis_result = {
            'can_hire_editors': False,
            'confidence': 0.0,
            'reasons': [],
            'analysis': ''
        }
        
        try:
            # Combine post and channel information
            content_to_analyze = f"""
            Channel: {channel_info.get('username', '')}
            Platform: {channel_info.get('platform', '')}
            Subscribers/Followers: {channel_info.get('subscriber_count', 0)}
            Post Title: {post.get('title', '')}
            Post Description: {post.get('description', '')}
            Channel Description: {channel_info.get('description', '')}
            """
            
            # Use OpenAI to analyze
            if self.openai_client:
                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an AI that analyzes social media channels to determine if they are likely to hire video editors. Look for indicators like: growing channel, professional content, mentions of needing help, high subscriber count, regular posting schedule, or content that suggests they produce videos regularly."
                            },
                            {
                                "role": "user",
                                "content": f"Analyze this channel and post information:\n{content_to_analyze}\n\nCan this channel hire editors? Provide a yes/no answer, confidence score (0-1), and brief reasons."
                            }
                        ],
                        max_tokens=200
                    )
                    
                    analysis_text = response.choices[0].message.content
                    analysis_result['analysis'] = analysis_text
                    
                    # Parse the response
                    if 'yes' in analysis_text.lower():
                        analysis_result['can_hire_editors'] = True
                        analysis_result['confidence'] = 0.7
                    
                    # Extract confidence score if mentioned
                    if 'confidence' in analysis_text.lower():
                        # Try to extract number
                        import re
                        confidence_match = re.search(r'(\d+\.?\d*)', analysis_text)
                        if confidence_match:
                            conf_value = float(confidence_match.group(1))
                            if conf_value > 1:
                                conf_value = conf_value / 100
                            analysis_result['confidence'] = min(max(conf_value, 0.0), 1.0)
                    
                    analysis_result['reasons'] = analysis_text.split('\n')[:3]
                    
                except Exception as e:
                    print(f"OpenAI API error: {e}")
                    # Fallback analysis
                    analysis_result = self._fallback_analysis(channel_info, post)
            else:
                # Fallback analysis without AI
                analysis_result = self._fallback_analysis(channel_info, post)
                
        except Exception as e:
            print(f"Error analyzing post: {e}")
            analysis_result = self._fallback_analysis(channel_info, post)
        
        return analysis_result
    
    def _fallback_analysis(self, channel_info: Dict, post: Dict) -> Dict:
        """Fallback analysis when AI is not available"""
        subscriber_count = channel_info.get('subscriber_count', 0)
        video_count = channel_info.get('video_count', 0)
        
        can_hire = False
        confidence = 0.0
        reasons = []
        
        # Simple heuristics
        if subscriber_count > 1000:
            can_hire = True
            confidence = 0.6
            reasons.append(f"Has {subscriber_count} subscribers")
        
        if video_count > 10:
            can_hire = True
            confidence = min(confidence + 0.2, 0.9)
            reasons.append(f"Has {video_count} videos")
        
        return {
            'can_hire_editors': can_hire,
            'confidence': confidence,
            'reasons': reasons,
            'analysis': f"Based on subscriber count ({subscriber_count}) and video count ({video_count})"
        }
