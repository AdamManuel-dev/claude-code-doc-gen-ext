---
description: Generate documentation for files from the last git commit or recently modified files
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Glob, Grep, LS]
argument-hint: "[--dry-run] [--verbose] [--no-enhance]"
---

# Generate Documentation for Recent Files

Generate comprehensive documentation for files that were modified in the last git commit. If no commit is found, falls back to recently modified files.

## Usage
```
/doc-last [options]
```

## Options
- `--dry-run` - Preview changes without modifying files
- `--verbose` - Show detailed output
- `--no-enhance` - Skip Claude enhancement step

## What I'll do:

1. Detect recently modified files using git or filesystem timestamps
2. Analyze each file to find undocumented functions, classes, and methods
3. Generate appropriate documentation:
   - JSDoc for JavaScript/TypeScript files
   - Google-style docstrings for Python files
4. Create backups before modifying any files
5. Optionally enhance documentation with more meaningful descriptions

Execute the documentation generator:

!cd "$PROJECT_ROOT" && python "$PROJECT_ROOT/.claude/commands/doc-last" $ARGUMENTS