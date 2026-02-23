import os, shutil


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


def main():
    recursive_copy_dir('static', 'public')


main()

