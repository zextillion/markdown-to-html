import unittest
from markdown_extractor import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type


class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(2, len(matches))
        self.assertEqual(
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), matches[0])
        self.assertEqual(
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"), matches[1])

        text = "No values: ![]()"
        matches = extract_markdown_images(text)
        self.assertEqual(1, len(matches))
        self.assertEqual(
            ("", ""), matches[0])

        text = "No match"
        matches = extract_markdown_images(text)
        self.assertEqual(0, len(matches))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(2, len(matches))
        self.assertEqual(
            ("to boot dev", "https://www.boot.dev"), matches[0])
        self.assertEqual(
            ("to youtube", "https://www.youtube.com/@bootdotdev"), matches[1])

        text = "No values: []()"
        matches = extract_markdown_links(text)
        self.assertEqual(1, len(matches))
        self.assertEqual(
            ("", ""), matches[0])

        text = "No match"
        matches = extract_markdown_links(text)
        self.assertEqual(0, len(matches))

    def test_extract_markdown_links_with_image_syntax(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(text)
        self.assertEqual(0, len(matches))

    def test_markdown_to_blocks(self):
        markdown_str = "# This is a heading"
        markdown_str += "\n"
        markdown_str += "\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it."
        markdown_str += "\n"
        markdown_str += "\n* This is the first list item in a list block"
        markdown_str += "\n* This is a list item"
        markdown_str += "\n* This is another list item"

        list = markdown_to_blocks(markdown_str)

        correctOutput = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(correctOutput, list)

    def test_markdown_to_blocks_empty_spaces(self):
        markdown_str = "# This is a heading"
        markdown_str += "\n"
        markdown_str += "\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it."
        markdown_str += "\n"
        markdown_str += "\n* This is the first list item in a list block"
        markdown_str += "\n* This is a list item"
        markdown_str += "\n"
        markdown_str += "\n* This is another list item"

        list = markdown_to_blocks(markdown_str)

        correctOutput = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item",
            "* This is another list item",
        ]
        self.assertEqual(correctOutput, list)

    def test_markdown_to_blocks_whitespace(self):
        markdown_str = "# This is a heading"
        markdown_str += "\n"
        markdown_str += "\n  This is a paragraph of text. It has some **bold** and *italic* words inside of it.  "
        markdown_str += "\n"
        markdown_str += "\n * This is the first list item in a list block"
        markdown_str += " \n * This is a list item "
        markdown_str += "\n"
        markdown_str += " \n* This is another list item  "

        list = markdown_to_blocks(markdown_str)

        correctOutput = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block \n * This is a list item",
            "* This is another list item",
        ]
        self.assertEqual(correctOutput, list)

    def test_block_to_block_type_heading(self):
        self.assertEqual("heading", block_to_block_type("# This is a heading"))
        self.assertEqual("heading", block_to_block_type(
            "## This is a heading"))
        self.assertEqual("heading", block_to_block_type(
            "### This is a heading"))
        self.assertEqual("heading", block_to_block_type(
            "#### This is a heading"))
        self.assertEqual("heading", block_to_block_type(
            "##### This is a heading"))
        self.assertEqual("heading", block_to_block_type(
            "###### This is a heading"))
        self.assertEqual("paragraph", block_to_block_type(
            "####### This is not a heading"))
        self.assertEqual("paragraph", block_to_block_type(
            "#This is not a heading"))

    def test_block_to_block_type_code(self):
        self.assertEqual("code", block_to_block_type("```Code```"))

    def test_block_to_block_type_quote(self):
        self.assertEqual("quote", block_to_block_type(">quote"))
        self.assertEqual("quote", block_to_block_type(">quote\n>quote"))
        self.assertEqual("paragraph", block_to_block_type(">quote\nnot quote"))

    def test_block_to_block_type_unordered_list_no_space(self):
        self.assertEqual("paragraph", block_to_block_type("*list item"))
        self.assertEqual("paragraph",
                         block_to_block_type("*list item\n*list item"))
        self.assertEqual("paragraph", block_to_block_type("-list item"))
        self.assertEqual("paragraph",
                         block_to_block_type("-list item\n-list item"))
        self.assertEqual("paragraph",
                         block_to_block_type("*list item\n-list item"))
        self.assertEqual("paragraph",
                         block_to_block_type("-list item\n*list item"))
        self.assertEqual(
            "paragraph", block_to_block_type(">quote\n*list item"))

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual("unordered_list", block_to_block_type("* list item"))
        self.assertEqual("unordered_list",
                         block_to_block_type("* list item\n* list item"))
        self.assertEqual("unordered_list", block_to_block_type("- list item"))
        self.assertEqual("unordered_list",
                         block_to_block_type("- list item\n- list item"))
        self.assertEqual("unordered_list",
                         block_to_block_type("* list item\n- list item"))
        self.assertEqual("unordered_list",
                         block_to_block_type("- list item\n* list item"))
        self.assertEqual(
            "paragraph", block_to_block_type(">quote\n* list item"))

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual("ordered_list", block_to_block_type("1. list item"))
        self.assertEqual("ordered_list", block_to_block_type(
            "1. list item\n2. list item"))
        self.assertEqual("ordered_list", block_to_block_type(
            "1. list item\n2. list item\n3. list item"))
        self.assertEqual("paragraph", block_to_block_type(
            "1. list item\n 2. list item"))
        self.assertEqual("paragraph", block_to_block_type(
            "2. list item\n3. list item"))
        self.assertEqual("paragraph", block_to_block_type(
            "0. list item\n"))
        self.assertEqual("paragraph", block_to_block_type(
            "0. list item\n1. list item"))
        self.assertEqual("paragraph", block_to_block_type(
            "1.list item"))
