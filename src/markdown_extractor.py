import re


def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.splitlines()
    blocks = []
    current_block = ""
    for line in lines:
        if line.strip() == "":
            if not current_block == "":
                blocks.append(current_block.strip())
            current_block = ""
            continue

        if not current_block == "":
            current_block += f"\n{line}"
        else:
            current_block += line

    if not current_block == "":
        blocks.append(current_block.strip())

    return blocks


def block_to_block_type(block: str) -> str:
    if len(re.findall(r"^#{1,6} .*", block)) > 0:  # Heading
        return "heading"
    elif block.startswith("```") and block.endswith("```"):  # Code
        return "code"

    lines = block.splitlines()
    quote = True
    unordered_list = True
    ordered_list = True
    ordered_list_cur_index = 1
    for line in lines:
        if not line.startswith(">"):
            quote = False
        if not line.startswith("* ") and not line.startswith("- "):
            unordered_list = False
        if not line.startswith(f"{ordered_list_cur_index}. "):
            ordered_list = False
        ordered_list_cur_index += 1

    if quote:
        return "quote"
    elif unordered_list:
        return "unordered_list"
    elif ordered_list:
        return "ordered_list"
    else:
        return "paragraph"
