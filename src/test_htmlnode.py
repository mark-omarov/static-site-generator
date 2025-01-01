import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType


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


class TestParentNode(unittest.TestCase):
    def test_parentnode(self):
        parent = ParentNode(None, None)
        with self.assertRaises(ValueError):
            parent.to_html()
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()
        parent = ParentNode("div", [LeafNode("span", "Hello")])
        self.assertEqual(parent.to_html(), "<div><span>Hello</span></div>")
        parent = ParentNode("div", [LeafNode("span", "Hello")], {"class": "container"})
        self.assertEqual(
            parent.to_html(), '<div class="container"><span>Hello</span></div>'
        )
        parent = ParentNode(
            "div",
            [
                LeafNode("span", "Hello"),
                ParentNode("div", [LeafNode("span", "World")]),
            ],
            {"class": "container"},
        )
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>Hello</span><div><span>World</span></div></div>',
        )


class TestLeafNode(unittest.TestCase):
    def test_leafnode(self):
        leaf = LeafNode("p", "Hello, World!")
        self.assertEqual(leaf.to_html(), "<p>Hello, World!</p>")
        leaf = LeafNode(None, "Hello, World!")
        self.assertEqual(leaf.to_html(), "Hello, World!")
        leaf = LeafNode("p", "Hello, World!", {"class": "text"})
        self.assertEqual(leaf.to_html(), '<p class="text">Hello, World!</p>')
        leaf = LeafNode(None, "Hello, World!", {"class": "text"})
        self.assertEqual(leaf.to_html(), "Hello, World!")
        leaf = LeafNode(None, "")
        with self.assertRaises(ValueError):
            leaf.to_html()


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        with self.assertRaises(Exception):
            text_node_to_html_node(TextNode("Hello, World!", "unknown"))
        html_node = text_node_to_html_node(TextNode("Hello, World!", TextType.NORMAL))
        self.assertEqual(repr(html_node), repr(LeafNode(None, "Hello, World!")))
        html_node = text_node_to_html_node(TextNode("Hello, World!", TextType.BOLD))
        self.assertEqual(repr(html_node), repr(LeafNode("b", "Hello, World!")))
        html_node = text_node_to_html_node(TextNode("Hello, World!", TextType.ITALIC))
        self.assertEqual(repr(html_node), repr(LeafNode("i", "Hello, World!")))
        html_node = text_node_to_html_node(TextNode("Hello, World!", TextType.CODE))
        self.assertEqual(repr(html_node), repr(LeafNode("code", "Hello, World!")))
        html_node = text_node_to_html_node(
            TextNode("Hello, World!", TextType.LINK, "https://example.com")
        )
        self.assertEqual(
            repr(html_node),
            repr(LeafNode("a", "Hello, World!", {"href": "https://example.com"})),
        )
        html_node = text_node_to_html_node(
            TextNode("Hello, World!", TextType.IMAGE, "https://example.com")
        )
        self.assertEqual(
            repr(html_node),
            repr(
                LeafNode(
                    "img", "", {"src": "https://example.com", "alt": "Hello, World!"}
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()
