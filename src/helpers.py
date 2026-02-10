from textnode import TextNode, TextType
from regex_help import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Splitting a list of nodes by a specific markdown delimeter

    Args:
        old_nodes (list[TextNode]): The list of TextNodes to split
        delimiter (str): The markdown delimeter to split on e.g("**", "_", "`")
        text_type (TextType): The TextType enum of the delimeter

    Raises:
        Exception: Raises a ValueError if a delimeter isn't closed

    Returns:
        list[TextNode]: A list of nodes containing TextNodes for each split section
    """
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue
        split_nodes = []
        splitteded_strings = old_node.text.split(delimiter)
        if len(splitteded_strings) % 2 == 0:
            raise ValueError("You haven't (ENDEDed THE DELIMITER)")
        for i in range(len(splitteded_strings)):
            if splitteded_strings[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(splitteded_strings[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(splitteded_strings[i], text_type))
        new_list.extend(split_nodes)
    return new_list


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue # rerun
        text_to_split: str = old_node.text
        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_list.append(old_node)
            continue # rerun
        for match in matches:
            delimeter_string = f"![{match[0]}]({match[1]})"
            sections = text_to_split.split(delimeter_string, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed (tut tut)")
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text_to_split = sections[1]
        if text_to_split != "":
            new_list.append(TextNode(text_to_split, TextType.TEXT))
    return new_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue # rerun
        text_to_split: str = old_node.text
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_list.append(old_node)
            continue # rerun
        for match in matches:
            delimeter_string = f"[{match[0]}]({match[1]})"
            sections = text_to_split.split(delimeter_string, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed (tut tut)")
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(match[0], TextType.LINK, match[1]))
            text_to_split = sections[1]
        if text_to_split != "":
            new_list.append(TextNode(text_to_split, TextType.TEXT))
    return new_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,'**',TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,'_',TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,'`',TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    formatted_block_strings = []
    for value in block_strings:
        value = value.strip()
        if value != '':
            formatted_block_strings.append(value)
    return(formatted_block_strings)

