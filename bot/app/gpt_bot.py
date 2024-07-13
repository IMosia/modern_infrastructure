from dotenv import load_dotenv
import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, Updater, ConversationHandler, CallbackContext
import json
import logging

from src.commands import start, world_time_now, provide_picture_and_ask_prompt
from src.gpt_handler import message_acrhistator
from src.decorators import decorator_logging

# env variables
load_dotenv()
BOT_NAME =  os.getenv('BOT_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')

PROMPT_STATE = 1

async def start_picture_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Please provide a prompt for the picture.")
    return PROMPT_STATE

# config from config.json
with open('config.json', 'r') as file:
    config = json.load(file)
model_version = config['model_version']
model_constant = config['model_constant']
important_timezones = config['important_timezones']

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    logging.info(f"Bot {BOT_NAME} started.")

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("current_time",
                                            lambda update, context: world_time_now(important_timezones, update, context)))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('picture', start_picture_command)],
        states={
            PROMPT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, provide_picture_and_ask_prompt)],
        },
        fallbacks=[]
    )
    application.add_handler(conv_handler)

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_acrhistator))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    
if __name__ == '__main__':
    main()