import re
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(text):
    return list(
        map(
            lambda x: x.strip(),
            filter(lambda x: len(x) > 0, text.split("\n\n")),
        )
    )


def block_to_block_type(block):
    if re.match(r"#+ ", block):
        return "header"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    if all(line.startswith(">") for line in block.split("\n")):
        return "quote"
    if all(line.startswith(("* ", "- ")) for line in block.split("\n")):
        return "unordered_list"
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(block.split("\n"))):
        return "ordered_list"
    return "paragraph"


def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            children.append(LeafNode(None, node.text))
        elif node.text_type == TextType.BOLD:
            children.append(LeafNode("b", node.text))
        elif node.text_type == TextType.ITALIC:
            children.append(LeafNode("i", node.text))
        elif node.text_type == TextType.CODE:
            children.append(LeafNode("code", node.text))
        elif node.text_type == TextType.LINK:
            children.append(LeafNode("a", node.text, {"href": node.url}))
        elif node.text_type == TextType.IMAGE:
            children.append(
                LeafNode("img", node.text, {"src": node.url, "alt": node.text})
            )
    return children


def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "paragraph":
            children.append(ParentNode("p", text_to_children(block)))

        elif block_type == "header":
            level = len(block.split(" ")[0])  # Count #'s
            header_text = block[level + 1 :]  # Skip #'s and space
            children.append(ParentNode(f"h{level}", text_to_children(header_text)))

        elif block_type == "code":
            code_text = block.strip("```").strip()
            code_node = ParentNode("code", text_to_children(code_text))
            children.append(ParentNode("pre", [code_node]))

        elif block_type == "quote":
            quote_text = "\n".join(line[2:] for line in block.split("\n"))
            children.append(ParentNode("blockquote", text_to_children(quote_text)))

        elif block_type == "unordered_list":
            items = []
            for line in block.split("\n"):
                item_text = line[2:]  # Remove "* " or "- "
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(ParentNode("ul", items))

        elif block_type == "ordered_list":
            items = []
            for line in block.split("\n"):
                item_text = line[line.find(" ") + 1 :]  # Remove "1. ", "2. ", etc
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(ParentNode("ol", items))

    return ParentNode("div", children)
