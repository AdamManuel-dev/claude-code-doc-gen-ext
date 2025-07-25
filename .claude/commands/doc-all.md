---
description: Generate documentation for all supported files in the project (use with caution)
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Glob, Grep, LS]
argument-hint: "[--dry-run] [--verbose] [--no-enhance]"
---

# Generate Documentation for All Files

Generate comprehensive documentation for all supported files in the project. 

⚠️ **Warning**: This command will process ALL code files in your project. Use with caution on large projects.

## Usage
```
/doc-all [options]
```

## Options
- `--dry-run` - Preview changes without modifying files (recommended first)
- `--verbose` - Show detailed output
- `--no-enhance` - Skip Claude enhancement step

## What I'll do:

1. Find all supported code files in the project
2. Analyze each file to find undocumented functions, classes, and methods
3. Generate appropriate documentation:
   - JSDoc for JavaScript/TypeScript files
   - Google-style docstrings for Python files
4. Create backups before modifying any files
5. Show progress for large projects
6. Optionally enhance documentation with more meaningful descriptions

Execute the documentation generator for all files:

!cd "$PROJECT_ROOT" && python "$PROJECT_ROOT/.claude/commands/doc-last" --all $ARGUMENTS