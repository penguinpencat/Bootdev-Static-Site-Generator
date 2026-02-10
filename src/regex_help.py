import re
from textnode import BlockType

def extract_markdown_links(text):
    tuples = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    tuples.extend(matches)
    return tuples

def extract_markdown_images(text):
    tuples = []
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    tuples.extend(matches)
    return tuples

def block_to_block_type(text):
    if re.fullmatch(r"^# .*$", text):
        return BlockType.HEADING

    elif re.fullmatch(r"^```\n[\s\S]*\n```$", text):
         return BlockType.CODE
    
    elif re.fullmatch(r"^(>.*\n?)+", text):
            return BlockType.QUOTE
    
    elif re.fullmatch(r"([-*] .*\n?)+", text):
        return BlockType.UNORDERED_LIST
    
    elif re.fullmatch(r"(\d\. .*\n?)+", text):
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH
    
#extract_markdown_links("click [here](www.more.net) for info. I'm just joking, it's a [RICK ROLL](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
#extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")