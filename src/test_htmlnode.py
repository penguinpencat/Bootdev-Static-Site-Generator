import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_eq_html_node(self):
        html1 = HTMLNode("a", "NO", None, {"href" : "aris_freear.dev", "target" : "_blank"})
        html2 = HTMLNode("a", "NO", None, {"href" : "aris_freear.dev", "target" : "_blank"})
        self.assertEqual(html1, html2)

    def test_not_eq_html_node(self):
        html1 = HTMLNode("a", "NO", None, {"href" : "aris_freear.dev", "target" : "_blank"})
        html2 = HTMLNode("a", "WHY", None, {"href" : "aris_freear.dev", "target" : "_blank"})
        self.assertNotEqual(html1, html2)

    def test_props_to_html_html_node(self):
        html1 = HTMLNode("a", "HELLO DARKNESS MY OLD FRIENDDDDDDDD", None, {"href" : "aris_freear.dev", "target" : "_blank"})
        result1 = html1.props_to_html()
        result2 = 'href="aris_freear.dev" target="_blank" '
        self.assertEqual(result1, result2)

if __name__ == "__main__":
    unittest.main()