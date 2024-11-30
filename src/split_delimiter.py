from textnode import TextNode, TextType
from markdown_extractor import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    def are_delimiters_balanced(input_string, delimiter):
        # Track the count of opening and closing delimiters
        count = 0
        i = 0
        while i < len(input_string):
            # Check for the delimiter
            if input_string[i:i+len(delimiter)] == delimiter:
                count += 1
                i += len(delimiter)  # Move past the delimiter
            else:
                i += 1

        # If the count is even, the delimiters are balanced
        return count % 2 == 0

    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue

        if not are_delimiters_balanced(node.text, delimiter):
            # There is no closing delimiter
            raise ValueError(
                f"Invalid Markdown: There is no closing delimiter in {node.text}")

        split_text = node.text.split(delimiter)
        for i, t in enumerate(split_text):
            if t == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(t, TextType.TEXT))
            else:
                new_nodes.append(TextNode(t, text_type))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        cur_text = node.text
        for alt, src in matches:
            split_text = cur_text.split(f"![{alt}]({src})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, src))
            cur_text = split_text[1]

        if not cur_text is None and not cur_text == "":
            new_nodes.append(TextNode(cur_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        cur_text = node.text
        for alt, src in matches:
            split_text = cur_text.split(f"[{alt}]({src})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, src))
            cur_text = split_text[1]
        if not cur_text is None and not cur_text == "":
            new_nodes.append(TextNode(cur_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes
