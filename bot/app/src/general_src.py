import re

def split_into_chunks(text, chunk_size=4096):
    """
    Split text into chunks of specified size.
    """
    # TODO: add Markdown library
    chunks = []
    while len(text) > chunk_size:
        chunk = text[:chunk_size-3]
        text = text[chunk_size-3:]

        n_code_blocks = chunk.count("```")
        if n_code_blocks % 2 == 1:
            last_code_block = chunk.rfind("```")
            formating_info = chunk[last_code_block:].split(" ")[0]
            chunk += "```"
            text = f"{formating_info} {text}"

        chunks.append(chunk)
    chunks.append(text)

    return chunks


def escape_markdown(text: str) -> str:
    """Helper function to escape telegram markup symbols."""

    escape_chars = r"\_*[]()~>#+-=|{}.!"

    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def make_from_guid_s3_name(guid: str) -> str:
    """
    Make s3 name from guid
    """
    return f"{guid}.jpg"