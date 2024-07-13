


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
    