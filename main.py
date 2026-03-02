import os, shutil
from src.helpers.helpers import markdown_to_html_node
from src.helpers.regex_help import extract_markdown_html_title


def recursive_copy_dir(from_dir, to_dir):
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    else:
        print(f"to_dir ({to_dir}) doesn't exist. Creating now.")
    os.mkdir(to_dir)
    list_of_files = os.listdir(from_dir)
    print(f"reading contents of {from_dir}:")
    print(list_of_files)
    for file in list_of_files:
        from_path = os.path.join(from_dir, file)
        to_path = os.path.join(to_dir, file)
        if os.path.isfile(from_path):
            print(f"{from_path} is a file")
            shutil.copy(from_path, to_dir)
        else:
            print(f"{from_path} is a directory")
            recursive_copy_dir(from_path, to_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    book = open(from_path, "r")
    shelf = book.read()
    template_book = open(template_path)
    shelf_2 = template_book.read()
    # shelf and shelf_2 is a string (OF MARKDOWN) btw
    library = markdown_to_html_node(shelf) # returns a HTML Node Object !
    text = library.to_html()
    title = extract_markdown_html_title(shelf)
    shelf_2 = shelf_2.replace("{{ Title }}", title)
    shelf_2 = shelf_2.replace("{{ Content }}", text)
    dest_dir = os.path.dirname(dest_path)
    if os.path.exists(dest_dir) == False:
        os.makedirs(dest_dir)
    dest_file_obj = open(dest_path, "w")
    dest_file_obj.write(shelf_2)
    dest_file_obj.close()


def main():
    recursive_copy_dir('static', 'public')
    generate_page("./html/content/index.md", "./html/template.html", "./public/index.html")


main()

