import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("test1", TextType.TEXT)
        node2 = TextNode("test1", TextType.TEXT)
        self.assertEqual(node, node2)

        node = TextNode("test2", TextType.BOLD)
        node2 = TextNode("test2", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("test3", TextType.TEXT, "https://boot.dev")
        node2 = TextNode("test3", TextType.TEXT, "https://boot.dev")
        self.assertEqual(node, node2)

        node = TextNode("test4", TextType.TEXT)
        node2 = TextNode("test4", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("test1", TextType.TEXT)
        node2 = TextNode("test1-not eq", TextType.TEXT)
        self.assertNotEqual(node, node2)

        node = TextNode("test2", TextType.TEXT)
        node2 = TextNode("test2", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("test3", TextType.TEXT, "https://boot.dev")
        node2 = TextNode("test3", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("test1", TextType.TEXT)
        self.assertEqual("TextNode(test1, text)", str(node))

        node = TextNode("test2", TextType.TEXT, "https://boot.dev")
        self.assertEqual("TextNode(test2, text, https://boot.dev)", str(node))

    def test_text_node_to_html_node(self):
        text_node = TextNode(None, None)
        with self.assertRaises(AttributeError):
            leaf_node = text_node.text_node_to_html_node()
            leaf_node.to_html()

        text_node = TextNode("", TextType.TEXT)
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual("", leaf_node.to_html())

        text_node = TextNode("text value", TextType.TEXT)
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual("text value", leaf_node.to_html())

        text_node = TextNode("text value", TextType.BOLD)
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual("<b>text value</b>", leaf_node.to_html())

        text_node = TextNode("text value", TextType.ITALIC)
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual("<i>text value</i>", leaf_node.to_html())

        text_node = TextNode("text value", TextType.CODE)
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual("<code>text value</code>", leaf_node.to_html())

        text_node = TextNode("text value", TextType.LINK)
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual("<a href=\"None\">text value</a>",
                         leaf_node.to_html())

        text_node = TextNode("text value", TextType.LINK, "https://boot.dev")
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual(
            "<a href=\"https://boot.dev\">text value</a>", leaf_node.to_html())

        text_node = TextNode("text value", TextType.IMAGE, "https://boot.dev")
        leaf_node = text_node.text_node_to_html_node()
        self.assertEqual(
            "<img src=\"https://boot.dev\" alt=\"text value\"></img>", leaf_node.to_html())


if __name__ == "__main__":
    unittest.main()
