import unittest

from regex_help import extract_markdown_links, extract_markdown_images, block_to_block_type
from textnode import BlockType


class TestRegexHelper(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [LINK](www.more.net), and another [LINK OH MY GOD WHO COULDA BELIVED](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
        self.assertListEqual([
            ("LINK", "www.more.net"), 
            ("LINK OH MY GOD WHO COULDA BELIVED", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        ], matches)

    def test_block_to_block_type_heading(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("# There and Back Again"))

    def test_block_to_block_type_code(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("""```\nThis is some code\n```"""))

    def test_block_to_block_type_code_false(self):
        self.assertIsNot(BlockType.CODE, block_to_block_type("""```\nThis is some code\n"""))

    def test_block_to_block_type_quote(self):
        self.assertEqual(BlockType.QUOTE, block_to_block_type("> This is a quote\n> AND SO IS THIS"))

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type("- LIST\n* List\n- LISt AGAIN"))

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type("1. Eggs\n2. Milk\n3. Flour\n4. Sugar\n5. Baking powder\n6. CHOCOLATE (most important)"))

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("This is a normal paragraph, nuthin special 'bout it whatsoeva :)"))