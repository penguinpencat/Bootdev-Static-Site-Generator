import unittest

from src.classes.htmlnode import HTMLNode, LeafNode, ParentNode
from src.helpers.helpers import *

class TestHelper(unittest.TestCase):
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

    def test_split_links_in_front(self):
        node = TextNode(
            "[link](https://www.daddy-is-the-best.com) this is text with a link and another [link, who wouldda guessed it](https://https://www.youtube.com/@bootdotdev) to boot.dev",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.daddy-is-the-best.com"),
                TextNode(" this is text with a link and another ", TextType.TEXT),
                TextNode(
                    "link, who wouldda guessed it", TextType.LINK, "https://https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" to boot.dev", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        test_string = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(test_string)
        self.assertListEqual(
            [
                TextNode('This is ', TextType.TEXT), 
                TextNode('text', TextType.BOLD), 
                TextNode(' with an ', TextType.TEXT), 
                TextNode('italic', TextType.ITALIC), 
                TextNode(' word and a ', TextType.TEXT), 
                TextNode('code block', TextType.CODE), 
                TextNode(' and an ', TextType.TEXT), 
                TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'), 
                TextNode(' and a ', TextType.TEXT), 
                TextNode('link', TextType.LINK, 'https://boot.dev')
            ],
            result
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excess_line(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_one_block(self):
        md = """
This is **bolded** paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )


    def test_markdown_to_html_node_paragraphs(self):
            md = """
This is **bolded** paragraph 
text in a p 
tag here

This is another paragraph with _italic_ text and `code` here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph \ntext in a p \ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

    def test_markdown_to_html_node_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
            )

    def test_markdown_to_html_node_big_document(self):
        md = """
# Heading

Text paragraph
with multiple lines
and a [link](www.moo.com) inside with
some `code` and
more text afterwards

![alt text](https://image.source)

> this is
> a block
> quote

* list item 1
* list item 2

- sgds
- sdgsd

1. Ordered Item 1
2. Ordered Item 2

```
    <?php
    $variable = "string"
    var_dump($variable)
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><h1>Heading</h1><p>Text paragraph
with multiple lines
and a <a href="www.moo.com">link</a> inside with
some <code>code</code> and
more text afterwards</p><p><img src="https://image.source" alt="alt text"></img></p><blockquote>this is
a block
quote</blockquote><ul><li>list item 1</li><li>list item 2</li></ul><ul><li>sgds</li><li>sdgsd</li></ul><ol><li>Ordered Item 1</li><li>Ordered Item 2</li></ol><pre><code>    <?php
    $variable = "string"
    var_dump($variable)</code></pre></div>""",
        )