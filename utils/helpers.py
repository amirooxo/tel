#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper utilities for the Persian Telegram Bot
"""

import os
import logging
import re
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PersianHelper:
    """Helper functions for Persian text processing"""
    
    @staticmethod
    def clean_persian_text(text: str) -> str:
        """Clean and normalize Persian text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Normalize Persian/Arabic characters
        persian_chars = {
            'ك': 'ک',
            'ي': 'ی',
            '٠': '۰',
            '١': '۱',
            '٢': '۲',
            '٣': '۳',
            '٤': '۴',
            '٥': '۵',
            '٦': '۶',
            '٧': '۷',
            '٨': '۸',
            '٩': '۹'
        }
        
        for arabic, persian in persian_chars.items():
            text = text.replace(arabic, persian)
        
        return text
    
    @staticmethod
    def is_persian_text(text: str) -> bool:
        """Check if text contains Persian characters"""
        persian_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
        return bool(re.search(persian_pattern, text))
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 4096) -> str:
        """Truncate text to fit Telegram message limits"""
        if len(text) <= max_length:
            return text
        
        # Try to cut at a word boundary
        truncated = text[:max_length-3]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # If we found a good break point
            return truncated[:last_space] + "..."
        else:
            return truncated + "..."

class FileHelper:
    """Helper functions for file operations"""
    
    @staticmethod
    def ensure_directory(directory: str) -> None:
        """Ensure directory exists"""
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def cleanup_old_files(directory: str, max_age_hours: int = 24) -> None:
        """Clean up old temporary files"""
        try:
            if not os.path.exists(directory):
                return
            
            current_time = datetime.now()
            
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    age_hours = (current_time - file_time).total_seconds() / 3600
                    
                    if age_hours > max_age_hours:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old file: {filename}")
                        
        except Exception as e:
            logger.error(f"Error cleaning up files: {e}")
    
    @staticmethod
    def get_file_size_mb(file_path: str) -> float:
        """Get file size in MB"""
        try:
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)
        except Exception:
            return 0.0

class ValidationHelper:
    """Helper functions for input validation"""
    
    @staticmethod
    def is_valid_song_query(query: str) -> bool:
        """Validate song search query"""
        if not query or len(query.strip()) < 2:
            return False
        
        if len(query) > 100:  # Too long
            return False
        
        # Check for basic content
        clean_query = re.sub(r'[^\w\s\u0600-\u06FF]', '', query)
        return len(clean_query.strip()) >= 2
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe filesystem operations"""
        # Remove or replace unsafe characters
        filename = re.sub(r'[^\w\s-.]', '', filename)
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename.strip('-.')

class LogHelper:
    """Helper functions for logging"""
    
    @staticmethod
    def setup_logging(log_level: str = "INFO") -> None:
        """Setup logging configuration"""
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=getattr(logging, log_level.upper()),
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('bot.log', encoding='utf-8')
            ]
        )
    
    @staticmethod
    def log_user_interaction(user_id: int, username: str, message_type: str, content: str) -> None:
        """Log user interactions for monitoring"""
        logger.info(
            f"User interaction - ID: {user_id}, Username: {username}, "
            f"Type: {message_type}, Content: {content[:50]}..."
        )
