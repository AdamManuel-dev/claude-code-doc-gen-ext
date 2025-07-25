---
description: Generate documentation for files currently staged in git
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Glob, Grep, LS]
argument-hint: "[--dry-run] [--verbose] [--no-enhance]"
---

# Generate Documentation for Staged Files

Generate comprehensive documentation for files that are currently staged in git.

## Usage
```
/doc-staged [options]
```

## Options
- `--dry-run` - Preview changes without modifying files
- `--verbose` - Show detailed output
- `--no-enhance` - Skip Claude enhancement step

## What I'll do:

1. Get list of staged files from git
2. Filter for supported code files (JS, TS, Python, etc.)
3. Analyze each file to find undocumented functions, classes, and methods
4. Generate appropriate documentation:
   - JSDoc for JavaScript/TypeScript files
   - Google-style docstrings for Python files
5. Create backups before modifying any files
6. Optionally enhance documentation with more meaningful descriptions

Execute the documentation generator for staged files:

!cd "$PROJECT_ROOT" && python "$PROJECT_ROOT/.claude/commands/doc-last" --staged $ARGUMENTS