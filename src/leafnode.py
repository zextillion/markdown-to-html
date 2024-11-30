from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if not self.tag or not self.tag.strip():
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
