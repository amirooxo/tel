#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chat service for handling conversations with Behnoosh
"""

import logging
import random
import requests
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.config = Config()
        
        # Persian conversation templates for fallback
        self.conversation_templates = [
            f"{self.config.USER_NAME} جان، حرفت خیلی جالب بود!",
            f"{self.config.USER_NAME}، من همیشه اینجام که باهات حرف بزنم.",
            f"از این حرفت خوشم اومد، {self.config.USER_NAME}!",
            f"{self.config.USER_NAME} عزیزم، چه خبر؟",
            f"همیشه دوست دارم باهات گپ بزنم، {self.config.USER_NAME} جان!"
        ]
        
        # Movie suggestions
        self.movie_suggestions = [
            "فیلم 'خانه پدری' ساخته کیانوش عیاری",
            "فیلم 'درباره الی' اصغر فرهادی",
            "فیلم 'جدایی نادر از سیمین'",
            "فیلم 'فروشنده' اصغر فرهادی",
            "فیلم 'مادر' علی حاتمی"
        ]
        
        # Music suggestions
        self.music_suggestions = [
            "آهنگ 'دیره' محسن یگانه",
            "آهنگ 'نگاه' محسن چاوشی",
            "آهنگ 'بهت قول میدم' آرون افشار",
            "آهنگ 'دل' حامید حامی",
            "آهنگ 'عاشقانه' محسن ابراهیم زاده"
        ]
    
    async def get_response(self, user_message: str) -> str:
        """
        Get a response to user message
        Priority: Gemini API -> Pattern matching -> Fallback responses
        """
        try:
            # Try Gemini API if available
            if self.config.has_gemini_api:
                gemini_response = await self._get_gemini_response(user_message)
                if gemini_response:
                    return gemini_response
            
            # Pattern-based responses
            pattern_response = self._get_pattern_response(user_message)
            if pattern_response:
                return pattern_response
            
            # Fallback to template responses
            return random.choice(self.conversation_templates)
            
        except Exception as e:
            logger.error(f"Chat service error: {e}")
            return f"{self.config.USER_NAME} جان، متأسفانه نتونستم جواب درستی بدم. دوباره امتحان کن! 🤔"
    
    async def _get_gemini_response(self, user_message: str) -> Optional[str]:
        """Get response from Gemini API"""
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
            
            headers = {
                "x-goog-api-key": self.config.GEMINI_API_KEY,
                "Content-Type": "application/json"
            }
            
            # Create personalized prompt
            prompt = f"""تو امیر هستی و داری با همسرت بهنوش حرف می‌زنی. پاسخت باید:
- به فارسی باشه
- گرم و صمیمی باشه
- با خطاب 'بهنوش جان' یا 'بهنوش' شروع شه
- کوتاه و مفید باشه (حداکثر 100 کلمه)

پیام بهنوش: {user_message}

پاسخ امیر:"""
            
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 200
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    return text.strip()
            else:
                logger.error(f"Gemini API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            
        return None
    
    def _get_pattern_response(self, user_message: str) -> Optional[str]:
        """Get response based on message patterns"""
        message_lower = user_message.lower()
        
        # Movie suggestions
        if any(word in message_lower for word in ['فیلم', 'سینما', 'movie']):
            suggestion = random.choice(self.movie_suggestions)
            return f"{self.config.USER_NAME} جان، {suggestion} رو پیشنهاد می‌دم! خیلی قشنگه 🎬"
        
        # Music suggestions
        if any(word in message_lower for word in ['آهنگ', 'موزیک', 'music']):
            suggestion = random.choice(self.music_suggestions)
            return f"{self.config.USER_NAME} جان، {suggestion} رو گوش کن، فوق‌العادست! 🎵"
        
        # Greetings
        if any(word in message_lower for word in ['سلام', 'درود', 'hello']):
            return f"سلام {self.config.USER_NAME} جان! چطوری عزیزم؟ 😊"
        
        # How are you
        if any(word in message_lower for word in ['چطوری', 'حالت', 'خوبی']):
            return f"{self.config.USER_NAME} جان، من عالیم! تو چطوری؟ امیدوارم حالت خوب باشه 💕"
        
        # Love expressions
        if any(word in message_lower for word in ['دوست دارم', 'عاشقتم', 'love']):
            return f"{self.config.USER_NAME} جان، منم عاشقتم! ❤️"
        
        # Questions
        if any(word in message_lower for word in ['چی', 'چه', 'کجا', 'کی', 'چرا']):
            return f"{self.config.USER_NAME} جان، سؤال جالبی پرسیدی! بذار فکر کنم... 🤔"
        
        return None
