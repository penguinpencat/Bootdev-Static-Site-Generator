from textnode import TextNode, TextType

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
                raise Exception("You haven't (ENDED THE DELIMITER)")
            new_list.append(TextNode(splitteded_strings[0], TextType.TEXT))
            new_list.append(TextNode(splitteded_strings[1], delimiter_type))
            new_list.append(TextNode(splitteded_strings[2], TextType.TEXT))

    return new_list
