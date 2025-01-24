import os

def read_gitignore():
    """Read patterns from .gitignore to exclude files and directories."""
    gitignore_path = ".gitignore"
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as file:
            patterns = file.read().splitlines()
        return [pattern.strip() for pattern in patterns if pattern.strip() and not pattern.startswith("#")]
    return []

def is_ignored(path, ignore_patterns):
    """Check if a file or directory matches any .gitignore patterns or is in .git."""
    # Explicitly ignore .git folder
    if ".git" in path.split(os.sep):
        return True

    for pattern in ignore_patterns:
        if pattern.endswith("/") and path.startswith(pattern):  # Directory match
            return True
        if path.endswith(pattern):  # File match
            return True
    return False

def collect_project_structure(root_dir, ignore_patterns):
    """Generate a folder/file structure and collect file contents."""
    structure = []
    file_contents = []

    for root, dirs, files in os.walk(root_dir):
        # Filter ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d) + "/", ignore_patterns)]

        # Add directory structure
        relative_root = os.path.relpath(root, root_dir)
        structure.append(relative_root if relative_root != "." else "/")

        # Add files and collect contents
        for file in files:
            if not is_ignored(os.path.join(root, file), ignore_patterns):
                file_path = os.path.join(root, file)
                structure.append(os.path.join(relative_root, file))
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    file_contents.append(f"\n--- {file_path} ---\n")
                    file_contents.append(f.read())

    return structure, file_contents

def save_to_txt(structure, file_contents, output_dir="reports"):
    """Save folder structure and file contents to separate .txt files."""
    # Ensure the reports directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save project structure
    with open(os.path.join(output_dir, "project_structure.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(structure))

    # Save file contents
    with open(os.path.join(output_dir, "project_files.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(file_contents))

def main():
    ignore_patterns = read_gitignore()
    structure, file_contents = collect_project_structure(".", ignore_patterns)
    save_to_txt(structure, file_contents)
    print("Project structure and files collected into 'reports/project_structure.txt' and 'reports/project_files.txt'.")

if __name__ == "__main__":
    main()
