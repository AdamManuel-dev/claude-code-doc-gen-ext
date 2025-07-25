# Claude Code Documentation Extension - Usage Guide

## Table of Contents
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Command Options](#command-options)
- [Examples](#examples)
- [Supported Languages](#supported-languages)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Known Issues](#known-issues)

## Installation

The documentation commands are already installed if you have this extension. To verify:

```bash
# Check if commands are available
ls .claude/commands/doc-*

# Make sure they're executable
chmod +x .claude/commands/doc-*
```

## Basic Usage

The extension provides four documentation commands:

### 1. `/doc-last` - Document files from last commit
```bash
/doc-last
```
Documents files changed in the most recent git commit. Falls back to recently modified files if not in a git repository.

### 2. `/doc-recent` - Document recently modified files
```bash
/doc-recent
```
Documents files modified in the last 5 minutes, regardless of git status.

### 3. `/doc-staged` - Document staged files
```bash
/doc-staged
```
Documents files currently staged in git (added with `git add`).

### 4. `/doc-all` - Document all project files
```bash
/doc-all
```
Documents all supported files in the current directory and subdirectories.

## Command Options

All commands support the following options:

### `--help` or `-h`
Show help message and usage information.
```bash
/doc-last --help
```

### `--verbose` or `-v`
Show detailed output during processing.
```bash
/doc-last --verbose
```

### `--dry-run` or `-n`
Preview what would be done without making any changes.
```bash
/doc-last --dry-run
```

### `--no-enhance`
Skip the Claude Code enhancement step (faster but less sophisticated docs).
```bash
/doc-last --no-enhance
```

### `--version`
Show the version of the documentation generator.
```bash
/doc-last --version
```

## Examples

### Example 1: Document recent changes before committing
```bash
# Make some code changes
vim src/utils.js

# Generate documentation for changed files
/doc-last

# Review the changes
git diff

# Commit with documentation
git add .
git commit -m "Add utilities with documentation"
```

### Example 2: Preview documentation changes
```bash
# See what would be documented without making changes
/doc-last --dry-run

# If satisfied, run for real
/doc-last
```

### Example 3: Document specific staged files
```bash
# Stage only the files you want to document
git add src/api.js src/auth.py

# Document just those files
/doc-staged

# Commit the documented files
git commit -m "Document API and auth modules"
```

### Example 4: Full project documentation
```bash
# Document everything (use with caution on large projects)
/doc-all --dry-run

# If the list looks reasonable, proceed
/doc-all
```

## Supported Languages

### JavaScript/TypeScript
- File extensions: `.js`, `.jsx`, `.ts`, `.tsx`
- Documentation format: JSDoc
- Detects: Functions, arrow functions, classes, methods

Example output:
```javascript
/**
 * Calculates the total price.
 * @param {*} items - The items.
 * @param {*} taxRate - The taxRate.
 * @returns {*} The result.
 */
function calculateTotal(items, taxRate) {
    // ...
}
```

### Python
- File extensions: `.py`, `.pyw`
- Documentation format: Google-style docstrings
- Detects: Functions, methods, classes

Example output:
```python
def calculate_average(numbers):
    """
    Calculate average.
    
    Args:
        numbers: The numbers.
    
    Returns:
        The result.
    """
    # ...
```

## How It Works

1. **File Detection**: The command identifies which files to process based on:
   - Git status (commits, staged files, or changes)
   - File modification times
   - File extensions

2. **Analysis**: For each file, it:
   - Parses the code to find functions, classes, and methods
   - Checks if documentation already exists
   - Identifies items needing documentation

3. **Generation**: For undocumented items, it:
   - Creates appropriate documentation templates
   - Infers basic information from function/parameter names
   - Inserts documentation at the correct location

4. **Backup**: Before modifying any files:
   - Creates timestamped backups in `.doc-last-backups/`
   - Preserves original file permissions

5. **Enhancement** (optional): If Claude Code CLI is available:
   - Sends files to Claude for intelligent documentation enhancement
   - Improves descriptions based on actual code logic

6. **Reporting**: After completion:
   - Shows summary of changes
   - Creates `documentation-report.md` with details

## Troubleshooting

### Command not found
```bash
# Make sure the command is executable
chmod +x .claude/commands/doc-last

# Check if .claude/commands is in your PATH or use full path
./.claude/commands/doc-last
```

### No files detected
- Ensure you have uncommitted changes or recently modified files
- Check that files have supported extensions (.js, .ts, .py, etc.)
- Try using `/doc-recent` for time-based detection

### Documentation not inserted correctly
- Check the backup files in `.doc-last-backups/`
- Ensure files have proper syntax (parsing errors can cause issues)
- Review generated documentation with `--dry-run` first

### Claude enhancement fails
- This is optional - use `--no-enhance` to skip
- Ensure Claude Code CLI is installed and available
- Check that you have API access configured

## Known Issues

1. **Python Docstring Placement**: Currently, Python docstrings may be placed incorrectly (above the function instead of inside). This is tracked in BUGS.md.

2. **Complex Syntax**: Some edge cases may not be detected:
   - Dynamic function creation
   - Decorated functions (Python)
   - Complex destructuring patterns

3. **Large Files**: Very large files may take time to process. Use `--verbose` to see progress.

## Best Practices

1. **Review Before Committing**: Always review generated documentation:
   ```bash
   /doc-last --dry-run  # Preview
   /doc-last           # Execute
   git diff            # Review changes
   ```

2. **Use Backups**: Backups are created automatically, but you can also:
   ```bash
   git stash          # Save current state
   /doc-last          # Generate docs
   git diff           # Review
   git stash pop      # If you want to revert
   ```

3. **Incremental Documentation**: Document as you code:
   - Use `/doc-last` after each feature
   - Don't wait until the end of the project
   - Keep documentation in sync with code

4. **Enhance When Possible**: If you have Claude Code CLI:
   - Let Claude improve the documentation
   - It understands context and generates better descriptions
   - Review and adjust as needed

## Configuration

Currently, configuration is done via command-line options. Future versions may support:
- Configuration files
- Custom documentation templates
- File pattern exclusions
- Documentation style preferences

## Contributing

To improve the documentation generator:
1. Test with various code patterns
2. Report issues in the project repository
3. Suggest enhancements for better detection or generation

## Version History

- **v1.0.0** (2025-07-25): Initial release
  - Basic JSDoc and Python docstring generation
  - Git integration
  - Claude Code enhancement support