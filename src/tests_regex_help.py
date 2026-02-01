import unittest

from regex_help import extract_markdown_links, extract_markdown_images


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
