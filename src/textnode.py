from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "**BOLD**"
    ITALIC = "_italic_"
    CODE = "`code`"
    LINK = "[anchor](url)"
    IMAGE = "![alt text](url)"


class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if self.text == value.text and self.text_type == value.text_type and self.url == value.url:
            return True

    def __repr__(self):
        return f"TextNode({self.text, self.text_type.value, self.url})"
