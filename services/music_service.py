#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Music search service for Persian music platforms
"""

import logging
import requests
import asyncio
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class MusicService:
    def __init__(self):
        self.config = Config()
        
    async def search_persian_music(self, query: str) -> List[Dict]:
        """
        Search for Persian music using multiple sources
        Priority: RadioJavan API -> YouTube API -> Mock results
        """
        results = []
        
        # Try RadioJavan unofficial API first
        try:
            radiojavan_results = await self._search_radiojavan(query)
            if radiojavan_results:
                results.extend(radiojavan_results)
        except Exception as e:
            logger.warning(f"RadioJavan search failed: {e}")
        
        # Try YouTube API as fallback
        if not results and self.config.has_youtube_api:
            try:
                youtube_results = await self._search_youtube(query)
                if youtube_results:
                    results.extend(youtube_results)
            except Exception as e:
                logger.warning(f"YouTube search failed: {e}")
        
        # If no results found, return empty list (no mock data)
        return results[:10]  # Limit to 10 results
    
    async def _search_radiojavan(self, query: str) -> List[Dict]:
        """Search using RadioJavan unofficial API"""
        try:
            # Using radiojavanapi package approach
            # Note: This would require the radiojavanapi package to be installed
            # For now, we'll try a direct API approach
            
            search_url = "https://www.radiojavan.com/api/mp3_search"
            params = {
                'query': query,
                'limit': 10
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if 'mp3s' in data:
                    for item in data['mp3s']:
                        result = {
                            'title': item.get('song', 'نامشخص'),
                            'artist': item.get('artist', 'نامشخص'),
                            'url': f"https://www.radiojavan.com{item.get('link', '')}",
                            'source': 'RadioJavan',
                            'duration': item.get('length', ''),
                            'year': item.get('date', '')
                        }
                        results.append(result)
                
                return results
            
        except Exception as e:
            logger.error(f"RadioJavan API error: {e}")
            
        return []
    
    async def _search_youtube(self, query: str) -> List[Dict]:
        """Search YouTube for Persian music"""
        try:
            # Add Persian music keywords to improve results
            search_query = f"{query} آهنگ فارسی موزیک ایرانی"
            
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': search_query,
                'key': self.config.YOUTUBE_API_KEY,
                'type': 'video',
                'maxResults': 10,
                'regionCode': 'IR',  # Iran region
                'relevanceLanguage': 'fa'  # Persian language
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('items', []):
                    snippet = item['snippet']
                    video_id = item['id']['videoId']
                    
                    # Extract artist and song from title (basic parsing)
                    title = snippet['title']
                    channel = snippet['channelTitle']
                    
                    result = {
                        'title': title,
                        'artist': channel,
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'source': 'YouTube',
                        'description': snippet.get('description', '')[:100] + '...',
                        'published': snippet.get('publishedAt', '')
                    }
                    results.append(result)
                
                return results
            else:
                logger.error(f"YouTube API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            
        return []
    
    async def get_song_details(self, song_url: str) -> Optional[Dict]:
        """Get detailed information about a specific song"""
        try:
            # This would be implemented based on the specific platform
            # For now, return basic info
            return {
                'url': song_url,
                'status': 'available'
            }
        except Exception as e:
            logger.error(f"Error getting song details: {e}")
            return None
