from unittest import TestCase
from parentnode import ParentNode
from textnode import TextNode, TextType
from blocks import markdown_to_html_node
from leafnode import LeafNode


class TestBlocks(TestCase):
    def test_headers(self):
        text_node = TextNode("Header", TextType.TEXT)
        heading_node = ParentNode("h1", [text_node])
        top_node = ParentNode("div", [heading_node])
        self.assertEqual(str(top_node), str(markdown_to_html_node("# Header")))

        text_node = TextNode("Header", TextType.TEXT)
        heading_node = ParentNode("h2", [text_node])
        top_node = ParentNode("div", [heading_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("## Header")))

        text_node = TextNode("Header", TextType.TEXT)
        heading_node = ParentNode("h3", [text_node])
        top_node = ParentNode("div", [heading_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("### Header")))

        text_node = TextNode("Header", TextType.TEXT)
        heading_node = ParentNode("h4", [text_node])
        top_node = ParentNode("div", [heading_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("#### Header")))

        text_node = TextNode("Header", TextType.TEXT)
        heading_node = ParentNode("h5", [text_node])
        top_node = ParentNode("div", [heading_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("##### Header")))

        text_node = TextNode("Header", TextType.TEXT)
        heading_node = ParentNode("h6", [text_node])
        top_node = ParentNode("div", [heading_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("###### Header")))

    def test_nested_text_types(self):
        heading_node = ParentNode("h1", [TextNode("Header ", TextType.TEXT),
                                         TextNode("italics", TextType.ITALIC),
                                         TextNode(" ", TextType.TEXT),
                                         TextNode("bold", TextType.BOLD),
                                         ])
        top_node = ParentNode("div", [heading_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("# Header _italics_ **bold**")))

    def test_paragraph(self):
        p_node = ParentNode("p", [TextNode("Paragraph", TextType.TEXT)])
        top_node = ParentNode("div", [p_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("Paragraph")))

        p_node = ParentNode("p", [TextNode("2. A", TextType.TEXT)])
        top_node = ParentNode("div", [p_node])
        self.assertEqual(str(top_node), str(
            markdown_to_html_node("2. A")))

    def test_unordered_list(self):
        li_1_node = ParentNode("li", [TextNode("List item", TextType.TEXT)])
        li_2_node = ParentNode("li", [TextNode("List item", TextType.TEXT)])
        ul_node = ParentNode("ul", [li_1_node, li_2_node])
        top_node = ParentNode("div", [ul_node])

        markdown_str = ""
        markdown_str += "\n- List item"
        markdown_str += "\n- List item"
        self.assertEqual(str(top_node), str(
            markdown_to_html_node(markdown_str)))

        markdown_str = ""
        markdown_str += "\n* List item"
        markdown_str += "\n* List item"
        self.assertEqual(str(top_node), str(
            markdown_to_html_node(markdown_str)))

        p_node = ParentNode("p", [TextNode(
            "List item\n", TextType.ITALIC), TextNode("List item", TextType.TEXT)])
        top_node = ParentNode("div", [p_node])

        markdown_str = ""
        markdown_str += "*List item"
        markdown_str += "\n*List item"
        self.assertEqual(str(top_node), str(
            markdown_to_html_node(markdown_str)))

        markdown_str = ""
        markdown_str += "\n*List item"
        markdown_str += "\n*List item"
        self.assertEqual(str(top_node), str(
            markdown_to_html_node(markdown_str)))

    def test_ordered_list(self):
        li_1_node = ParentNode(
            "li", [TextNode("List item", TextType.TEXT)])
        li_2_node = ParentNode("li", [TextNode("List item", TextType.TEXT)])
        ol_node = ParentNode("ol", [li_1_node, li_2_node])
        top_node = ParentNode("div", [ol_node])

        markdown_str = ""
        markdown_str += "1. List item"
        markdown_str += "\n2. List item"
        self.assertEqual(str(top_node), str(
            markdown_to_html_node(markdown_str)))

    def test_multiple(self):
        heading_node = ParentNode("h1", [TextNode("Header", TextType.TEXT)])
        p_node = ParentNode("p", [TextNode("Paragraph", TextType.TEXT)])
        li_1_node = ParentNode("li", [TextNode("List item", TextType.TEXT)])
        li_2_node = ParentNode("li", [TextNode("List item", TextType.TEXT)])
        ul_node = ParentNode("ul", [li_1_node, li_2_node])
        link_node = TextNode("link text", TextType.LINK,
                             "link url")
        link_parent_node = ParentNode("p", [link_node])
        image_node = TextNode("image alt text", TextType.IMAGE,
                              "image url")
        image_parent_node = ParentNode("p", [image_node])
        italics_node = ParentNode(
            "p", [TextNode("italics text", TextType.ITALIC)])
        bold_node = ParentNode("p", [TextNode("bold text", TextType.BOLD)])
        top_node = ParentNode("div", [
            heading_node, p_node, ul_node, link_parent_node, image_parent_node, italics_node, bold_node])

        markdown_str = ""
        markdown_str += "# Header"
        markdown_str += "\n"
        markdown_str += "\nParagraph"
        markdown_str += "\n"
        markdown_str += "\n- List item"
        markdown_str += "\n- List item"
        markdown_str += "\n"
        markdown_str += "\n[link text](link url)"
        markdown_str += "\n"
        markdown_str += "\n![image alt text](image url)"
        markdown_str += "\n"
        markdown_str += "\n_italics text_"
        markdown_str += "\n"
        markdown_str += "\n**bold text**"

        self.assertEqual(str(top_node), str(
            markdown_to_html_node(markdown_str)))

    def test_quote(self):
        p_node = ParentNode(
            "blockquote", [TextNode("Quote", TextType.TEXT)])
        top_node = ParentNode("div", [p_node])

        markdown_str = "> Quote"
        self.assertEqual(str(top_node), str(
            markdown_to_html_node(markdown_str)))
