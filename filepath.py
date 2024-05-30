import os
import argparse

def list_files(startpath):
    # https://stackoverflow.com/a/9728478
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def get_args():
    parser = argparse.ArgumentParser("file-test")
    parser.add_argument("directory")
    return parser.parse_args()

def main():
    args = get_args()
    list_files(args.directory)

if __name__ == "__main__":
    main()
