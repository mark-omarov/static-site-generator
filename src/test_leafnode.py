import unittest
from leafnode import LeafNode


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


if __name__ == "__main__":
    unittest.main()
