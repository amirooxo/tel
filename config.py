#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for the Persian Telegram Bot
"""

import os
from typing import Optional

class Config:
    """Configuration class for bot settings and API keys"""
    
    def __init__(self):
        # Bot configuration
        self.TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8136898238:AAHRrQ-87-9zYy946cnLnmXtLhnzlrmJDDg")
        
        # API Keys
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
        self.YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
        self.ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
        
        # Webhook configuration
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
        
        # Bot personality
        self.BOT_NAME = "امیر"
        self.USER_NAME = "بهنوش"
        
        # TTS Configuration
        self.TTS_LANGUAGE = "fa"
        self.TTS_SLOW = False
        
        # Voice cloning settings
        self.ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
        
        # Rate limiting
        self.MAX_MESSAGE_LENGTH = 4096
        self.MAX_AUDIO_DURATION = 300  # 5 minutes
        
        # File paths
        self.TEMP_AUDIO_DIR = "temp_audio"
        
        # Ensure temp directory exists
        os.makedirs(self.TEMP_AUDIO_DIR, exist_ok=True)
    
    def validate_config(self) -> bool:
        """Validate essential configuration"""
        if not self.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN is required")
        return True
    
    @property
    def has_youtube_api(self) -> bool:
        """Check if YouTube API key is available"""
        return bool(self.YOUTUBE_API_KEY)
    
    @property
    def has_gemini_api(self) -> bool:
        """Check if Gemini API key is available"""
        return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY.startswith("AIzaSy"))
    
    @property
    def has_elevenlabs_api(self) -> bool:
        """Check if ElevenLabs API key is available"""
        return bool(self.ELEVENLABS_API_KEY)
