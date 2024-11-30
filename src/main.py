from os import path, listdir, mkdir
from shutil import copy, rmtree
from blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ").strip()
    raise (ValueError("No # header found in the input markdown"))


def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path} to \n\
          {dest_path} using {template_path}")
    with open(from_path) as f:
        with open(template_path) as t:
            markdown = f.read()
            html = markdown_to_html_node(markdown).to_html()

            template = t.read()
            title = extract_title(markdown)

            new_html = template.replace("{{ Title }}", title)
            new_html = new_html.replace("{{ Content }}", html)

            with open(dest_path, "w") as dest_file:
                dest_file.write(new_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> None:
    contents = listdir(dir_path_content)
    for content in contents:
        if not path.isfile(path.join(dir_path_content, content)):
            mkdir(path.join(dest_dir_path, content))
            generate_pages_recursive(path.join(
                dir_path_content, content), template_path, path.join(dest_dir_path, content.replace(".md", ".html")))
        else:
            generate_page(path.join(dir_path_content, content),
                          template_path, path.join(dest_dir_path, content.replace(".md", ".html")))


def refresh_public_directory() -> None:
    def clean_public_directory() -> None:
        if path.exists("public"):
            rmtree("public")
        mkdir("public")

    def copy_static_to_public() -> None:
        if not path.exists("public") or not path.exists("static"):
            return

        def copy_folder_contents(source_folder, destination_folder):
            if not path.exists(destination_folder):
                mkdir(destination_folder)

            contents = listdir(source_folder)
            for content in contents:
                if path.isfile(path.join(source_folder, content)):
                    copy(path.join(source_folder, content),
                         path.join(destination_folder, content))
                else:
                    copy_folder_contents(path.join(source_folder, content),
                                         path.join(destination_folder, content))

        copy_folder_contents("static", "public")

    clean_public_directory()
    copy_static_to_public()
    generate_pages_recursive(
        "content", "template.html", "public")


def main():
    refresh_public_directory()


main()
