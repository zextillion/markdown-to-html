from htmlnode import HTMLNode
from parentnode import ParentNode
from split_delimiter import text_to_textnodes
from markdown_extractor import markdown_to_blocks, block_to_block_type
import re


def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown)
    html_node_children = []
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        match block_type:
            case "heading":
                heading_node = None
                if markdown_block.startswith("######"):
                    text_nodes = text_to_textnodes(
                        markdown_block.strip("######").strip())
                    heading_node = ParentNode(
                        "h6", text_nodes)
                elif markdown_block.startswith("#####"):
                    text_nodes = text_to_textnodes(
                        markdown_block.strip("#####").strip())
                    heading_node = ParentNode(
                        "h5", text_nodes)
                elif markdown_block.startswith("####"):
                    text_nodes = text_to_textnodes(
                        markdown_block.strip("####").strip())
                    heading_node = ParentNode(
                        "h4", text_nodes)
                elif markdown_block.startswith("###"):
                    text_nodes = text_to_textnodes(
                        markdown_block.strip("###").strip())
                    heading_node = ParentNode(
                        "h3", text_nodes)
                elif markdown_block.startswith("##"):
                    text_nodes = text_to_textnodes(
                        markdown_block.strip("##").strip())
                    heading_node = ParentNode(
                        "h2", text_nodes)
                else:
                    text_nodes = text_to_textnodes(
                        markdown_block.strip("#").strip())
                    heading_node = ParentNode(
                        "h1", text_nodes)
                html_node_children.append(heading_node)
            case "code":
                text_nodes = text_to_textnodes(markdown_block)
                code_node = ParentNode(
                    "pre", text_nodes)
                html_node_children.append(code_node)
            case "quote":
                text_nodes = text_to_textnodes(markdown_block)
                for node in text_nodes:
                    node.text = node.text.strip("> ")
                quote_node = ParentNode(
                    "blockquote", text_nodes)
                html_node_children.append(quote_node)
            case "unordered_list":
                list_item_nodes = []
                for line in markdown_block.splitlines():
                    line = line.strip("* ").strip("- ").strip()
                    text_nodes = text_to_textnodes(line)
                    list_item_node = ParentNode("li", text_nodes)
                    list_item_nodes.append(list_item_node)

                unordered_list_node = ParentNode(
                    "ul", list_item_nodes)

                html_node_children.append(unordered_list_node)
            case "ordered_list":
                list_item_nodes = []
                for line in markdown_block.splitlines():
                    line = re.sub(r"\d+. ", "", line).strip()
                    text_nodes = text_to_textnodes(line)
                    list_item_node = ParentNode("li", text_nodes)
                    list_item_nodes.append(list_item_node)

                ordered_list_node = ParentNode(
                    "ol", list_item_nodes)

                html_node_children.append(ordered_list_node)
            case "paragraph":
                text_nodes = text_to_textnodes(markdown_block)
                paragraph_node = ParentNode("p", text_nodes)
                html_node_children.append(paragraph_node)
    parent = ParentNode("div", html_node_children)
    return parent
