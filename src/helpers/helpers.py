from src.classes.textnode import TextNode, TextType, BlockType
from src.classes.htmlnode import LeafNode, ParentNode
from src.helpers.regex_help import extract_markdown_images, extract_markdown_links, block_to_block_type, strip_numbers_from_start

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


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"TextNode({TextNode}) is not a valid TextType")


def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    formatted_block_strings = []
    for value in block_strings:
        value = value.strip()
        if value != '':
            formatted_block_strings.append(value)
    return(formatted_block_strings)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])
    for block in blocks:
        result = block_to_block_type(block)
        if result == BlockType.HEADING:
            original_length = len(block)
            stripped_text = block.lstrip('#')
            new_length = len(stripped_text)
            tag = f"h{original_length-new_length}"
            new_node = ParentNode(tag, [])
            stripped_text = stripped_text.lstrip(" ")
            textnodes = text_to_textnodes(stripped_text)
            for textnode in textnodes:
                htmlnode = text_node_to_html_node(textnode)
                new_node.appendChild(htmlnode)
          
        elif result == BlockType.CODE:
            lines = block.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            contents = "\n".join(lines)
            content_node = TextNode(contents, TextType.TEXT)
            content_html_node = text_node_to_html_node(content_node)
            new_node = ParentNode('pre', [])
            new_node.appendChild(ParentNode("code", [content_html_node]))
          
        elif result == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                line = line.strip().lstrip(">").strip()
                new_lines.append(line)
            
            contents = "\n".join(new_lines)
            new_node = LeafNode('blockquote', contents)
          
        elif result == BlockType.UNORDERED_LIST:
            new_node = ParentNode('ul', [])
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                line = line.strip().lstrip("*-+").strip()
                list_item = ParentNode("li", [])
                textnodes = text_to_textnodes(line)
                for textnode in textnodes:
                    htmlnode = text_node_to_html_node(textnode)
                    list_item.appendChild(htmlnode)
                new_node.appendChild(list_item)
          
        elif result == BlockType.ORDERED_LIST:
            new_node = ParentNode('ol', [])
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                line = line.strip()
                line = strip_numbers_from_start(line)
                line = line.strip()
                list_item = ParentNode("li", [])
                textnodes = text_to_textnodes(line)
                for textnode in textnodes:
                    htmlnode = text_node_to_html_node(textnode)
                    list_item.appendChild(htmlnode)
                new_node.appendChild(list_item)
          
        else:
            new_node = ParentNode('p', [])
            textnodes = text_to_textnodes(block)
            for textnode in textnodes:
                htmlnode = text_node_to_html_node(textnode)
                new_node.appendChild(htmlnode)

        parent_node.appendChild(new_node)
    return parent_node
