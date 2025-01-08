from textnode import TextNode, TextType
from inline_markdown import markdown_to_html
import os
import shutil


def copy_content(src="static", dst="public"):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            copy_content(src_path, dst_path)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise ValueError("No h1 header found in markdown file")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)

        if os.path.isfile(src_path) and src_path.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, os.path.splitext(item)[0] + ".html")
            generate_page(src_path, template_path, dest_path)
        elif os.path.isdir(src_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            new_src_dir = os.path.join(dir_path_content, item)
            generate_pages_recursive(new_src_dir, template_path, new_dest_dir)


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_content("static", "public")

    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
