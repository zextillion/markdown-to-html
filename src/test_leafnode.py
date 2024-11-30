import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(TypeError):
            node = LeafNode()

        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

        node = LeafNode(None, "value")
        self.assertEqual(None, node.tag)
        self.assertEqual("value", node.value)
        self.assertEqual(None, node.props)

        node = LeafNode("a", "Testing props initialization",
                        {"href": "https://boot.dev"})
        self.assertEqual("a", node.tag)
        self.assertEqual("Testing props initialization", node.value)
        self.assertEqual({"href": "https://boot.dev"}, node.props)

    def test_to_html(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

        node = LeafNode(None, "")
        self.assertEqual("", node.to_html())

        node = LeafNode("", "Test value")
        self.assertEqual("Test value", node.to_html())

        node = LeafNode(" ", "Test value 2")
        self.assertEqual("Test value 2", node.to_html())

        node = LeafNode("p", "Test value 3")
        self.assertEqual("<p>Test value 3</p>", node.to_html())

        node = LeafNode("a", "Test value 4",
                        {"href": "https://boot.dev"})
        self.assertEqual(
            "<a href=\"https://boot.dev\">Test value 4</a>", node.to_html())
