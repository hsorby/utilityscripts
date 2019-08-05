#!/usr/local/bin/python3
import os
from shutil import copyfile


def main():
    with open("missing.txt") as f:
        lines = f.readlines()

    print(lines[0].split(' '))
    for line in lines:
        parts = line.split(' ')
        reference = parts[2]
        relative_path = reference.replace('http://localhost:5000/map/', '')
        print('copy master_transparent.png {}'.format(relative_path))
        if not os.path.isdir(os.path.dirname(relative_path)):
            print('make directory: {}'.format(os.path.dirname(relative_path)))
            os.makedirs(os.path.dirname(relative_path))
        copyfile('master_transparent.png', relative_path)


if __name__ == "__main__":
    main()

