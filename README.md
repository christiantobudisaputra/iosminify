# iOS Project Minifier

This Python script minifies and chunks an iOS project into multiple markdown files. It's designed to help developers work with large iOS projects in AI-assisted development environments by breaking down the project into manageable pieces.

## Features

- Minifies Swift and Objective-C files
- Chunks large files into smaller markdown files
- Creates an index file for easy navigation
- Includes asset information
- Generates a project structure overview
- Supports custom ignore patterns
- Handles both Swift and Objective-C code

## Requirements

- Python 3.6 or higher

## Usage

1. Place the `ios_project_minifier.py` script in a convenient location.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script with the following command:

```
python ios_project_minifier.py /path/to/ios/project /path/to/output/directory --include-objc --chunk-size 8000
```

Replace `/path/to/ios/project` with the path to your iOS project, and `/path/to/output/directory` with the desired output location for the markdown files.

### Command-line Arguments

- `project_path`: Path to the iOS project (required)
- `output_dir`: Path to the output directory for markdown files (required)
- `--include-objc`: Include Objective-C files in the minification process (optional)
- `--chunk-size`: Maximum size of each chunk in characters (optional, default is 8000)

## Output

The script will generate:

1. An `index.md` file in the output directory, serving as a table of contents for all chunked files.
2. Multiple markdown files containing chunked content from your iOS project.
3. A project structure overview in JSON format.
4. A list of available assets in the project.

## Customizing Ignore Patterns

Create a `.iosminifyignore` file in your iOS project root to specify files or directories to ignore. The syntax is similar to `.gitignore`.

## File Hashing

The script generates MD5 hashes for each processed file. These hashes are included in the project structure overview, allowing for quick identification of file changes without processing the entire content.

## Minification Process

- Swift files are minified by removing comments and extra whitespace.
- Objective-C files (if included) are not minified but are included in their original form.
- Other file types are ignored unless specifically handled in the script.

## Note on Minification

This script provides basic minification for Swift files. For production use or more complex projects, consider implementing a more robust minification solution that takes into account Swift's syntax intricacies.

## Use with AI Models

The chunked output is designed to work well with AI models that have context window limitations. You can load relevant chunks as needed when working on specific parts of your project.

## Best Practices

1. Run the script periodically as your project evolves to keep the minified version up-to-date.
2. When using with AI models, start by loading the `index.md` file to understand the project structure.
3. Load specific chunks as needed based on the feature or bug you're working on.
4. Use the file hashes to quickly identify which files have changed since the last minification.

## Troubleshooting

- If you encounter "File not found" errors, ensure all paths are correct and you have necessary permissions.
- For large projects, you might need to increase the `--chunk-size` if you're seeing truncated content.
- If certain files are unexpectedly ignored, check your `.iosminifyignore` file.

## Contributing

Feel free to submit issues or pull requests to improve this script. Some areas for potential enhancement include:

- More sophisticated code analysis for meaningful chunking
- Support for additional iOS-specific file types
- Integration with version control systems for differential updates

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]

## Disclaimer

This script is provided as-is. Always backup your project before running any automated scripts. The authors are not responsible for any data loss or project corruption.
