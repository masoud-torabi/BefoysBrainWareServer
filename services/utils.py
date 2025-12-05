import re

def split_qwen_output(text: str):
    think_pattern = r"<think>(.*?)</think>"
    match = re.search(think_pattern, text, flags=re.DOTALL)

    think = ""
    response = text

    if match:
        think = match.group(1).strip()
        response = text.replace(match.group(0), "").strip()

    return think, response
