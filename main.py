
import os
import requests
import json
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from gtts import gTTS
import asyncio
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Check if required tokens are available
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN not found in environment variables")
    exit(1)
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables")
    exit(1)
if not YOUTUBE_API_KEY:
    logger.error("YOUTUBE_API_KEY not found in environment variables")
    exit(1)

# User configuration
USER_NAME = "بهنوش"
BOT_NAME = "امیر"

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Persian jokes database
JOKES = [
    f"{USER_NAME} جان، چرا اژدها از همه جدا شد؟ چون همش آتیش می‌سوزوند! 😂",
    f"{USER_NAME} عزیز، چرا شترمرغ سرشو کرد تو خاک؟ فکر کرد داره استوری می‌ذاره! 📱",
    f"{USER_NAME} جان، چرا کامپیوتر به دکتر رفت؟ چون ویروس گرفته بود! 💻",
    f"{USER_NAME} عزیز، چرا کتاب درس خوابش نمی‌برد؟ چون پر از کابوس بود! 📚",
    f"{USER_NAME} جان، چرا تلفن همیشه مودب بود؟ چون همیشه می‌گفت الو! 📞"
]

class PersianMusicAPI:
    """Handler for Persian music search using public APIs"""
    
    @staticmethod
    def search_youtube_music(query):
        """Search Persian music on YouTube"""
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': f"{query} آهنگ ایرانی Persian music",
                'type': 'video',
                'maxResults': 5,
                'key': YOUTUBE_API_KEY,
                'regionCode': 'IR'
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
        except Exception as e:
            logger.error(f"YouTube API error: {e}")
        return []
    
    @staticmethod
    def search_spotify_public(query):
        """Search Persian music using Spotify Web API (public endpoints)"""
        try:
            # Using Spotify's public search endpoint
            url = "https://api.spotify.com/v1/search"
            headers = {
                'Authorization': f'Bearer {os.getenv("SPOTIFY_TOKEN", "")}'
            }
            params = {
                'q': f"{query} Persian Iranian",
                'type': 'track',
                'market': 'IR',
                'limit': 5
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('tracks', {}).get('items', [])
        except Exception as e:
            logger.error(f"Spotify API error: {e}")
        return []

class MovieAPI:
    """Handler for movie search using public APIs"""
    
    @staticmethod
    def search_tmdb(query):
        """Search movies using TMDB API"""
        try:
            url = "https://api.themoviedb.org/3/search/movie"
            params = {
                'api_key': TMDB_API_KEY,
                'query': query,
                'language': 'fa-IR',
                'region': 'IR'
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
        except Exception as e:
            logger.error(f"TMDB API error: {e}")
        return []
    
    @staticmethod
    def search_omdb(query):
        """Search movies using OMDB API"""
        try:
            url = "http://www.omdbapi.com/"
            params = {
                'apikey': os.getenv("OMDB_API_KEY", ""),
                's': query,
                'type': 'movie'
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('Search', [])
        except Exception as e:
            logger.error(f"OMDB API error: {e}")
        return []

class VoiceService:
    """Text-to-speech service"""
    
    @staticmethod
    def create_audio(text, lang='fa'):
        """Create audio from text using gTTS"""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return None

class GeminiService:
    """Gemini AI service for conversations"""
    
    @staticmethod
    def generate_response(prompt):
        """Generate response using Gemini AI"""
        try:
            full_prompt = f"تو {BOT_NAME} هستی و با {USER_NAME} صحبت می‌کنی. به صورت دوستانه و گرم پاسخ بده. سوال: {prompt}"
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini AI error: {e}")
            return f"{USER_NAME} جان، متاسفانه الان نمی‌تونم جواب بدم. دوباره امتحان کن! 😊"

# Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    welcome_message = f"""
سلام {USER_NAME} عزیز! من {BOT_NAME}، دستیار شخصی توام 💙

از منوی زیر می‌تونی به راحتی از قابلیت‌هام استفاده کنی:
"""
    
    # Create inline keyboard menu
    keyboard = [
        [
            InlineKeyboardButton("🎵 جستجوی موزیک", callback_data='search_music'),
            InlineKeyboardButton("🎬 جستجوی فیلم", callback_data='search_movie')
        ],
        [
            InlineKeyboardButton("😂 جک بگو", callback_data='tell_joke'),
            InlineKeyboardButton("💬 گفتگو", callback_data='start_chat')
        ],
        [
            InlineKeyboardButton("📋 راهنما", callback_data='show_help'),
            InlineKeyboardButton("🔄 منوی اصلی", callback_data='main_menu')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu command handler"""
    menu_message = f"{USER_NAME} جان، منوی اصلی:"
    
    keyboard = [
        [
            InlineKeyboardButton("🎵 جستجوی موزیک", callback_data='search_music'),
            InlineKeyboardButton("🎬 جستجوی فیلم", callback_data='search_movie')
        ],
        [
            InlineKeyboardButton("😂 جک بگو", callback_data='tell_joke'),
            InlineKeyboardButton("💬 گفتگو", callback_data='start_chat')
        ],
        [
            InlineKeyboardButton("📋 راهنما", callback_data='show_help'),
            InlineKeyboardButton("🔄 منوی اصلی", callback_data='main_menu')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(menu_message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    help_text = f"""
راهنمای کامل ربات {BOT_NAME} 📖

🎵 جستجوی موزیک:
/song محسن یگانه - دیره
/song شادمهر عقیلی

🎬 جستجوی فیلم:
/movie جدایی نادر از سیمین
/movie مجید مجیدی

😂 شنیدن جک:
/joke

💬 گفتگو با هوش مصنوعی:
/talk یه فیلم خوب معرفی کن
یا فقط پیام بفرست بدون دستور

🔄 دستورات دیگر:
/start - شروع مجدد
/help - این راهنما

نکته: همه پاسخ‌ها به صورت صوتی و متنی ارسال می‌شوند 🎤
"""
    await update.message.reply_text(help_text)

async def song_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Song search command handler"""
    if not context.args:
        await update.message.reply_text(f"{USER_NAME} جان، اسم آهنگ یا خواننده رو بگو! مثال: /song محسن یگانه")
        return
    
    query = ' '.join(context.args)
    await update.message.reply_text(f"{USER_NAME} جان، دارم '{query}' رو برات جستجو می‌کنم... 🎵")
    
    # Search YouTube for Persian music
    youtube_results = PersianMusicAPI.search_youtube_music(query)
    
    if youtube_results:
        result_text = f"{USER_NAME} عزیز، این آهنگ‌ها رو برات پیدا کردم:\n\n"
        for i, video in enumerate(youtube_results[:3], 1):
            title = video['snippet']['title']
            video_id = video['id']['videoId']
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            result_text += f"{i}. {title}\n🔗 {youtube_url}\n\n"
        
        # Create audio response
        audio_text = f"{USER_NAME} جان، {len(youtube_results)} آهنگ برات پیدا کردم!"
        audio_buffer = VoiceService.create_audio(audio_text)
        
        if audio_buffer:
            await update.message.reply_audio(audio_buffer, caption=result_text)
        else:
            await update.message.reply_text(result_text)
    else:
        error_msg = f"{USER_NAME} جان، متاسفانه '{query}' رو پیدا نکردم. یه اسم دیگه امتحان کن! 🎵"
        audio_buffer = VoiceService.create_audio(error_msg)
        
        if audio_buffer:
            await update.message.reply_audio(audio_buffer, caption=error_msg)
        else:
            await update.message.reply_text(error_msg)

async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Movie search command handler"""
    if not context.args:
        await update.message.reply_text(f"{USER_NAME} جان، اسم فیلم رو بگو! مثال: /movie جدایی نادر از سیمین")
        return
    
    query = ' '.join(context.args)
    await update.message.reply_text(f"{USER_NAME} جان، دارم '{query}' رو برات جستجو می‌کنم... 🎬")
    
    # Search TMDB for movies
    tmdb_results = MovieAPI.search_tmdb(query)
    
    if tmdb_results:
        result_text = f"{USER_NAME} عزیز، این فیلم‌ها رو برات پیدا کردم:\n\n"
        for i, movie in enumerate(tmdb_results[:3], 1):
            title = movie.get('title', 'نامشخص')
            overview = movie.get('overview', 'خلاصه موجود نیست')
            release_date = movie.get('release_date', 'تاریخ نامشخص')
            vote_average = movie.get('vote_average', 0)
            
            result_text += f"{i}. {title}\n"
            result_text += f"📅 سال انتشار: {release_date}\n"
            result_text += f"⭐ امتیاز: {vote_average}/10\n"
            result_text += f"📝 خلاصه: {overview[:100]}...\n\n"
        
        # Create audio response
        audio_text = f"{USER_NAME} جان، {len(tmdb_results)} فیلم برات پیدا کردم!"
        audio_buffer = VoiceService.create_audio(audio_text)
        
        if audio_buffer:
            await update.message.reply_audio(audio_buffer, caption=result_text)
        else:
            await update.message.reply_text(result_text)
    else:
        error_msg = f"{USER_NAME} جان، متاسفانه '{query}' رو پیدا نکردم. یه اسم دیگه امتحان کن! 🎬"
        audio_buffer = VoiceService.create_audio(error_msg)
        
        if audio_buffer:
            await update.message.reply_audio(audio_buffer, caption=error_msg)
        else:
            await update.message.reply_text(error_msg)

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Joke command handler"""
    joke = random.choice(JOKES)
    audio_buffer = VoiceService.create_audio(joke)
    
    if audio_buffer:
        await update.message.reply_audio(audio_buffer, caption=joke)
    else:
        await update.message.reply_text(joke)

async def talk_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Talk command handler"""
    if not context.args:
        await update.message.reply_text(f"{USER_NAME} جان، چی می‌خوای بگی؟ مثال: /talk یه فیلم خوب معرفی کن")
        return
    
    user_message = ' '.join(context.args)
    await update.message.reply_text(f"{USER_NAME} جان، دارم فکر می‌کنم... 💭")
    
    # Generate response using Gemini
    response = GeminiService.generate_response(user_message)
    audio_buffer = VoiceService.create_audio(response)
    
    if audio_buffer:
        await update.message.reply_audio(audio_buffer, caption=response)
    else:
        await update.message.reply_text(response)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user_message = update.message.text
    
    # Generate response using Gemini
    response = GeminiService.generate_response(user_message)
    audio_buffer = VoiceService.create_audio(response)
    
    if audio_buffer:
        await update.message.reply_audio(audio_buffer, caption=response)
    else:
        await update.message.reply_text(response)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🎵 جستجوی موزیک", callback_data='search_music'),
            InlineKeyboardButton("🎬 جستجوی فیلم", callback_data='search_movie')
        ],
        [
            InlineKeyboardButton("😂 جک بگو", callback_data='tell_joke'),
            InlineKeyboardButton("💬 گفتگو", callback_data='start_chat')
        ],
        [
            InlineKeyboardButton("📋 راهنما", callback_data='show_help'),
            InlineKeyboardButton("🔄 منوی اصلی", callback_data='main_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query.data == 'search_music':
        text = f"{USER_NAME} جان، برای جستجوی موزیک، از دستور زیر استفاده کن:\n\n/song [نام آهنگ یا خواننده]\n\nمثال: /song محسن یگانه دیره"
        await query.edit_message_text(text, reply_markup=reply_markup)
        
    elif query.data == 'search_movie':
        text = f"{USER_NAME} جان، برای جستجوی فیلم، از دستور زیر استفاده کن:\n\n/movie [نام فیلم]\n\nمثال: /movie جدایی نادر از سیمین"
        await query.edit_message_text(text, reply_markup=reply_markup)
        
    elif query.data == 'tell_joke':
        joke = random.choice(JOKES)
        audio_buffer = VoiceService.create_audio(joke)
        
        # Send audio first
        if audio_buffer:
            await query.message.reply_audio(audio_buffer, caption=joke)
        else:
            await query.message.reply_text(joke)
            
        # Then update the message with menu
        await query.edit_message_text(f"{USER_NAME} جان، امیدوارم خوشت اومده باشه! 😊", reply_markup=reply_markup)
        
    elif query.data == 'start_chat':
        text = f"{USER_NAME} جان، برای گفتگو می‌تونی:\n\n1️⃣ از دستور /talk استفاده کنی:\n/talk یه فیلم خوب معرفی کن\n\n2️⃣ یا مستقیماً پیام بفرستی بدون دستور"
        await query.edit_message_text(text, reply_markup=reply_markup)
        
    elif query.data == 'show_help':
        help_text = f"""
راهنمای کامل ربات {BOT_NAME} 📖

🎵 جستجوی موزیک:
/song محسن یگانه - دیره
/song شادمهر عقیلی

🎬 جستجوی فیلم:
/movie جدایی نادر از سیمین
/movie مجید مجیدی

😂 شنیدن جک:
/joke یا از منو استفاده کن

💬 گفتگو با هوش مصنوعی:
/talk یه فیلم خوب معرفی کن
یا فقط پیام بفرست بدون دستور

🔄 دستورات دیگر:
/start - شروع مجدد
/menu - نمایش منو
/help - این راهنما

نکته: همه پاسخ‌ها به صورت صوتی و متنی ارسال می‌شوند 🎤
"""
        await query.edit_message_text(help_text, reply_markup=reply_markup)
        
    elif query.data == 'main_menu':
        menu_text = f"{USER_NAME} جان، منوی اصلی:"
        await query.edit_message_text(menu_text, reply_markup=reply_markup)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    logger.warning(f'Update {update} caused error {context.error}')
    if update.message:
        await update.message.reply_text(f"{USER_NAME} جان، یه مشکلی پیش اومد. دوباره امتحان کن! 😊")

def main():
    """Main function to run the bot"""
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("song", song_command))
    application.add_handler(CommandHandler("movie", movie_command))
    application.add_handler(CommandHandler("joke", joke_command))
    application.add_handler(CommandHandler("talk", talk_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Run the bot
    print(f"ربات {BOT_NAME} برای {USER_NAME} شروع شد! 🚀")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
