import re

def split_into_chunks(text, chunk_size=4096):
    """
    Split text into chunks of specified size.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def escape_markdown(text: str) -> str:
    """Helper function to escape telegram markup symbols."""

    escape_chars = r"\_*[]()~>#+-=|{}.!"

    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def make_from_guid_s3_name(guid: str) -> str:
    """
    Make s3 name from guid
    """
    return f"{guid}.jpg"