import os, shutil, pathlib, sys
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


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}") # Doing a print line to ensure the user understands what the function is doing
    book = open(from_path, "r") # Creating a pointer to the markdown file
    shelf = book.read() # Reading the markdown file and returning the contents
    template_book = open(template_path) # Creating a pointer to the template HTML file
    shelf_2 = template_book.read() # Reading the template HTML file and returning the contents
    # shelf and shelf_2 is a string (OF MARKDOWN) btw
    library = markdown_to_html_node(shelf) # Converting the contents of our markdown file into a HTML Node Object
    text = library.to_html() # Converting the HTML Node object into a raw HTML string
    title = extract_markdown_html_title(shelf) # Finding and returning the heading of the markdown file
    shelf_2 = shelf_2.replace("{{ Title }}", title) # Replacing the placeholder "{{ Title }}" with the HTML title in the template file
    shelf_2 = shelf_2.replace("{{ Content }}", text) # Replacing the placeholder "{{ Content }}" with the HTML content in the template file
    shelf_2 = shelf_2.replace('href="/', f'href="{basepath}')
    shelf_2 = shelf_2.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path) # Finding and returning the destination directory path
    if os.path.exists(dest_dir) == False: # This if statment checks to see if the path exists, if it doesn't it creates it
        print(f"Path to destination directory doesn't exist. Creating ({dest_dir}) now...")
        os.makedirs(dest_dir)
    dest_file_obj = open(dest_path, "w") # Creating a 'write' pointer to the destination path
    dest_file_obj.write(shelf_2) # Writing over the destination file with it's HTML file
    dest_file_obj.close() # Closing the file to ensure that it saves

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content) != True: # Checking if the content path doesn't exist
        raise Exception(f"Content directory ({dir_path_content}) does not exist") # Raising an Exception if it doesn't exist
    print(f"Generating pages from {dir_path_content}") # Prints a helpful message to help the user understand whats going on
    contents = os.listdir(dir_path_content) # Creating a contents variable that is the contents of the directory path file
    for item in contents: # Looping through each "item" in contents and adding the item to a "from path" variable
        from_path = os.path.join(dir_path_content, item)
        if os.path.isfile(from_path): # Checking if the from path is a file
            filename = pathlib.Path(item).stem # Removing the extension from the file name
            to_path = os.path.join(dest_dir_path, f"{filename}.html") # Creating the full path to the destination file
            print(f"Generating page: {from_path} > {to_path}")
            generate_page(from_path, template_path, to_path, basepath) # Generating the page using the generate_page function
        else: # Otherwise, it's a directory
            to_path = os.path.join(dest_dir_path, item) # Changing the to path to point to the new directory
            generate_pages_recursive(from_path, template_path, to_path, basepath) # Recursivly calling generate_pages_recursive on the new to_path

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(f"Basepath is {basepath}")
    recursive_copy_dir('static', 'docs')
    generate_pages_recursive("content", "html/template.html", "docs", basepath)
    # generate_page("./content/index.md", "./html/template.html", "./public/index.html")


main()

