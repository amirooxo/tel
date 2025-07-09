
import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class MusicService:
    """Service for searching Persian music using public APIs"""
    
    def __init__(self, youtube_api_key: str, spotify_token: Optional[str] = None):
        self.youtube_api_key = youtube_api_key
        self.spotify_token = spotify_token
    
    def search_youtube_music(self, query: str) -> List[Dict]:
        """Search for Persian music on YouTube"""
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': f"{query} آهنگ ایرانی Persian music",
                'type': 'video',
                'maxResults': 5,
                'key': self.youtube_api_key,
                'regionCode': 'IR'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_youtube_results(data.get('items', []))
            
        except requests.exceptions.RequestException as e:
            logger.error(f"YouTube API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in YouTube search: {e}")
            return []
    
    def search_spotify_music(self, query: str) -> List[Dict]:
        """Search for Persian music on Spotify (if token available)"""
        if not self.spotify_token:
            return []
        
        try:
            url = "https://api.spotify.com/v1/search"
            headers = {
                'Authorization': f'Bearer {self.spotify_token}',
                'Content-Type': 'application/json'
            }
            params = {
                'q': f"{query} Persian Iranian",
                'type': 'track',
                'market': 'IR',
                'limit': 5
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_spotify_results(data.get('tracks', {}).get('items', []))
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Spotify API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Spotify search: {e}")
            return []
    
    def _format_youtube_results(self, items: List[Dict]) -> List[Dict]:
        """Format YouTube search results"""
        formatted_results = []
        for item in items:
            try:
                result = {
                    'title': item['snippet']['title'],
                    'artist': item['snippet']['channelTitle'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'source': 'YouTube'
                }
                formatted_results.append(result)
            except KeyError as e:
                logger.warning(f"Missing key in YouTube result: {e}")
                continue
        
        return formatted_results
    
    def _format_spotify_results(self, items: List[Dict]) -> List[Dict]:
        """Format Spotify search results"""
        formatted_results = []
        for item in items:
            try:
                artists = ', '.join([artist['name'] for artist in item['artists']])
                result = {
                    'title': item['name'],
                    'artist': artists,
                    'url': item['external_urls']['spotify'],
                    'thumbnail': item['album']['images'][0]['url'] if item['album']['images'] else None,
                    'source': 'Spotify'
                }
                formatted_results.append(result)
            except KeyError as e:
                logger.warning(f"Missing key in Spotify result: {e}")
                continue
        
        return formatted_results
    
    def comprehensive_search(self, query: str) -> List[Dict]:
        """Search across multiple platforms"""
        all_results = []
        
        # Search YouTube
        youtube_results = self.search_youtube_music(query)
        all_results.extend(youtube_results)
        
        # Search Spotify if available
        spotify_results = self.search_spotify_music(query)
        all_results.extend(spotify_results)
        
        # Remove duplicates based on title similarity
        unique_results = self._remove_duplicates(all_results)
        
        return unique_results[:10]  # Return top 10 results
    
    def _remove_duplicates(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results based on title similarity"""
        unique_results = []
        seen_titles = set()
        
        for result in results:
            title_lower = result['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_results.append(result)
        
        return unique_results
