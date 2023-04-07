from text_type import TextType
import re


def __check_url(text: str) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    result = re.match(regex, text)

    return result != None


def categorize_texts(texts: list[str]) -> dict:
    result: dict = {}

    for text in texts:

        if len(text) == 10 and text.isdigit():
            result[text] = str(TextType.NUMBER)

        elif re.match('[^@]+@[^@]+\.[^@]+', text) is not None:
            result[text] = str(TextType.EMAIL)

        elif __check_url(text):
            result[text] = str(TextType.URL)

        else:
            result[text] = str(TextType.PLAIN_TEXT)

    return result
