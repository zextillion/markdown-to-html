from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    HTML = "html"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    LEAF = "leaf"
    TEXT = "text"


class TextNode():
    def __init__(self, TEXT: str, TEXT_TYPE: TextType, URL: str = None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, other):
        return self.text == other.text \
            and self.text_type == other.text_type \
            and self.url == other.url

    def __repr__(self):
        if self.url == None:
            return f"TextNode({self.text}, {self.text_type.value})"
        else:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(text_node) -> LeafNode:
        leaf_node = None
        match text_node.text_type:
            case TextType.TEXT:
                leaf_node = LeafNode(None, text_node.text)
            case TextType.BOLD:
                leaf_node = LeafNode("b", text_node.text)
            case TextType.ITALIC:
                leaf_node = LeafNode("i", text_node.text)
            case TextType.CODE:
                leaf_node = LeafNode("code", text_node.text)
            case TextType.LINK:
                props = {
                    "href": text_node.url
                }
                leaf_node = LeafNode("a", text_node.text, props)
            case TextType.IMAGE:
                props = {
                    "src": text_node.url,
                    "alt": text_node.text,
                }
                leaf_node = LeafNode("img", "", props)
        return leaf_node

    def to_html(self):
        return self.text_node_to_html_node().to_html()
