# git2md

A command-line tool for converting Git repository contents to Markdown format. This tool generates a Markdown file containing the repository's directory tree and the contents of its files. It supports various file types, including Python scripts, Markdown files, Jupyter Notebooks, and PDFs.

---

## Features

- **Generate repository directory tree**: Outputs the structure of the repository in a `tree` block format.
- **Convert files to Markdown**:
  - Supports syntax highlighting for code files.
  - Converts Jupyter Notebooks (`.ipynb`) and PDFs (`.pdf`) into Markdown.
- **Support for `.gitignore` and `.globalignore`**:
  - Automatically excludes files/directories listed in `.gitignore` or `.globalignore`.
- **Custom exclusion patterns**: Use regular expressions to exclude specific files or directories.
- **Skip empty files**: Avoids processing files with no content.
- **Copy output to clipboard**: Easily copy the generated Markdown output for further use.

---

## Requirements

- **Python 3.12 or higher**
- **Linux operating system**
- **Dependencies**:
  - `pathspec` (for `.gitignore` support)
  - `nbconvert` (for Jupyter Notebook conversion)
  - `PyMuPDF4LLM` (for PDF conversion)
  - `wl-copy` (optional, for clipboard functionality)

---

## Installation

### Install from PyPI

You can install `git2md` directly from PyPI using pip:

```bash
pip install git2md
```

### Install from source

1. Clone the repository:

   ```bash
   git clone https://github.com/xpos587/git2md.git
   cd git2md
   ```

2. Run the installation script:

   ```bash
   python install.py
   ```

   The script will:

   - Install the package in your Python environment.
   - Create a symlink in `/usr/local/bin` for global access (requires `sudo`).

---

## Usage

### Basic Command

```bash
git2md <path> [options]
```

### Options

| Option                       | Description                                                           |
| ---------------------------- | --------------------------------------------------------------------- |
| `path`                       | Path to the Git project directory or file to process.                 |
| `-o`, `--output`             | Output file path for saving the generated Markdown.                   |
| `-rex`, `--regex-exclude`    | List of regular expressions to exclude specific files or directories. |
| `-se`, `--skip-empty-files`  | Skip empty files during processing.                                   |
| `-cp`, `--clipboard`         | Copy the output content to clipboard (requires `wl-copy`).            |
| `-igi`, `--ignore-gitignore` | Ignore `.gitignore` and `.globalignore` rules.                        |

---

## Examples

### Generate Markdown for an entire repository

```bash
git2md /path/to/repo -o output.md
```

### Exclude specific files/directories using regex

```bash
git2md /path/to/repo -rex ".*\.log$" ".*\.tmp$" -o output.md
```

### Skip empty files and copy output to clipboard

```bash
git2md /path/to/repo -se -cp
```

### Ignore `.gitignore` rules

```bash
git2md /path/to/repo -igi -o output.md
```

---

## Output Format

### Directory Tree

The directory tree is included as a code block with the language identifier `tree`. For example:

```tree
src/
├── main.py
├── utils/
│   ├── helper.py
│   └── __init__.py
└── README.md
```

### File Contents

Each file is included with its relative path as a header, followed by its content in a code block.

#### Example for a Python File (`main.py`)

````markdown
# File: src/main.py

```python
print("Hello, world!")
```

# End of file: src/main.py
````

#### Example for a Jupyter Notebook (`notebook.ipynb`)

The content is converted from `.ipynb` to Markdown and included directly:

```markdown
# File: notebook.ipynb

# Converted content from Jupyter Notebook...

# End of file: notebook.ipynb
```

#### Example for a PDF (`document.pdf`)

The content is extracted as Markdown:

```markdown
# File: document.pdf

# Extracted content from PDF...

# End of file: document.pdf
```

---

## Global Ignore Patterns

You can create a `.globalignore` file in the same directory as the script to specify patterns that should be ignored across all repositories. The format is identical to `.gitignore`.

#### Example `.globalignore`

```plaintext
__pycache__/
*.pyc
.mypy_cache/
.env
*.log
```

---

## Development

To set up the development environment:

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install pathspec nbconvert pymupdf4llm
   ```

3. Install in editable mode:

   ```bash
   pip install -e .
   ```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## Authors

Michael (<x30827pos@gmail.com>)

---

## Acknowledgments

Thanks to the developers of the `pathspec`, `nbconvert`, and `PyMuPDF4LLM` libraries.

Inspired by the need to easily document Git repositories for LLM-based workflows.
