"""
Module for funciton to communicate with OpenAI
"""

from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
from io import BytesIO
import asyncio

import sys
sys.path.append('..')



# config from config.json
with open('config.json', 'r') as file:
    config = json.load(file)
model_version = config['model_version']
model_constant = config['model_constant']
picture_model = config['picture_model']
picture_quality = config['picture_quality']
picture_resolution = config['picture_resolution']

# env variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Init OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

async def message_acrhistator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Get response from GPT based on user message
    """
    async def keep_typing():
        while keep_typing.is_typing:
            try:
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                return

    keep_typing.is_typing = True
    typing_task = asyncio.create_task(keep_typing())

    response = await asyncio.get_running_loop().run_in_executor(
        None,
        lambda:  client.chat.completions.create(
        model=model_version,
        messages=[
            {"role": "system", "content": model_constant},
            {"role": "user", "content": update.message.text}
        ]
        )
    )
    ai_response = response.choices[0].message.content

    keep_typing.is_typing = False

    typing_task.cancel()
    await update.message.reply_text(ai_response.strip())
    

async def provide_picture(update: Update, context: ContextTypes.DEFAULT_TYPE, user_prompt: str):
    """
    To provide picture from GPT based on promt from user
    """
    async def keep_upload_photo():
        try:
            while keep_upload_photo.is_upload_photo:
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='upload_photo')
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            return

    keep_upload_photo.is_upload_photo = True
    keep_upload_photo_task = asyncio.create_task(keep_upload_photo())

    response = await asyncio.get_running_loop().run_in_executor(
        None,
        lambda: client.images.generate(
        model=picture_model,
        prompt=user_prompt,
        n=1,
        size=picture_resolution
        )
    )

    picture_url = response.data[0].url
    response = requests.get(picture_url)

    keep_upload_photo.is_upload_photo = False

    keep_upload_photo_task.cancel()
    await update.message.reply_photo(BytesIO(response.content))
    

    
