"""
This module contains function to collect information and communicate with the database.
"""

import os
import uuid
import json

import aiohttp
import asyncpg

from src.general_src import make_from_guid_s3_name


try:
    with open('config.json', 'r') as file:
        config = json.load(file)
    aws_region = config['aws_region']
    bucket_name = config['bucket_name']
    IMAGE_PRICE = config['image_price']
except:
    aws_region = 'ap-southeast-1'
    bucket_name = 'ai-response-pictures-danilevich-bot'
    IMAGE_PRICE = 10


MEETING_STATE_SECOND = 3


# make it as permament connection
async def db_connect():
    """Connect to the database."""
    return await asyncpg.connect(user=os.getenv("POSTGRES_USER"),
                                 password=os.getenv("POSTGRES_PASSWORD"),
                                 database=os.getenv("POSTGRES_DB"),
                                 port=os.getenv("POSTGRES_PORT"),
                                 host=os.getenv("DB_HOST"))


async def is_user_allowed(user_id: int) -> bool:
    """Check if the user is allowed to use the bot."""
    conn = await db_connect()
    try:
        existing_user = await conn.fetchval("SELECT user_id FROM allowed_users WHERE user_id = $1",
                                            user_id)
        return existing_user is not None
    finally:
        await conn.close()


async def is_enough_balance_for_image(user_id: int) -> (bool, float):
    """
    Checks if the user has balance to generate an image.
    Returns a tuple (bool, float) where bool indicates if the user has enough currency,
    and float represents the current balance of the user.
    """
    conn = await db_connect()
    try:
        current_balance = await conn.fetchval(
                            "SELECT balance FROM user_balances WHERE user_id = $1"
                            , user_id
                            )
        if current_balance is None:  # This means the user does not exist in the user_balances table
            return False, 0.0
        return current_balance >= IMAGE_PRICE, current_balance
    finally:
        await conn.close()


async def collect_information_on_request(user_id, user_inquery, inquery_type, is_athena):
    """
    Collects information on user request
    """
    # generate id as guid
    generation_id = str(uuid.uuid4())
    if is_athena:
        pass
    else:
        conn = await db_connect()
        await conn.fetchval("INSERT INTO user_requests (timestamp, user_id, generation_id, user_inquery, inquery_type) VALUES (NOW(), $1, $2, $3, $4)"
                                                , user_id, generation_id, user_inquery, inquery_type)
   
        await conn.close()
    return generation_id


async def collect_information_on_machine_response_text(generation_id, ai_response, is_athena):
    """
    Collects information on machine response for generation of text
    """
    if is_athena:
        pass
    else:
        conn = await db_connect()
        data_type = 'text'
        await conn.fetchval("INSERT INTO machine_responses (generation_id, data_type, ai_response) VALUES ($1, $2, $3)"
                                                , generation_id, data_type, ai_response)    
        await conn.close()


async def collect_information_on_machine_response_image(generation_id, link, is_athena):
    """
    Collects information on machine response for generation of pictures
    """
    data_type = 'image'
    picture_name = make_from_guid_s3_name(generation_id)
    full_s3_path = f"{bucket_name}/{picture_name}"

    url = "http://picture-uploader:5001/api/request"
    data = {
        'link': link,
        'picture_name': picture_name,
        'bucket_name': bucket_name
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    print(f"Error while uploading picture to S3: {response.status} \n {response.text}")
                else:
                    print(f"Picture {picture_name} uploaded to S3, address: {bucket_name}/{picture_name}")
                    if is_athena:
                        pass
                    else:
                        conn = await db_connect()
                        await conn.fetchval("INSERT INTO machine_responses (generation_id, data_type, ai_response) VALUES ($1, $2, $3)"
                                                                , generation_id, data_type, full_s3_path)
                        await conn.close()
    except Exception as e:
        print(f"Error while uploading picture to S3: {e}")
