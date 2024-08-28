"""
This is orchestrator for telegram bot commands and communication
"""

import os
import json
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler, filters
                          , ConversationHandler, CallbackQueryHandler)

from src.commands import (start, world_time_now, provide_picture_and_ask_prompt
                          , start_picture_command)
from src.gpt_handler import message_acrhistator


# env variables
load_dotenv()
BOT_NAME =  os.getenv('BOT_NAME', 'GPT_Danilevich_bot')
BOT_TOKEN = os.getenv('BOT_TOKEN')

PROMPT_STATE = 1
MEETING_STATE = 2
MEETING_STATE_SECOND = 3


# config from config.json
try:
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    model_version = config['model_version']
    model_constant = config['model_constant']
    important_timezones = config['important_timezones']
except:
    model_version = 'gpt-4o'
    model_constant = "You are Soviet Comrad!"
    important_timezones = {
                    "America/Vancouver": "Vancouver",
                    "Europe/Zurich": "Switzerland",
                    "Israel": "Israel",
                    "Asia/Samarkand": "Samarkand",
                    "Asia/Singapore": "Bali",
                    "UTC": "UTC"
    }

def main():
    """Main"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    logging.info(f"Bot {BOT_NAME} started.")
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("current_time",
                                lambda update
                                , context: world_time_now(important_timezones, update, context)))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('picture', start_picture_command)],
        states={
            PROMPT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND
                                          , provide_picture_and_ask_prompt)],
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_acrhistator))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
