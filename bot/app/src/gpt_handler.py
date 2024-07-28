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

import telegramify_markdown
from telegramify_markdown import customize

# Configure telegramify_markdown
customize.markdown_symbol.head_level_1 = "📌"
customize.markdown_symbol.link = "🔗"
customize.strict_markdown = True

import sys
sys.path.append('..')

from src.decorators import decorator_logging, decorator_check_if_user_is_allowed, decorator_has_enough_money_for_picture
from src.general_src import escape_markdown, split_into_chunks
from src.collection_of_info import collect_information_on_request, collect_information_on_machine_response_text, collect_information_on_machine_response_image


# config from config.json
with open('config.json', 'r') as file:
    config = json.load(file)
model_version = config['model_version']
model_constant = config['model_constant']
picture_model = config['picture_model']
picture_quality = config['picture_quality']
picture_resolution = config['picture_resolution']
tables_athena = config['tables_athena']

# env variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Init OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

@decorator_logging
@decorator_check_if_user_is_allowed
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

    user_inquery = update.message.text
    user_id = update.message.from_user.id
    response = await asyncio.get_running_loop().run_in_executor(
        None,
        lambda:  client.chat.completions.create(
        model=model_version,
        messages=[
            {"role": "system", "content": model_constant},
            {"role": "user", "content": user_inquery}
        ]
        )
    )
    ai_response = escape_markdown(response.choices[0].message.content)
    chunks_of_response = split_into_chunks(ai_response.strip())

    keep_typing.is_typing = False
    typing_task.cancel()

    for chunk in chunks_of_response:
        try:
            formatted_chunk = telegramify_markdown.markdownify(
                    chunk,
                    max_line_length=None,
                    normalize_whitespace=False
                )
            await update.message.reply_text(formatted_chunk,
                                            reply_to_message_id=update.message.message_id,
                                            parse_mode="MarkdownV2")
        except:
            # add logging here
            await update.message.reply_text(chunk
                                            , reply_to_message_id=update.message.message_id
                                            )

    # collecting information after response
    generation_id = await collect_information_on_request(user_id, user_inquery, inquery_type='text', is_athena=tables_athena)
    await collect_information_on_machine_response_text(generation_id, ai_response, is_athena=tables_athena)
    
    
@decorator_logging
@decorator_check_if_user_is_allowed
@decorator_has_enough_money_for_picture
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

    generation_id = await collect_information_on_request(update.message.from_user.id, user_prompt, inquery_type='picture', is_athena=tables_athena)

    try:
        response = await asyncio.get_running_loop().run_in_executor(
            None,
            lambda: client.images.generate(
            model=picture_model,
            prompt=user_prompt,
            n=1,
            size=picture_resolution
            )
        )
    except:
        await update.message.reply_text("Error while generating picture, violation of OpenAI policy")
        keep_upload_photo.is_upload_photo = False
        keep_upload_photo_task.cancel()
        return

    picture_url = response.data[0].url
    response = requests.get(picture_url)

    
    await update.message.reply_photo(BytesIO(response.content))

    keep_upload_photo.is_upload_photo = False
    keep_upload_photo_task.cancel()

    await collect_information_on_machine_response_image(generation_id, picture_url, is_athena=tables_athena)
    

    
