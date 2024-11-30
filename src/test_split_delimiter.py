from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType
from unittest import TestCase


class TestSplitDelimiter(TestCase):
    def test_multiple_nodes(self):
        old_text_node_1 = TextNode("test1 test2 test3", TextType.TEXT)
        old_text_node_2 = TextNode("test4 test5 test6", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [old_text_node_1, old_text_node_2], " ", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("test1", TextType.TEXT),
                TextNode("test2", TextType.TEXT),
                TextNode("test3", TextType.TEXT),
                TextNode("test4", TextType.TEXT),
                TextNode("test5", TextType.TEXT),
                TextNode("test6", TextType.TEXT),
            ], new_nodes)

    def test_old_node_types(self):
        old_text_node = TextNode("test1 test2 test3", TextType.TEXT)
        old_bold_node = TextNode("test1 test2 test3", TextType.BOLD)
        new_nodes = split_nodes_delimiter(
            [old_text_node, old_bold_node], " ", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("test1", TextType.TEXT),
                TextNode("test2", TextType.TEXT),
                TextNode("test3", TextType.TEXT),
                TextNode("test1 test2 test3", TextType.BOLD)
            ], new_nodes)

    def test_split_text(self):
        old_text_node = TextNode("test1 test2 test3", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_text_node], " ", TextType.TEXT)
        self.assertEqual(
            [
                TextNode("test1", TextType.TEXT),
                TextNode("test2", TextType.TEXT),
                TextNode("test3", TextType.TEXT)
            ], new_nodes)

    def test_bold_type(self):
        old_text_node = TextNode("This is a **bold** test", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_text_node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" test", TextType.TEXT)
            ], new_nodes)

        old_text_node = TextNode("This is a **bold test", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter(
                [old_text_node], "**", TextType.BOLD)
            self.assertEqual(
                [
                    TextNode("This is a **bold test", TextType.TEXT),
                ], new_nodes)

        old_text_node = TextNode("This is a **bold test**", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [old_text_node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold test", TextType.BOLD)
            ], new_nodes)

        old_text_node = TextNode("**bold test**", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [old_text_node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("bold test", TextType.BOLD)
            ], new_nodes)

    def test_italic_type(self):
        old_text_node = TextNode("This is an *italic* test", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [old_text_node], "*", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" test", TextType.TEXT)
            ], new_nodes)

        old_text_node = TextNode("This is an *italic test", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter(
                [old_text_node], "*", TextType.ITALIC)
            self.assertEqual(
                [
                    TextNode("This is an *italic test", TextType.TEXT),
                ], new_nodes)

        old_text_node = TextNode("*italic test*", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [old_text_node], "*", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("italic test", TextType.ITALIC),
            ], new_nodes)

    def test_code_type(self):
        old_text_node = TextNode("This is a `code` test", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [old_text_node], "`", TextType.CODE)
        self.assertEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" test", TextType.TEXT)
            ], new_nodes)

        old_text_node = TextNode("This is a `code test", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter(
                [old_text_node], "`", TextType.CODE)
            self.assertEqual(
                [
                    TextNode("This is a `code test", TextType.TEXT),
                ], new_nodes)

    def test_link_type(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK,
                         "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) + ending text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK,
                         "https://www.youtube.com/@bootdotdev"),
                TextNode(" + ending text", TextType.TEXT),
            ], new_nodes)

    def test_link_type_multiple_nodes(self):
        node_1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node_2 = TextNode(
            "New node: [node_2](https://www.boot.dev) and [node_2](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node_1, node_2])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK,
                         "https://www.youtube.com/@bootdotdev"),
                TextNode("New node: ", TextType.TEXT),
                TextNode("node_2", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("node_2", TextType.LINK,
                         "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

    def test_links_with_not_text_old_node(self):
        new_nodes = split_nodes_link([TextNode("This is text with a link ", TextType.TEXT),
                                      TextNode("to boot dev", TextType.LINK,
                                               "https://www.boot.dev"),
                                      TextNode(" and ", TextType.TEXT),
                                      TextNode("to youtube", TextType.LINK,
                                               "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK,
                         "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

    def test_image_type(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE,
                         "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) + ending text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE,
                         "https://www.youtube.com/@bootdotdev"),
                TextNode(" + ending text", TextType.TEXT),
            ], new_nodes)

    def test_image_type_multiple_nodes(self):
        node_1 = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node_2 = TextNode(
            "New node: ![node_2](https://www.boot.dev) and ![node_2](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node_1, node_2])
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE,
                         "https://www.youtube.com/@bootdotdev"),
                TextNode("New node: ", TextType.TEXT),
                TextNode("node_2", TextType.IMAGE,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("node_2", TextType.IMAGE,
                         "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

    def test_images_with_not_text_old_node(self):
        new_nodes = split_nodes_image([TextNode("This is text with an image ", TextType.TEXT),
                                      TextNode("to boot dev", TextType.IMAGE,
                                               "https://www.boot.dev"),
                                      TextNode(" and ", TextType.TEXT),
                                      TextNode("to youtube", TextType.IMAGE,
                                               "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE,
                         "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE,
                         "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

    def test_images_with_link_text(self):
        node = TextNode(
            "This is text with an image [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode(
                    "This is text with an image [to boot dev](https://www.boot.dev) and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE,
                         "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], new_nodes
        )
