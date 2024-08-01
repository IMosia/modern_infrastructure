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
                          , start_picture_command, start_recording_meeting)
from src.gpt_handler import message_acrhistator
from src.collection_of_info import handle_meeting_type, handle_meeting_name


# env variables
load_dotenv()
BOT_NAME =  os.getenv('BOT_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')

PROMPT_STATE = 1
MEETING_STATE = 2
MEETING_STATE_SECOND = 3

# config from config.json
with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
model_version = config['model_version']
model_constant = config['model_constant']
important_timezones = config['important_timezones']

def main():
    """Main"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    logging.info(f"Bot {BOT_NAME} started.")
#gpt_bot.py:40:4: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
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

    meeting_handler = ConversationHandler(
        entry_points=[CommandHandler('record_meeting', start_recording_meeting)],
        states={
            MEETING_STATE: [CallbackQueryHandler(handle_meeting_type)],
            MEETING_STATE_SECOND: [MessageHandler(filters.TEXT & ~filters.COMMAND
                                                  , handle_meeting_name)],
        },
        fallbacks=[]
    )
    application.add_handler(meeting_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_acrhistator))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
