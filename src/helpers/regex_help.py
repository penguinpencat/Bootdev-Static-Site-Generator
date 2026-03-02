import re
from src.classes.textnode import BlockType

def extract_markdown_html_title(text):
    heading = re.search(r"^#\s+(.*)$", text, re.MULTILINE)
    if heading != None:
        return heading.group(1)
    raise Exception("No title header found.")

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
    text = text.strip()
    if re.fullmatch(r"^#{1,6} .*$", text):
        return BlockType.HEADING

    elif re.fullmatch(r"^```\n[\s\S]*\n\s*```$", text):
         return BlockType.CODE
    
    elif re.fullmatch(r"^(>.*\n?)+", text):
            return BlockType.QUOTE
    
    elif re.fullmatch(r"([-*+] .*\n?)+", text):
        return BlockType.UNORDERED_LIST
    
    elif re.fullmatch(r"(\d\. .*\n?)+", text):
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH

def strip_numbers_from_start(text):
     clean_text = re.sub(r'^\d+\.\s?', '', text)
     return clean_text

#extract_markdown_links("click [here](www.more.net) for info. I'm just joking, it's a [RICK ROLL](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
#extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")