import os
import argparse
from pathlib import Path
import fnmatch
import json
import hashlib

def read_ignore_file(ignore_file_path):
    if os.path.exists(ignore_file_path):
        with open(ignore_file_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def should_ignore(file_path, ignore_patterns):
    return any(fnmatch.fnmatch(file_path, pattern) for pattern in ignore_patterns)

def minify_swift_code(code):
    lines = code.split('\n')
    minified = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]
    return ' '.join(minified)

def process_file(file_path, ignore_patterns):
    if should_ignore(file_path, ignore_patterns):
        return None

    with open(file_path, 'r') as f:
        content = f.read()

    if file_path.endswith('.swift'):
        return minify_swift_code(content)
    elif file_path.endswith('.m') or file_path.endswith('.h'):
        return content
    else:
        return None

def find_assets(project_path):
    asset_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.xcassets']
    assets = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in asset_extensions):
                assets.append(os.path.join(root, file))
    return assets

def generate_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def create_chunk(content, chunk_size, file_path, output_dir):
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_file = os.path.join(output_dir, f"{os.path.basename(file_path)}_chunk_{i+1}.md")
        with open(chunk_file, 'w') as f:
            f.write(chunk)
        chunk_files.append(chunk_file)
    return chunk_files

def main(project_path, output_dir, include_objc=False, chunk_size=8000):
    ignore_file = os.path.join(project_path, '.iosminifyignore')
    ignore_patterns = read_ignore_file(ignore_file)

    os.makedirs(output_dir, exist_ok=True)

    index_content = "# iOS Project Minified Code Index\n\n"
    file_hashes = {}

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.swift') or (include_objc and (file.endswith('.m') or file.endswith('.h'))):
                file_path = os.path.join(root, file)
                processed_content = process_file(file_path, ignore_patterns)
                if processed_content:
                    relative_path = os.path.relpath(file_path, project_path)
                    file_hash = generate_file_hash(file_path)
                    file_hashes[relative_path] = file_hash

                    content = f"## {relative_path}\n\n```swift\n{processed_content}\n```\n\n"
                    chunk_files = create_chunk(content, chunk_size, relative_path, output_dir)

                    index_content += f"- {relative_path}\n"
                    for i, chunk_file in enumerate(chunk_files):
                        index_content += f"  - [Chunk {i+1}]({os.path.relpath(chunk_file, output_dir)})\n"

    assets = find_assets(project_path)
    if assets:
        asset_content = "## Available Assets\n\n"
        for asset in assets:
            relative_path = os.path.relpath(asset, project_path)
            asset_content += f"- {relative_path}\n"

        asset_chunks = create_chunk(asset_content, chunk_size, "assets", output_dir)
        index_content += "\n## Assets\n"
        for i, chunk_file in enumerate(asset_chunks):
            index_content += f"- [Asset List Chunk {i+1}]({os.path.relpath(chunk_file, output_dir)})\n"

    project_structure = {
        "name": os.path.basename(project_path),
        "structure": {}
    }

    def build_structure(path, structure):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path) and not should_ignore(item_path, ignore_patterns):
                structure[item] = {}
                build_structure(item_path, structure[item])
            elif os.path.isfile(item_path) and not should_ignore(item_path, ignore_patterns):
                structure[item] = file_hashes.get(os.path.relpath(item_path, project_path), None)

    build_structure(project_path, project_structure["structure"])

    structure_content = "\n## Project Structure\n\n```json\n"
    structure_content += json.dumps(project_structure, indent=2)
    structure_content += "\n```\n"

    structure_chunks = create_chunk(structure_content, chunk_size, "project_structure", output_dir)
    index_content += "\n## Project Structure\n"
    for i, chunk_file in enumerate(structure_chunks):
        index_content += f"- [Structure Chunk {i+1}]({os.path.relpath(chunk_file, output_dir)})\n"

    with open(os.path.join(output_dir, "index.md"), 'w') as f:
        f.write(index_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minify iOS project into multiple markdown files.")
    parser.add_argument("project_path", help="Path to the iOS project")
    parser.add_argument("output_dir", help="Path to the output directory for markdown files")
    parser.add_argument("--include-objc", action="store_true", help="Include Objective-C files")
    parser.add_argument("--chunk-size", type=int, default=8000, help="Maximum size of each chunk in characters")
    args = parser.parse_args()

    main(args.project_path, args.output_dir, args.include_objc, args.chunk_size)
