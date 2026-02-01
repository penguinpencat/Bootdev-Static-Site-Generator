import re

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


#extract_markdown_links("click [here](www.more.net) for info. I'm just joking, it's a [RICK ROLL](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
#extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")