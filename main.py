#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Persian Telegram Bot for Behnoosh
A personalized bot with music search, jokes, and chat functionality
"""

import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from config import Config
from handlers.commands import CommandHandlers
from handlers.messages import MessageHandlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class PersianBot:
    def __init__(self):
        """Initialize the Persian bot with handlers"""
        self.config = Config()
        self.command_handlers = CommandHandlers()
        self.message_handlers = MessageHandlers()
        
    def setup_handlers(self, application: Application) -> None:
        """Setup all command and message handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.command_handlers.start))
        application.add_handler(CommandHandler("help", self.command_handlers.help_command))
        application.add_handler(CommandHandler("song", self.command_handlers.song))
        application.add_handler(CommandHandler("joke", self.command_handlers.joke))
        application.add_handler(CommandHandler("talk", self.command_handlers.talk))
        
        # Message handlers (non-command text messages)
        application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, 
                self.message_handlers.handle_text_message
            )
        )
        
        # Voice message handler
        application.add_handler(
            MessageHandler(
                filters.VOICE, 
                self.message_handlers.handle_voice_message
            )
        )
        
        # Error handler
        application.add_error_handler(self.error_handler)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors gracefully with Persian messages"""
        logger.error(f"Exception while handling an update: {context.error}")
        
        if update.effective_message:
            await update.effective_message.reply_text(
                "بهنوش جان، متأسفانه یه مشکل پیش اومده. لطفاً دوباره امتحان کن! 🙏"
            )

def main():
    """Main function to start the bot"""
    try:
        # Create bot instance
        bot = PersianBot()
        
        # Create application
        application = Application.builder().token(bot.config.TELEGRAM_TOKEN).build()
        
        # Setup handlers
        bot.setup_handlers(application)
        
        logger.info("Bot is starting...")
        
        # Start the bot with webhook or polling
        if bot.config.WEBHOOK_URL:
            # Webhook mode for production
            application.run_webhook(
                listen="0.0.0.0",
                port=8000,
                url_path=bot.config.TELEGRAM_TOKEN,
                webhook_url=f"{bot.config.WEBHOOK_URL}/{bot.config.TELEGRAM_TOKEN}"
            )
        else:
            # Polling mode for development
            application.run_polling(allowed_updates=Update.ALL_TYPES)
            
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
