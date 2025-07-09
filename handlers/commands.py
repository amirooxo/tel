#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command handlers for the Persian Telegram Bot
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.music_service import MusicService
from services.tts_service import TTSService
from services.chat_service import ChatService
from utils.persian_jokes import PersianJokes
from config import Config

logger = logging.getLogger(__name__)

class CommandHandlers:
    def __init__(self):
        self.config = Config()
        self.music_service = MusicService()
        self.tts_service = TTSService()
        self.chat_service = ChatService()
        self.jokes = PersianJokes()
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        welcome_message = f"""سلام {self.config.USER_NAME} جان! 💕

من {self.config.BOT_NAME}، دستیار شخصی توام! 😊

دستورات من:
🎵 /song [نام آهنگ یا خواننده] - برای پیدا کردن آهنگ فارسی
😂 /joke - برای شنیدن جک فارسی
💬 /talk [متن] - برای گپ زدن
❓ /help - برای راهنمای کامل

همچنین می‌تونی مستقیم با من حرف بزنی! 🗣️"""

        await update.message.reply_text(welcome_message)
        
        # Send welcome voice message if TTS is available
        try:
            audio_file = await self.tts_service.text_to_speech(
                f"{self.config.USER_NAME} جان، خوشحالم که دوباره اینجایی!"
            )
            if audio_file:
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_voice(audio)
        except Exception as e:
            logger.warning(f"Could not send welcome voice: {e}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_text = f"""راهنمای کامل ربات {self.config.BOT_NAME} 📖

🎵 **جستجوی موزیک:**
/song [نام آهنگ یا خواننده]
مثال: /song محسن یگانه دیره

😂 **جک فارسی:**
/joke - برای شنیدن جک تازه

💬 **گپ و چت:**
/talk [متن شما]
یا فقط پیام بفرستید

🎤 **پیام صوتی:**
پیام صوتی بفرستید تا جوابتون رو صوتی بدم!

📱 **نکات مهم:**
• همه جواب‌ها به فارسی هستند
• پیام‌های صوتی ارسال می‌شود
• آهنگ‌های فارسی از منابع معتبر جستجو می‌شود

{self.config.USER_NAME} جان، هر سؤالی داری بپرس! 💕"""

        await update.message.reply_text(help_text)
    
    async def song(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /song command for music search"""
        if not context.args:
            await update.message.reply_text(
                f"{self.config.USER_NAME} جان، نام آهنگ یا خواننده‌ای که می‌خوای رو بنویس!\n"
                "مثال: /song محسن یگانه دیره"
            )
            return
        
        query = " ".join(context.args)
        
        # Send typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, 
            action="typing"
        )
        
        try:
            # Search for music
            results = await self.music_service.search_persian_music(query)
            
            if results:
                response_text = f"{self.config.USER_NAME} جان، این آهنگ‌ها رو برات پیدا کردم! 🎵\n\n"
                
                for i, song in enumerate(results[:5], 1):  # Limit to 5 results
                    response_text += f"{i}. **{song['title']}**\n"
                    if song.get('artist'):
                        response_text += f"خواننده: {song['artist']}\n"
                    if song.get('url'):
                        response_text += f"لینک: {song['url']}\n"
                    response_text += "─────────────\n"
                
                await update.message.reply_text(
                    response_text, 
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
                
                # Send voice response
                voice_message = f"{self.config.USER_NAME} جان، {len(results)} آهنگ برات پیدا کردم!"
                audio_file = await self.tts_service.text_to_speech(voice_message)
                if audio_file:
                    with open(audio_file, 'rb') as audio:
                        await update.message.reply_voice(audio)
                        
            else:
                error_message = f"{self.config.USER_NAME} جان، متأسفانه این آهنگ رو پیدا نکردم. یه چیز دیگه امتحان کن! 🎼"
                await update.message.reply_text(error_message)
                
                # Send voice error message
                audio_file = await self.tts_service.text_to_speech(error_message)
                if audio_file:
                    with open(audio_file, 'rb') as audio:
                        await update.message.reply_voice(audio)
                        
        except Exception as e:
            logger.error(f"Error in song search: {e}")
            await update.message.reply_text(
                f"{self.config.USER_NAME} جان، توی جستجوی آهنگ مشکلی پیش اومد. لطفاً دوباره امتحان کن! 🙏"
            )
    
    async def joke(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /joke command"""
        try:
            joke_text = self.jokes.get_random_joke()
            
            # Send text joke
            await update.message.reply_text(joke_text)
            
            # Send voice joke
            audio_file = await self.tts_service.text_to_speech(joke_text)
            if audio_file:
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_voice(
                        audio, 
                        caption=f"{self.config.USER_NAME}، این جک رو گوش کن! 😄"
                    )
                    
        except Exception as e:
            logger.error(f"Error in joke command: {e}")
            await update.message.reply_text(
                f"{self.config.USER_NAME} جان، توی گفتن جک مشکلی پیش اومد! بعداً دوباره امتحان کن 😅"
            )
    
    async def talk(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /talk command for conversation"""
        if not context.args:
            await update.message.reply_text(
                f"{self.config.USER_NAME} جان، چی می‌خوای بگی؟\n"
                "مثال: /talk یه فیلم خوب پیشنهاد بده"
            )
            return
        
        user_message = " ".join(context.args)
        
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
            audio_file = await self.tts_service.text_to_speech(response)
            if audio_file:
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_voice(audio)
                    
        except Exception as e:
            logger.error(f"Error in talk command: {e}")
            await update.message.reply_text(
                f"{self.config.USER_NAME} جان، نتونستم جواب درستی بدم. دوباره امتحان کن! 🤔"
            )
