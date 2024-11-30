import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(TypeError):
            node = ParentNode()

        node = ParentNode("p", [])
        self.assertEqual("p", node.tag)
        self.assertEqual(None, node.value)
        self.assertEqual([], node.children)
        self.assertEqual(None, node.props)

        node = ParentNode("p", [], {"a": "https://boot.dev"})
        self.assertEqual("p", node.tag)
        self.assertEqual(None, node.value)
        self.assertEqual([], node.children)
        self.assertEqual({"a": "https://boot.dev"}, node.props)

    def test_to_html(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

        node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            node.to_html()

        child_node = LeafNode("p", "Child node value")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()

        child_node = LeafNode("p", "Child node value")
        node = ParentNode("p", [child_node])
        self.assertEqual("<p><p>Child node value</p></p>", node.to_html())

        child_node = LeafNode("p", "Child node value")
        parent_node = ParentNode("p", [child_node])
        node = ParentNode("p", [parent_node])
        self.assertEqual(
            "<p><p><p>Child node value</p></p></p>", node.to_html())

        child_node_1 = LeafNode("p", "Child node value 1")
        parent_node_1 = ParentNode("p", [child_node_1])
        child_node_2 = LeafNode("p", "Child node value 2")
        parent_node_2 = ParentNode("p", [child_node_2])
        node = ParentNode("p", [parent_node_1, parent_node_2])
        self.assertEqual(
            "<p><p><p>Child node value 1</p></p><p><p>Child node value 2</p></p></p>", node.to_html())

        child_node_1_1 = LeafNode("p", "Child node value 1-1")
        child_node_1_2 = LeafNode("p", "Child node value 1-2")
        parent_node_1 = ParentNode("p", [child_node_1_1, child_node_1_2])
        child_node_2_1 = LeafNode("p", "Child node value 2-1")
        child_node_2_2 = LeafNode("p", "Child node value 2-2")
        parent_node_2 = ParentNode("p", [child_node_2_1, child_node_2_2])
        node = ParentNode("p", [parent_node_1, parent_node_2])
        self.assertEqual(
            "<p><p><p>Child node value 1-1</p><p>Child node value 1-2</p></p><p><p>Child node value 2-1</p><p>Child node value 2-2</p></p></p>", node.to_html())
