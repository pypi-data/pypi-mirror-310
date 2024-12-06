import os
import argparse
from pathlib import Path
from typing import List, Optional


def show_help():
    """显示帮助信息"""
    help_text = """
DirView - 目录树显示工具

用法:
    dirview [路径] [选项]

选项:
    -h, --help          显示此帮助信息
    -e, --exclude       要排除的目录列表 (例如: -e node_modules .git)
    -L, --level         最大显示深度 (例如: -L 2)
    -s, --size          显示文件大小
    --version          显示版本信息

示例:
    dirview                     # 显示当前目录的树结构
    dirview /path/to/dir       # 显示指定目录的树结构
    dirview -s                 # 显示当前目录的树结构及文件大小
    dirview -L 2              # 只显示两层深度的目录结构
    dirview -e .git node_modules  # 排除指定目录
    """
    print(help_text)


def print_tree(directory: str,
               exclude_dirs: Optional[List[str]] = None,
               prefix: str = "",
               level: int = 0,
               max_level: Optional[int] = None,
               show_size: bool = False) -> None:
    """
    打印目录树结构

    Args:
        directory: 要显示的目录路径
        exclude_dirs: 要排除的目录列表
        prefix: 用于显示层级的前缀字符串
        level: 当前递归深度
        max_level: 最大显示深度
        show_size: 是否显示文件大小
    """
    if exclude_dirs is None:
        exclude_dirs = []

    if max_level is not None and level > max_level:
        return

    try:
        entries = list(os.scandir(directory))
    except PermissionError:
        print(f"{prefix}[访问被拒绝]")
        return
    except FileNotFoundError:
        print(f"错误: 目录 '{directory}' 不存在")
        return

    dirs = [e for e in entries if e.is_dir()]
    files = [e for e in entries if e.is_file()]

    dirs.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())

    # 计算统计信息
    total_dirs = len([d for d in dirs if d.name not in exclude_dirs])
    total_files = len(files)
    total_size = sum(f.stat().st_size for f in files) if show_size else 0

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

    # 在最顶层打印统计信息
    if level == 0:
        print("\n统计信息:")
        print(f"目录数: {total_dirs}")
        print(f"文件数: {total_files}")
        if show_size:
            print(f"总大小: {format_size(total_size)}")


def format_size(size: int) -> str:
    """
    格式化文件大小

    Args:
        size: 文件大小（字节）

    Returns:
        格式化后的大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"



def main():
    parser = argparse.ArgumentParser(
        description="显示目录树结构",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path', nargs='?', default='.', help='要显示的目录路径')
    parser.add_argument('-e', '--exclude', nargs='+', default=["langchain-env", ".git", "__pycache__", "node_modules"],
                        help='要排除的目录列表')
    parser.add_argument('-L', '--level', type=int, help='最大显示深度')
    parser.add_argument('-s', '--size', action='store_true', help='显示文件大小')
    parser.add_argument('--version', action='store_true', help='显示版本信息')

    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"DirView version {__version__}")
        return

    directory = os.path.abspath(args.path)
    print(f"目录树 for {directory}")
    print("=" * 50)
    print_tree(directory, args.exclude, max_level=args.level, show_size=args.size)



if __name__ == "__main__":
    main()
