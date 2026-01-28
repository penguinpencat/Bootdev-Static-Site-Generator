import unittest

from main import * # Main is importing TextNode don't worry Father


class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("THIS IS BOLD TEXT", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "THIS IS BOLD TEXT")

    def test_link(self):
        node = TextNode("I AM NOT A RICK ROLL", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "I AM NOT A RICK ROLL")
        self.assertEqual(html_node.to_html(), '<a href="www.google.com">I AM NOT A RICK ROLL</a>')


    def test_img(self):
        node = TextNode("it'sa gollum", TextType.IMAGE, "www.example.com/lordoftherings/gollum.jpeg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="www.example.com/lordoftherings/gollum.jpeg" alt="it\'sa gollum"></img>')