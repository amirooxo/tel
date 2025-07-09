
import logging
from io import BytesIO
from gtts import gTTS
import os
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)

class VoiceUtils:
    """Utilities for text-to-speech conversion"""
    
    @staticmethod
    def text_to_speech(text: str, lang: str = 'fa', slow: bool = False) -> Optional[BytesIO]:
        """Convert text to speech using gTTS"""
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=lang, slow=slow)
            
            # Create BytesIO buffer
            audio_buffer = BytesIO()
            
            # Write to buffer
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer
            
        except Exception as e:
            logger.error(f"Text-to-speech conversion failed: {e}")
            return None
    
    @staticmethod
    def text_to_speech_file(text: str, filename: str, lang: str = 'fa', slow: bool = False) -> bool:
        """Convert text to speech and save to file"""
        try:
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(filename)
            return True
            
        except Exception as e:
            logger.error(f"Text-to-speech file creation failed: {e}")
            return False
    
    @staticmethod
    def create_temp_audio(text: str, lang: str = 'fa') -> Optional[str]:
        """Create temporary audio file and return path"""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()
            
            # Generate audio
            if VoiceUtils.text_to_speech_file(text, temp_path, lang):
                return temp_path
            else:
                os.unlink(temp_path)
                return None
                
        except Exception as e:
            logger.error(f"Temporary audio creation failed: {e}")
            return None
    
    @staticmethod
    def cleanup_temp_file(file_path: str) -> bool:
        """Clean up temporary audio file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                return True
            return False
            
        except Exception as e:
            logger.error(f"Temporary file cleanup failed: {e}")
            return False
