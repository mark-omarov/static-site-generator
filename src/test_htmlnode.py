import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")
        node = HTMLNode("div", "Hello, world!", props={"class": "container"})
        self.assertEqual(node.props_to_html(), 'class="container"')
        node = HTMLNode(
            "div", "Hello, world!", props={"class": "container", "id": "main"}
        )
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')


if __name__ == "__main__":
    unittest.main()
