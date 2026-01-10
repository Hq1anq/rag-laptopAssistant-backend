def getColorText(text: str, color: str) -> str:
    """
    Trả về chuỗi text có màu cho terminal.

    Args:
        color (str): Tên màu (red, green, yellow, blue, magenta, cyan, white)
        text (str): Văn bản cần tô màu

    Returns:
        str: Văn bản đã được tô màu
    """
    color_codes = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    reset_code = "\033[0m"
    color_code = color_codes.get(color.lower(), "")
    return f"{color_code}{text}{reset_code}" if color_code else text

def display_message(role, content, terminal_width=80):
    if role == 'user':
        padding = " " * (terminal_width - len(content))
        print(padding + getColorText(content, "green"))
    elif role == 'assistant':
        print(getColorText(content, "yellow"))
    elif role == 'system':
        print(getColorText(f">> {content}", "cyan"))

def display_chat_history(chat_history, terminal_width = 80):    
    for msg in chat_history:
        display_message(msg['role'], msg['content'], terminal_width)