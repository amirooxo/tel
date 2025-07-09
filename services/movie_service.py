
import requests
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class MovieService:
    """Service for searching movies using public APIs"""
    
    def __init__(self, tmdb_api_key: str, omdb_api_key: Optional[str] = None):
        self.tmdb_api_key = tmdb_api_key
        self.omdb_api_key = omdb_api_key
    
    def search_tmdb(self, query: str) -> List[Dict]:
        """Search movies using TMDB API"""
        try:
            url = "https://api.themoviedb.org/3/search/movie"
            params = {
                'api_key': self.tmdb_api_key,
                'query': query,
                'language': 'fa-IR',
                'region': 'IR',
                'include_adult': False
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_tmdb_results(data.get('results', []))
            
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in TMDB search: {e}")
            return []
    
    def search_omdb(self, query: str) -> List[Dict]:
        """Search movies using OMDB API (if key available)"""
        if not self.omdb_api_key:
            return []
        
        try:
            url = "http://www.omdbapi.com/"
            params = {
                'apikey': self.omdb_api_key,
                's': query,
                'type': 'movie',
                'r': 'json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('Response') == 'True':
                return self._format_omdb_results(data.get('Search', []))
            else:
                logger.warning(f"OMDB API returned error: {data.get('Error', 'Unknown error')}")
                return []
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OMDB API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in OMDB search: {e}")
            return []
    
    def search_persian_movies(self, query: str) -> List[Dict]:
        """Search specifically for Persian/Iranian movies"""
        try:
            url = "https://api.themoviedb.org/3/search/movie"
            params = {
                'api_key': self.tmdb_api_key,
                'query': f"{query} Persian Iranian",
                'language': 'fa-IR',
                'region': 'IR',
                'include_adult': False
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._format_tmdb_results(data.get('results', []))
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Persian movie search failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Persian movie search: {e}")
            return []
    
    def _format_tmdb_results(self, items: List[Dict]) -> List[Dict]:
        """Format TMDB search results"""
        formatted_results = []
        for item in items:
            try:
                poster_path = item.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                
                result = {
                    'title': item.get('title', 'نامشخص'),
                    'original_title': item.get('original_title', ''),
                    'overview': item.get('overview', 'خلاصه موجود نیست'),
                    'release_date': item.get('release_date', 'تاریخ نامشخص'),
                    'vote_average': item.get('vote_average', 0),
                    'poster_url': poster_url,
                    'tmdb_id': item.get('id'),
                    'source': 'TMDB'
                }
                formatted_results.append(result)
            except Exception as e:
                logger.warning(f"Error formatting TMDB result: {e}")
                continue
        
        return formatted_results
    
    def _format_omdb_results(self, items: List[Dict]) -> List[Dict]:
        """Format OMDB search results"""
        formatted_results = []
        for item in items:
            try:
                result = {
                    'title': item.get('Title', 'نامشخص'),
                    'year': item.get('Year', 'سال نامشخص'),
                    'type': item.get('Type', 'نوع نامشخص'),
                    'poster_url': item.get('Poster') if item.get('Poster') != 'N/A' else None,
                    'imdb_id': item.get('imdbID'),
                    'source': 'OMDB'
                }
                formatted_results.append(result)
            except Exception as e:
                logger.warning(f"Error formatting OMDB result: {e}")
                continue
        
        return formatted_results
    
    def comprehensive_search(self, query: str) -> List[Dict]:
        """Search across multiple movie databases"""
        all_results = []
        
        # Search TMDB
        tmdb_results = self.search_tmdb(query)
        all_results.extend(tmdb_results)
        
        # Search for Persian movies specifically
        persian_results = self.search_persian_movies(query)
        all_results.extend(persian_results)
        
        # Search OMDB if available
        omdb_results = self.search_omdb(query)
        all_results.extend(omdb_results)
        
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
