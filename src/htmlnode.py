

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        # A String represtenting the HTML tag name
        self.tag = tag

        # A String representing the value of the HTML tag
        self.value = value

        # A List of the HTMLNode objecrs representing the children of this node
        self.children = children

        # A Dictionary of key-value pairs representing the attributes of the HTML tag, for example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props = props

    def __repr__(self):
        return (f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}")
    
    def __eq__(self, value):
        if self.tag == value.tag and self.value == value.value and self.children == value.children and self.props == value.props:
            return True
        else:
            return False

    def to_html(self):
        raise NotImplementedError("SILLY PERSON, YOU DUMB PERSON, YOU DO NOT HAVE A TO_HTML METHOD SOMEWHERE IN YOU RIDICULOUSLY LONG CODE :]")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        string = ""
        for prop in self.props:
            value = self.props[prop]
            string += (f' {prop}="{value}"')
        return string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return (f"tag = {self.tag}, value = {self.value}, props = {self.props}")

    def to_html(self):
        if self.value == None:
            raise ValueError("TEE HEE NO VALUE")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("YOU DOESNT HAS A TAG")
        if self.children == None:
            raise ValueError("NO CHILD FOR YOU")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string



# TestNode = HTMLNode("a", "HIII", None, None)
# print(TestNode)