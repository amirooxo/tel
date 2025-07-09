#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Message handlers for non-command messages
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.chat_service import ChatService
from services.tts_service import TTSService
from config import Config

logger = logging.getLogger(__name__)

class MessageHandlers:
    def __init__(self):
        self.config = Config()
        self.chat_service = ChatService()
        self.tts_service = TTSService()
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular text messages (non-commands)"""
        user_message = update.message.text
        
        # Send typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, 
            action="typing"
        )
        
        try:
            # Get response from chat service
            response = await self.chat_service.get_response(user_message)
            
            # Send text response
            await update.message.reply_text(response)
            
            # Send voice response
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action="record_voice"
            )
            
            audio_file = await self.tts_service.text_to_speech(response)
            if audio_file:
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_voice(
                        audio,
                        caption=f"{self.config.USER_NAME} جان، پیام صوتی از {self.config.BOT_NAME}! 🎤"
                    )
                    
        except Exception as e:
            logger.error(f"Error handling text message: {e}")
            await update.message.reply_text(
                f"{self.config.USER_NAME} جان، متأسفانه نتونستم پیامت رو درست درک کنم. دوباره امتحان کن! 🙏"
            )
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle voice messages"""
        try:
            # For now, respond to voice with a friendly message
            # In future versions, we can add speech-to-text functionality
            response = f"{self.config.USER_NAME} جان، پیام صوتیت رو شنیدم! 🎤 فعلاً فقط می‌تونم به پیام‌های متنی جواب بدم، ولی خیلی زود قابلیت تشخیص گفتار هم اضافه می‌شه! 😊"
            
            await update.message.reply_text(response)
            
            # Send voice response
            audio_file = await self.tts_service.text_to_speech(response)
            if audio_file:
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_voice(audio)
                    
        except Exception as e:
            logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text(
                f"{self.config.USER_NAME} جان، توی پردازش پیام صوتیت مشکلی پیش اومد! 🎤"
            )
