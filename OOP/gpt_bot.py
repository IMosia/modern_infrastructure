from dotenv import load_dotenv
import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json

# env variables
load_dotenv()
BOT_NAME =  os.getenv('BOT_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# config from config.json
with open('config.json', 'r') as file:
    config = json.load(file)
model_version = config['model_version']
model_constant = config['model_constant']

# Init OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Define a command handler. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(f"Shalom, my name is {BOT_NAME}!")

async def message_acrhistator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ To choose what we use"""
    if update.message.text.split()[0] == 'Comrad,':
        response = client.chat.completions.create(
        model=model_version,
        messages=[
            {"role": "system", "content": model_constant},
            {"role": "user", "content": update.message.text}
        ]
        )
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response.strip())
    else:
        await update.message.reply_text(update.message.text)
    

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_acrhistator))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == '__main__':
    main()