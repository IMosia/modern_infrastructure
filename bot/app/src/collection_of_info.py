import asyncpg
import asyncio
import os
from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update

MEETING_STATE_SECOND = 3
IMAGE_PRICE = 10.0

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


async def handle_meeting_type(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    meeting_type = str(query.data)
    context.user_data['meeting_type'] = meeting_type
    await query.edit_message_text(f"So, with whom:")
    return MEETING_STATE_SECOND


async def handle_meeting_name(update: Update, context: CallbackContext):
    meeting_type = context.user_data.get('meeting_type')

    people_names_list = get_peoples_names()

    # choose out of many
    


    conn = await db_connect()
    await conn.execute("INSERT INTO feedback (timestamp, meeting_tyoe, person_name) VALUES (NOW(), $1, $2)"
                        , meeting_type, person_name)
    await conn.close()


    return ConversationHandler.END


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
    