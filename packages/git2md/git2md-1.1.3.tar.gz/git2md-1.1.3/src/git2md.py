from fnmatch import fnmatch
import argparse
import sys
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from nbformat import read as nb_read, NO_CONVERT
from nbconvert import MarkdownExporter
import pymupdf4llm
import pathspec


def get_language_from_extension(file_path: Path) -> str:
    """Determine the programming language from the file extension."""
    extension_to_language = {
        ".py": "python",
        ".rs": "rust",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "csharp",
        ".rb": "ruby",
        ".php": "php",
        ".json": "json",
        ".jsonc": "jsonc",
        ".xml": "xml",
        ".sh": "bash",
        ".md": "markdown",
        ".lua": "lua",
    }
    return extension_to_language.get(file_path.suffix, "plaintext")


def build_tree(
    directory: Path, tree_dict: dict, gitignore_spec=None, glob_patterns=None
):
    """Build a tree structure of the directory."""
    for item in directory.iterdir():  # Убрана сортировка для ускорения
        if should_ignore(
            item.relative_to(directory), gitignore_spec, glob_patterns
        ):
            continue
        if item.is_dir():
            tree_dict[item.name] = {
                "path": str(item),
                "is_dir": True,
                "children": {},
            }
            build_tree(
                item,
                tree_dict[item.name]["children"],
                gitignore_spec,
                glob_patterns,
            )
        else:
            tree_dict[item.name] = {"path": str(item), "is_dir": False}


def format_tree(tree_dict: dict, padding="") -> str:
    result = []
    items = list(tree_dict.items())

    for i, (name, node) in enumerate(items):
        is_last = i == len(items) - 1
        prefix = "└── " if is_last else "├── "

        result.append(
            f"{padding}{prefix}{name}{
                '/' if node['is_dir'] else ''}"
        )

        if node["is_dir"]:
            next_padding = padding + ("    " if is_last else "│   ")
            result.append(format_tree(node["children"], next_padding))

    return "\n".join(x for x in result if x)


def write_tree_to_file(
    directory: Path, output_handle, gitignore_spec=None, glob_patterns=None
):
    """Write the directory tree to the output as a Markdown code block."""
    tree_dict = {}
    build_tree(directory, tree_dict, gitignore_spec, glob_patterns)
    tree_str = format_tree(tree_dict)
    output_handle.write(f"\n```tree\n{tree_str.rstrip()}\n```\n\n")


def should_ignore(
    file_path: Path, gitignore_spec=None, glob_patterns=None
) -> bool:
    path_str = str(file_path)

    if ".git" in path_str.split("/") or file_path.name == ".gitignore":
        return True

    if gitignore_spec:
        norm_path = path_str.replace("\\", "/")
        if file_path.is_dir():
            if gitignore_spec.match_file(
                norm_path
            ) or gitignore_spec.match_file(norm_path + "/"):
                return True
        else:
            if gitignore_spec.match_file(norm_path):
                return True

    if glob_patterns:
        rel_path = str(file_path)
        for pattern in glob_patterns:
            if fnmatch(rel_path, pattern) or fnmatch(
                file_path.name, pattern.split("/")[-1]
            ):
                return True

    return False


def convert_pdf_to_markdown(pdf_path):
    """Convert a PDF file to Markdown format."""
    try:
        return pymupdf4llm.to_markdown(pdf_path)
    except Exception as e:
        print(f"Error converting PDF to Markdown: {e}")
        return None


def convert_ipynb_to_markdown(ipynb_path):
    """Convert a Jupyter Notebook to Markdown format."""
    try:
        with open(ipynb_path, "r", encoding="utf-8") as f:
            notebook = nb_read(f, as_version=NO_CONVERT)
        exporter = MarkdownExporter()
        body, _ = exporter.from_notebook_node(notebook)
        return body
    except Exception as e:
        print(f"Error converting Jupyter Notebook to Markdown: {e}")
        return None


def append_to_file_markdown_style(
    relative_path: Path, file_content: str, output_handle, language=None
) -> None:
    """Append file content to the output in Markdown format."""
    if language:
        output_handle.write(
            f"## File: {relative_path}\n````{language}\n"
            f"{file_content}\n````\n## End of file: {relative_path}\n\n"
        )
    else:
        output_handle.write(
            f"## File: {relative_path}\n"
            f"{file_content}\n"
            f"## End of file: {relative_path}\n\n"
        )


