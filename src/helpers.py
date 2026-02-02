from textnode import TextNode, TextType
from regex_help import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    match delimiter:
        case "`":
            delimiter_type = TextType.CODE
        case "**":
            delimiter_type = TextType.BOLD
        case "_":
            delimiter_type = TextType.ITALIC
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
        else:
            splitteded_strings = old_node.text.split(delimiter)
            if len(splitteded_strings) != 3:
                raise Exception("You haven't (ENDEDed THE DELIMITER)")
            new_list.append(TextNode(splitteded_strings[0], TextType.TEXT))
            new_list.append(TextNode(splitteded_strings[1], delimiter_type))
            new_list.append(TextNode(splitteded_strings[2], TextType.TEXT))

    return new_list


def split_nodes_image(old_nodes: list[TextNode]):
    new_list = []
    for old_node in old_nodes:
        text_to_split: str = old_node.text
        matches = extract_markdown_images(old_node.text)
        for match in matches:
            delimeter_string = f"![{match[0]}]({match[1]})"
            sections = text_to_split.split(delimeter_string, 1)
            new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text_to_split = sections[1]
        if text_to_split != "":
            new_list.append(TextNode(text_to_split, TextType.TEXT))
    return new_list


def split_nodes_link(old_nodes: list[TextNode]):
    new_list = []
    for old_node in old_nodes:
        text_to_split: str = old_node.text
        matches = extract_markdown_links(old_node.text)
        for match in matches:
            delimeter_string = f"[{match[0]}]({match[1]})"
            sections = text_to_split.split(delimeter_string, 1)
            new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(match[0], TextType.LINK, match[1]))
            text_to_split = sections[1]
        if text_to_split != "":
            new_list.append(TextNode(text_to_split, TextType.TEXT))
    return new_list
            
            


node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
print(split_nodes_link([node]))


