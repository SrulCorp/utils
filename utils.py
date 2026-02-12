#!/usr/bin/env python3

import os
import sys
import subprocess

ROOT_DIR = r"C:/users/srulc/onedrive/documents/utils"


def find_file(root, filename):
    for dirpath, _, filenames in os.walk(root):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: utils.py <script_name> [args...]")
        sys.exit(1)

    target_name = sys.argv[1]

    if not target_name.lower().endswith(".py"):
        target_name += ".py"

    passthrough_args = sys.argv[2:]

    script_path = find_file(ROOT_DIR, target_name)

    if not script_path:
        print(f"Error: '{target_name}' not found under {ROOT_DIR}")
        sys.exit(1)

    cmd = [sys.executable, script_path] + passthrough_args

    try:
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running script: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
