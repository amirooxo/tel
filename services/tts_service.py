#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text-to-Speech service with support for multiple TTS providers
"""

import logging
import os
import tempfile
import asyncio
from typing import Optional
from gtts import gTTS
import requests
from config import Config

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.config = Config()
        
    async def text_to_speech(self, text: str) -> Optional[str]:
        """
        Convert text to speech audio file
        Priority: ElevenLabs (if available) -> Google TTS
        """
        if not text.strip():
            return None
            
        try:
            # Try ElevenLabs voice cloning first
            if self.config.has_elevenlabs_api and self.config.ELEVENLABS_VOICE_ID:
                return await self._elevenlabs_tts(text)
            
            # Fallback to Google TTS
            return await self._google_tts(text)
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return None
    
    async def _elevenlabs_tts(self, text: str) -> Optional[str]:
        """Generate speech using ElevenLabs voice cloning"""
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.config.ELEVENLABS_VOICE_ID}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.config.ELEVENLABS_API_KEY
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Save to temporary file
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix='.mp3', 
                    dir=self.config.TEMP_AUDIO_DIR
                )
                temp_file.write(response.content)
                temp_file.close()
                
                return temp_file.name
            else:
                logger.error(f"ElevenLabs API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            
        return None
    
    async def _google_tts(self, text: str) -> Optional[str]:
        """Generate speech using Google TTS (fallback)"""
        try:
            # Run gTTS in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            
            def create_tts():
                return gTTS(
                    text=text, 
                    lang=self.config.TTS_LANGUAGE, 
                    slow=self.config.TTS_SLOW
                )
            
            tts = await loop.run_in_executor(None, create_tts)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix='.mp3', 
                dir=self.config.TEMP_AUDIO_DIR
            )
            temp_file.close()
            
            # Save TTS to file
            await loop.run_in_executor(None, tts.save, temp_file.name)
            
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return None
    
    def cleanup_audio_file(self, file_path: str) -> None:
        """Clean up temporary audio file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.warning(f"Could not cleanup audio file {file_path}: {e}")
