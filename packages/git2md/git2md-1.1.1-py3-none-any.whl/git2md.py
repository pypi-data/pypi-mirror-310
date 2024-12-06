import re
import argparse
import sys
import subprocess
from pathlib import Path
from nbconvert import MarkdownExporter
from nbformat import read as nb_read, NO_CONVERT
import pymupdf4llm
import pathspec


def build_tree(
    directory: Path, tree_dict: dict, gitignore_spec=None, regex_patterns=None
):
    """Build a tree structure of the directory."""
    items = sorted(directory.iterdir())
    for item in items:
        if should_ignore(
            item.relative_to(directory), gitignore_spec, regex_patterns
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
                regex_patterns,
            )
        else:
            tree_dict[item.name] = {"path": str(item), "is_dir": False}


def format_tree(tree_dict: dict, padding=""):
    """Format the tree structure as a string."""
    lines = ""
    last_index = len(tree_dict) - 1
    for index, (name, node) in enumerate(tree_dict.items()):
        connector = "└──" if index == last_index else "├──"
        if node["is_dir"]:
            lines += f"{padding}{connector} {name}/\n"
            new_padding = padding + ("    " if index == last_index else "│   ")
            lines += format_tree(node["children"], new_padding)
        else:
            lines += f"{padding}{connector} {name}\n"
    return lines


def write_tree_to_file(
    directory: Path, output_handle, gitignore_spec=None, regex_patterns=None
):
    """Write the directory tree to the output as a Markdown code block."""
    tree_dict = {}
    build_tree(directory, tree_dict, gitignore_spec, regex_patterns)
    tree_str = format_tree(tree_dict)
    output_handle.write(f"```tree\n{tree_str.rstrip()}\n```\n\n")


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
    }
    return extension_to_language.get(file_path.suffix, "plaintext")


def should_ignore(
    file_path: Path, gitignore_spec=None, regex_patterns=None
) -> bool:
    """Check if the file should be ignored based on .gitignore and regex patterns."""
    path_str = str(file_path)

    # Always ignore .git directory and .gitignore file
    if ".git" in path_str.split("/") or file_path.name == ".gitignore":
        return True

    # Check .gitignore patterns
    if gitignore_spec:
        norm_path = path_str.replace("\\", "/")
        if file_path.is_dir():
            norm_path += "/"
        if gitignore_spec.match_file(norm_path):
            return True

    # Check regex patterns
    if regex_patterns:
        for pattern in regex_patterns:
            if re.search(pattern, path_str):
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
            f"# File: {relative_path}\n````{language}\n"
            f"{file_content}\n````\n# End of file: {relative_path}\n\n"
        )
    else:
        output_handle.write(
            f"# File: {relative_path}\n"
            f"{file_content}\n"
            f"# End of file: {relative_path}\n\n"
        )


def append_to_single_file(
    file_path: Path,
    git_path: Path,
    output_handle,
    gitignore_spec=None,
    regex_patterns=None,
):
    """Process individual files and append their content in Markdown format."""
    if should_ignore(
        file_path.relative_to(git_path), gitignore_spec, regex_patterns
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


def process_directory(
    directory: Path, output_handle, gitignore_spec=None, regex_patterns=None
):
    """Recursively process all files in a directory."""
    for file_path in directory.rglob("*"):
        if file_path.is_file():
            append_to_single_file(
                file_path,
                directory,
                output_handle,
                gitignore_spec,
                regex_patterns,
            )


def load_gitignore_patterns(directory: Path):
    """Load patterns from .gitignore and .globalignore."""
    patterns = []

    # Load .gitignore from the root directory
    gitignore_path = directory / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            patterns.extend(f.read().splitlines())

    # Load .globalignore from the script's directory
    globalignore_path = Path(__file__).parent / ".globalignore"
    if globalignore_path.exists():
        with open(globalignore_path, "r", encoding="utf-8") as f:
            patterns.extend(f.read().splitlines())

    return (
        pathspec.PathSpec.from_lines("gitwildmatch", patterns)
        if patterns
        else None
    )


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
    parser.add_argument("path", help="Path to the directory or file.")
    parser.add_argument("-o", "--output", help="Output file path.")
    parser.add_argument(
        "-rex",
        "--regex-exclude",
        nargs="*",
        default=[],
        help="List of regular expressions for excluding files or directories.",
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
                input_path, buffer, gitignore_spec, args.regex_exclude
            )
            process_directory(
                input_path, buffer, gitignore_spec, args.regex_exclude
            )
        elif input_path.is_file():
            append_to_single_file(
                input_path,
                input_path.parent,
                buffer,
                gitignore_spec,
                args.regex_exclude,
            )
        else:
            print(f"Error: Unsupported path type: {input_path}")
            sys.exit(1)

        content = buffer.getvalue()

        if args.output:
            output_file = Path(args.output)
            with output_file.open("w", encoding="utf-8") as out_fh:
                out_fh.write(content)

            if args.clipboard:
                copy_to_clipboard_content(content)
                print(f"Contents from {output_file} copied to clipboard.")
        else:
            if args.clipboard:
                copy_to_clipboard_content(content)
                print("Contents copied to clipboard.")
            else:
                print(content)

    finally:
        buffer.close()


if __name__ == "__main__":
    main()
