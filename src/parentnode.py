from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag or not self.tag.split():
            raise ValueError("No tag in parent node")

        if not self.children or len(self.children) == 0:
            raise ValueError("Parent node has no children")

        child_html_string = ""
        return f"<{self.tag}{self.props_to_html()}>{child_html_string.join(child.to_html() for child in self.children)}</{self.tag}>"
