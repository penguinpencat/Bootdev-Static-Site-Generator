

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        # A String represtenting the HTML tag name
        self.tag = tag

        # A String representing the value of the HTML tag
        self.value = value

        # A List of the HTMLNode objecrs representing the children of this node
        self.children = children

        # A Dictionary of key-value pairs representing the attributes of the HTML tag, for example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        string = ""
        for prop in self.props:
            value = self.props[prop]
            string += (f'{prop}="{value}" ')
        return string
    
    def __repr__(self):
        return (f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}")
    
    def __eq__(self, value):
        if self.tag == value.tag and self.value == value.value and self.children == value.children and self.props == value.props:
            return True
        else:
            return False



# TestNode = HTMLNode("a", "HIII", None, None)
# print(TestNode)