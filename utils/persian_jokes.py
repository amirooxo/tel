#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Persian jokes collection for the bot
"""

import random
from config import Config

class PersianJokes:
    def __init__(self):
        self.config = Config()
        
        # Collection of family-friendly Persian jokes
        self.jokes = [
            f"{self.config.USER_NAME} جان، چرا اژدها از همه جدا شد؟ چون همش آتیش می‌سوزوند! 🐲🔥",
            
            f"{self.config.USER_NAME}، چرا شترمرغ سرشو کرد تو خاک؟ فکر کرد داره استوری می‌ذاره! 📱😂",
            
            f"{self.config.USER_NAME} جان، چرا ماهی نمی‌تونه تنیس بازی کنه؟ چون ترس داره از تور! 🐟🎾",
            
            f"{self.config.USER_NAME}، چرا کامپیوتر عینک زد؟ چون دید ضعیف شده بود! 👓💻",
            
            f"{self.config.USER_NAME} جان، چرا قورباغه گوشیش رو جواب نمی‌ده؟ چون تو استخر شنا می‌کنه! 🐸📱",
            
            f"{self.config.USER_NAME}، چرا کتاب ریاضی غمگین بود؟ چون پر از مسئله بود! 📚😢",
            
            f"{self.config.USER_NAME} جان، چرا آفتاب عینک آفتابی می‌زنه؟ چون نمی‌خواد کور بشه! ☀️🕶️",
            
            f"{self.config.USER_NAME}، چرا مداد شکست؟ چون حرفاش بی‌نقطه بود! ✏️😄",
            
            f"{self.config.USER_NAME} جان، چرا ساعت به دکتر رفت؟ چون احساس می‌کرد وقت نداره! ⏰🏥",
            
            f"{self.config.USER_NAME}، چرا کیک به دندونپزشک رفت؟ چون شیرینی‌هاش دردش می‌گرفت! 🍰🦷",
            
            f"{self.config.USER_NAME} جان، چرا هواپیما خسته شده بود؟ چون زیاد پرواز کرده بود! ✈️😴",
            
            f"{self.config.USER_NAME}، چرا عنکبوت اینترنت نداشت؟ چون تارش پاره شده بود! 🕷️💻",
            
            f"{self.config.USER_NAME} جان، چرا گوجه فرنگی سرخ شد؟ چون خجالت کشید! 🍅😊",
            
            f"{self.config.USER_NAME}، چرا باتری خسته بود؟ چون انرژیش تموم شده بود! 🔋😪",
            
            f"{self.config.USER_NAME} جان، چرا قلم به مدرسه نرفت؟ چون نوکش کُند شده بود! 🖊️🏫"
        ]
    
    def get_random_joke(self) -> str:
        """Get a random Persian joke"""
        return random.choice(self.jokes)
    
    def add_joke(self, joke: str) -> None:
        """Add a new joke to the collection"""
        if joke.strip():
            formatted_joke = f"{self.config.USER_NAME} جان، {joke}"
            self.jokes.append(formatted_joke)
    
    def get_all_jokes(self) -> list:
        """Get all jokes in the collection"""
        return self.jokes.copy()
