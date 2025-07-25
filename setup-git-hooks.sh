#!/bin/bash
# Git Hooks Setup Script for Claude Code Documentation Generator
# Run this script in any git repository where you want automatic documentation

PROJECT_ROOT="/Users/adammanuel/Projects/claude-code-doc-generation-ext"
HOOK_SCRIPT="$PROJECT_ROOT/claude-code-documentation-hooks.py"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository"
    exit 1
fi

echo "Setting up documentation hooks in $(pwd)"

# Copy pre-commit hook
cp "$HOOK_SCRIPT" .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Update the hook with correct paths
sed -i.bak "s|DOC_GENERATOR_PATH = None|DOC_GENERATOR_PATH = \"$PROJECT_ROOT/doc-generator.js\"|" .git/hooks/pre-commit

echo "✓ Pre-commit hook installed"
echo "✓ Documentation will be generated automatically on git commit"
echo ""
echo "To disable hooks for a specific commit, use:"
echo "  git commit --no-verify"
