"""
This is orchestrator for telegram bot commands and communication
"""

import os
import json
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler, filters
                          , ConversationHandler)

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
with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
model_version = config['model_version']
model_constant = config['model_constant']
important_timezones = config['important_timezones']


def main():
    """
    Main
    Bot logic
    """
    application = Application.builder().token(BOT_TOKEN).build()
    logging.info(f"Bot {BOT_NAME} started.")


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

    if os.getenv("WEBHOOK_ENABLED", "False").lower() == "true":
        logger.info("Starting webhook mode.")
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("WEBHOOK_PORT", "8443")),
            secret_token=os.getenv("WEB_HOOK_SECRET_TOKEN"),
            allowed_updates=Update.ALL_TYPES,
            webhook_url=os.getenv("WEBHOOK_URL"),
        )
    else:
        logger.info("Starting polling mode.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
