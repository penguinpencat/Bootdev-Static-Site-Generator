import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from helpers import *

class TestHelper(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )
        
    def test_split_bold(self):
        node = TextNode("This is text with a **BOLD** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://www.daddy-is-the-best.com) and another [link, who wouldda guessed it](https://https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.daddy-is-the-best.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link, who wouldda guessed it", TextType.LINK, "https://https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_extra(self):
        node = TextNode(
            "This is text with an [link](https://www.daddy-is-the-best.com) and another [link, who wouldda guessed it](https://https://www.youtube.com/@bootdotdev) to boot.dev",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.daddy-is-the-best.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link, who wouldda guessed it", TextType.LINK, "https://https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" to boot.dev", TextType.TEXT)
            ],
            new_nodes,
        )

