import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node_1 = HTMLNode()
        self.assertEqual("HTMLNode(None, None, None, None)", str(node_1))

        node_2 = HTMLNode("a")
        self.assertEqual("HTMLNode(a, None, None, None)", str(node_2))

        node_3 = HTMLNode("a", "boot.dev")
        self.assertEqual("HTMLNode(a, boot.dev, None, None)", str(node_3))

        node_4 = HTMLNode("a", "boot.dev", [node_1, node_2, node_3])
        self.assertEqual(
            f"HTMLNode(a, boot.dev, {[node_1, node_2, node_3]}, None)", str(node_4))

        props = {
            "href": "https://boot.dev",
            "target": "_blank",
        }
        node_5 = HTMLNode("a", "boot.dev", [node_4], props)
        self.assertEqual(
            f"HTMLNode(a, boot.dev, {[node_4]}, {props})", str(node_5))

    def test_props_to_html(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

        props = {
            "href": "https://boot.dev",
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, props)
        self.assertEqual(
            " href=\"https://boot.dev\" target=\"_blank\"", node.props_to_html())


if __name__ == "__main__":
    unittest.main()
