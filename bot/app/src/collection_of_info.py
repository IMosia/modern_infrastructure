import asyncpg
import asyncio
import os

# make it as permament connection
async def db_connect():
    return await asyncpg.connect(user=os.getenv("POSTGRES_USER"),
                                 password=os.getenv("POSTGRES_PASSWORD"),
                                 database=os.getenv("POSTGRES_DB"),
                                 port=os.getenv("POSTGRES_PORT"),
                                 host=os.getenv("DB_HOST"))


async def is_user_allowed(user_id: int) -> bool:
    conn = await db_connect()
    try:
        existing_user = await conn.fetchval("SELECT user_id FROM allowed_users WHERE user_id = $1",
                                            user_id)
        return existing_user is not None
    finally:
        await conn.close()


IMAGE_PRICE = 10.0

async def is_enough_balance_for_image(user_id: int) -> (bool, float):
    """
    Checks if the user has balance to generate an image.
    Returns a tuple (bool, float) where bool indicates if the user has enough currency,
    and float represents the current balance of the user.
    """
    conn = await db_connect()
    try:
        current_balance = await conn.fetchval("SELECT balance FROM user_balances WHERE user_id = $1", user_id)
        if current_balance is None:  # This means the user does not exist in the user_balances table
            return False, 0.0
        return current_balance >= IMAGE_PRICE, current_balance
    finally:
        await conn.close()

def collect_information_on_request(Update):
    """
    Collects information on user request
    """
    user_id = Update.message.from_user.id
    user_name = Update.message.from_user.first_name
    user_last_name = Update.message.from_user.last_name
    user_username = Update.message.from_user.username
    chat_id = Update.message.chat.id
    chat_type = Update.message.chat.type
    chat_username = Update.message.chat.username
    message_id = Update.message.message_id
    message_text = Update.message.text
    message_date = Update.message.date
    group_chat_bool = Update.message.group_chat_created

def collect_information_on_machine_response(Update):
    """
    Collects information on machine response
    """
    