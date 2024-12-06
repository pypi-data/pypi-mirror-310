import os
import argparse
from pathlib import Path


def print_tree(directory, exclude_dirs=None, prefix="", level=0, max_level=None, show_size=False):
    """打印目录树结构"""
    if exclude_dirs is None:
        exclude_dirs = []

    if max_level is not None and level > max_level:
        return

    try:
        entries = list(os.scandir(directory))
    except PermissionError:
        print(f"{prefix}[访问被拒绝]")
        return

    dirs = [e for e in entries if e.is_dir()]
    files = [e for e in entries if e.is_file()]

    dirs.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())

    for i, entry in enumerate(dirs):
        if entry.name in exclude_dirs:
            continue

        is_last = (i == len(dirs) - 1 and len(files) == 0)
        branch = "└──" if is_last else "├──"
        new_prefix = prefix + "    " if is_last else prefix + "│   "

        print(f"{prefix}{branch} 📁 {entry.name}/")
        print_tree(entry.path, exclude_dirs, new_prefix, level + 1, max_level, show_size)

    for i, entry in enumerate(files):
        is_last = (i == len(files) - 1)
        branch = "└──" if is_last else "├──"

        size_info = f" ({format_size(entry.stat().st_size)})" if show_size else ""
        print(f"{prefix}{branch} 📄 {entry.name}{size_info}")


def format_size(size):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def main():
    parser = argparse.ArgumentParser(description="显示目录树结构")
    parser.add_argument('path', nargs='?', default='.', help='要显示的目录路径')
    parser.add_argument('-e', '--exclude', nargs='+', default=["langchain-env", ".git", "__pycache__", "node_modules"],
                        help='要排除的目录列表')
    parser.add_argument('-L', '--level', type=int, help='最大显示深度')
    parser.add_argument('-s', '--size', action='store_true', help='显示文件大小')

    args = parser.parse_args()

    directory = os.path.abspath(args.path)
    print(f"目录树 for {directory}")
    print("=" * 50)
    print_tree(directory, args.exclude, max_level=args.level, show_size=args.size)


if __name__ == "__main__":
    main()
