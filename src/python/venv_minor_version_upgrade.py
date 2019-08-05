#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import subprocess


def usage():
    print("./venv_minor_version_upgrade.py <path-to-virtual-env>")
    print("  where <path-to-virtual-env> is the path to the virtual environment to perform a minor version upgrade on.")


def get_sym_links(directory):
    sym_links = []
    for name in os.listdir(directory):
        if name not in (os.curdir, os.pardir):
            full = os.path.join(directory, name)
            if os.path.islink(full):
                sym_links.append(full)

    return sym_links


def get_target_python_exe(base_path):
    return os.path.join(base_path, "bin", "python")


def get_python_major_minor_string(target):
    return os.readlink(target)


def get_include_path(base_path):
    target = get_target_python_exe(base_path)
    python_major_minor_string = get_python_major_minor_string(target)
    return os.path.join(base_path, "include", "{0}m".format(python_major_minor_string))


def get_module_path(base_path):
    target = get_target_python_exe(base_path)
    python_major_minor_string = get_python_major_minor_string(target)

    return os.path.join(base_path, "lib", python_major_minor_string)


def upgrade_virtual_env(base_path):
    python3_exe = shutil.which("python3")
    p = subprocess.Popen(["virtualenv", "-p", python3_exe, base_path])
    p.wait()


def main():
    args = sys.argv[:]
    if len(args) > 1:
        if platform.system() == "Darwin":
            virtual_env_path = args.pop()
            if not os.path.isabs(virtual_env_path):
                virtual_env_path = os.path.abspath(virtual_env_path)
            python_exe = get_target_python_exe(virtual_env_path)
            if os.path.isfile(python_exe):
                python_link_file = os.path.join(virtual_env_path, ".Python")
                if os.path.islink(python_link_file):
                    # print("remove .Python", python_link_file)
                    os.remove(python_link_file)

                link_file_path = get_module_path(virtual_env_path)
                for path in get_sym_links(link_file_path):
                    if os.path.islink(path):
                        # print("remove link", path)
                        os.remove(path)
                    
                include_path = get_include_path(virtual_env_path)
                if os.path.islink(include_path):
                    # print("remove include", include_path)
                    os.remove(include_path)

                upgrade_virtual_env(virtual_env_path)
                
            else:
                print("Given path is not a virtual env.")
                sys.exit(-4)

        else:
            print("Script not able to work on this platform.")
            sys.exit(-3)
    else:
        usage()
        sys.exit(-2)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print("Script requires Python 3.")
        sys.exit(-1)
    main()
