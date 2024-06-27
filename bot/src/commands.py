"""
The commands for the bot.
"""

import os
from dotenv import load_dotenv
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
import pytz
from src.gpt_handler import provide_picture
import asyncio
import sys
sys.path.append('..')

# env variables
load_dotenv()
BOT_NAME =  os.getenv('BOT_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Send a message when the command /start is issued.
    """
    await update.message.reply_text(f"Greatings, call me {BOT_NAME}!")


async def world_time_now(important_timezones: dict, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Send a message when the command /world_time is issued.
    Provides the current itme in interesting places.
    List of places with timezones can be set in the config.json file.
    https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 (list of timezones)
    """

    place_width = time_width = 15

    message = "```\n"
    message += f"{'Place':<{place_width}} | {'Current time':<{time_width}}\n"
    message += '-' * place_width + '-+-' + '-' * time_width + '\n'

    for key, value in important_timezones.items():
        timezone = pytz.timezone(key)
        current_time = datetime.now(timezone).strftime('%H:%M')
        message += f"{value:<{place_width}} | {current_time:<{time_width}}\n"

    message += "```"

    await update.message.reply_text(message, parse_mode='MarkdownV2')


async def provide_picture_and_ask_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    When the command /picture is issued, ask for a prompt.
    Then provide a picture based on the prompt using OpenAI.
    """

    user_prompt = update.message.text.strip()
    
    await provide_picture(update, context, user_prompt)
    
    return ConversationHandler.END