def append_to_single_file(
    file_path: Path,
    git_path: Path,
    output_handle,
    gitignore_spec=None,
    glob_patterns=None,
):
    """Process individual files and append their content in Markdown format."""
    if should_ignore(
        file_path.relative_to(git_path), gitignore_spec, glob_patterns
    ):
        return

    relative_path = file_path.relative_to(git_path)
    try:
        # Handle pre-processed files (e.g., PDF, ipynb)
        if file_path.suffix in [".pdf", ".ipynb"]:
            preprocessors = {
                ".pdf": convert_pdf_to_markdown,
                ".ipynb": convert_ipynb_to_markdown,
            }
            md_content = preprocessors[file_path.suffix](file_path)
            if md_content:
                append_to_file_markdown_style(
                    relative_path, md_content, output_handle
                )
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            language = get_language_from_extension(file_path)
            append_to_file_markdown_style(
                relative_path, file_content, output_handle, language=language
            )
    except UnicodeDecodeError:
        print(f"Warning: Could not decode {file_path}. Skipping.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def process_directory_parallel(
    directory: Path, output_handle, gitignore_spec=None, glob_patterns=None
):
    """Process all files in a directory using multithreading."""
    with ThreadPoolExecutor() as executor:
        futures = []
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                futures.append(
                    executor.submit(
                        append_to_single_file,
                        file_path,
                        directory,
                        output_handle,
                        gitignore_spec,
                        glob_patterns,
                    )
                )
        for future in futures:
            future.result()  # Ожидаем завершения всех задач


def load_gitignore_patterns(directory: Path):
    """Load patterns from .gitignore and .globalignore."""
    patterns = []

    # Load .gitignore from the root directory
    gitignore_path = directory / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            git_patterns = f.read().splitlines()
            patterns.extend(git_patterns)

    # Load .globalignore from the script's directory
    globalignore_path = Path(__file__).parent / ".globalignore"
    if globalignore_path.exists():
        with open(globalignore_path, "r", encoding="utf-8") as f:
            global_patterns = f.read().splitlines()
            patterns.extend(global_patterns)

    if not patterns:
        return None

    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def copy_to_clipboard_content(content: str) -> None:
    """Copy the given content to the clipboard using wl-copy."""
    try:
        process = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE)
        process.communicate(input=content.encode("utf-8"))
    except FileNotFoundError:
        print("Clipboard functionality requires 'wl-copy' to be installed.")
    except ValueError as e:
        print(f"Error copying to clipboard: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert files to Markdown.")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the directory or file (default: current directory).",
    )
    parser.add_argument("-o", "--output", help="Output file path.")
    parser.add_argument(
        "-gexc",
        "--glob-exclude",
        nargs="*",
        default=[],
        help="List of glob patterns for excluding files or directories (e.g., '*.log' '*.tmp').",
    )
    parser.add_argument(
        "-se",
        "--skip-empty-files",
        action="store_true",
        help="Skip empty files.",
    )
    parser.add_argument(
        "-cp",
        "--clipboard",
        action="store_true",
        help="Copy the output file content to clipboard.",
    )
    parser.add_argument(
        "-igi",
        "--ignore-gitignore",
        action="store_true",
        help="Ignore .gitignore and .globalignore files.",
    )

    args = parser.parse_args()
    input_path = Path(args.path)

    if not input_path.exists():
        print(f"Error: Path not found: {input_path}")
        sys.exit(1)

    # Load .gitignore and .globalignore patterns unless ignored by the user
    gitignore_spec = (
        None if args.ignore_gitignore else load_gitignore_patterns(input_path)
    )

    import io

    buffer = io.StringIO()

    try:
        if input_path.is_dir():
            write_tree_to_file(
                input_path, buffer, gitignore_spec, args.glob_exclude
            )
            for file_path in input_path.rglob("*"):
                if file_path.is_file():
                    append_to_single_file(
                        file_path,
                        input_path,
                        buffer,
                        gitignore_spec,
                        args.glob_exclude,
                    )
        elif input_path.is_file():
            append_to_single_file(
                input_path,
                input_path.parent,
                buffer,
                gitignore_spec,
                args.glob_exclude,
            )
        else:
            print(f"Error: Unsupported path type: {input_path}")
            sys.exit(1)

        content = buffer.getvalue()

        if args.output:
            with Path(args.output).open("w", encoding="utf-8") as out_fh:
                out_fh.write(content)
            print(f"Contents saved to {args.output}.")
        elif args.clipboard:
            copy_to_clipboard_content(content)
            print("Contents copied to clipboard.")
        else:
            print(content)

    finally:
        buffer.close()


if __name__ == "__main__":
    main()
