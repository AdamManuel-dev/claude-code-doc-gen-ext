# Getting Started with Claude Code Documentation Generator

This tutorial will walk you through your first steps with the Claude Code Documentation Generator extension. By the end, you'll be able to automatically generate documentation for your code files.

## Prerequisites

Before starting, ensure you have:

- Node.js (version 14 or higher)
- Git (for repository-based file detection)
- Claude Code CLI (optional, for AI-enhanced documentation)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/claude-code-doc-generation-ext.git
cd claude-code-doc-generation-ext
```

### Step 2: Install Dependencies

```bash
npm install
```

This installs the required Babel packages for AST parsing.

### Step 3: Make Commands Executable

```bash
chmod +x doc-generator.js
chmod +x documentation-slash-command.py
```

### Step 4: Verify Installation

```bash
./doc-generator.js --version
```

You should see the version number displayed.

## Your First Documentation Generation

### Example 1: Document a Simple JavaScript File

Let's create a simple JavaScript file without documentation:

```javascript
// save as example.js
function calculateArea(length, width) {
    return length * width;
}

function calculatePerimeter(length, width) {
    return 2 * (length + width);
}

const formatDimensions = (length, width) => {
    return `${length}x${width}`;
};

export { calculateArea, calculatePerimeter, formatDimensions };
```

Now generate documentation:

```bash
./doc-generator.js --verbose
```

The file will be updated with JSDoc comments:

```javascript
/**
 * Calculate area.
 * @param {*} length - The length.
 * @param {*} width - The width.
 * @returns {*} The result.
 */
function calculateArea(length, width) {
    return length * width;
}

/**
 * Calculate perimeter.
 * @param {*} length - The length.
 * @param {*} width - The width.
 * @returns {*} The result.
 */
function calculatePerimeter(length, width) {
    return 2 * (length + width);
}

/**
 * Format dimensions.
 * @param {*} length - The length.
 * @param {*} width - The width.
 * @returns {*} The result.
 */
const formatDimensions = (length, width) => {
    return `${length}x${width}`;
};
```

### Example 2: Document Recent Git Changes

After making changes to your code:

```bash
# Make some changes
vim src/utils.js

# See what would be documented
./doc-generator.js --dry-run

# Generate documentation
./doc-generator.js

# Review changes
git diff

# Commit with documentation
git add .
git commit -m "Add utility functions with documentation"
```

### Example 3: Document Python Files

Create a Python file:

```python
# save as calculator.py
def add(a, b):
    return a + b

def multiply(a, b):
    result = 0
    for _ in range(b):
        result += a
    return result

class Calculator:
    def __init__(self):
        self.memory = 0
    
    def add_to_memory(self, value):
        self.memory += value
        return self.memory
```

Run the documentation generator:

```bash
python3 documentation-slash-command.py
```

Result:

```python
def add(a, b):
    """
    Add.
    
    Args:
        a: The a.
        b: The b.
    
    Returns:
        The result.
    """
    return a + b

def multiply(a, b):
    """
    Multiply.
    
    Args:
        a: The a.
        b: The b.
    
    Returns:
        The result.
    """
    result = 0
    for _ in range(b):
        result += a
    return result

class Calculator:
    """Calculator."""
    
    def __init__(self):
        """Initialize."""
        self.memory = 0
    
    def add_to_memory(self, value):
        """
        Add to memory.
        
        Args:
            value: The value.
        
        Returns:
            The result.
        """
        self.memory += value
        return self.memory
```

## Using with Claude Code

### Setup in Claude Code

1. Copy the commands to your Claude Code commands directory:

```bash
mkdir -p ~/.claude/commands
cp doc-generator.js ~/.claude/commands/doc-last
cp documentation-slash-command.py ~/.claude/commands/doc-recent
chmod +x ~/.claude/commands/doc-*
```

2. Now you can use slash commands in Claude Code:

```
/doc-last
/doc-recent
/doc-staged
/doc-all
```

### Integration with Workflow

1. **During Development**: Use `/doc-last` after writing new functions
2. **Before Commits**: Use `/doc-staged` to document staged files
3. **Code Review**: Use `/doc-all --dry-run` to check documentation coverage
4. **Refactoring**: Use `/doc-recent` after making changes

## Best Practices

### 1. Review Generated Documentation

Always review the generated documentation:

```bash
# Preview first
/doc-last --dry-run

# Then generate
/doc-last

# Review changes
git diff
```

### 2. Enhance with Claude AI

If you have Claude Code CLI installed:

```bash
# Generate with AI enhancement
/doc-last

# The tool will automatically use Claude to improve descriptions
```

### 3. Maintain Consistency

- Use the same documentation style throughout your project
- Configure your preferred style (future feature)
- Review and adjust generated documentation as needed

### 4. Use Git Integration

```bash
# Document before committing
git add src/newFeature.js
/doc-staged
git commit -m "Add new feature with documentation"
```

## Common Patterns

### Pattern 1: Document After Feature Complete

```bash
# Implement feature
vim src/feature.js

# Test feature
npm test

# Document feature
/doc-last

# Commit everything
git add .
git commit -m "feat: add feature with docs"
```

### Pattern 2: Progressive Documentation

```bash
# Document as you go
vim src/module1.js
/doc-recent

vim src/module2.js
/doc-recent

# Final review
/doc-all --dry-run
```

### Pattern 3: Bulk Documentation

```bash
# For existing projects
/doc-all --dry-run > documentation-plan.txt

# Review the plan
cat documentation-plan.txt

# Execute if satisfied
/doc-all
```

## Tips and Tricks

1. **Use Verbose Mode** for debugging:
   ```bash
   /doc-last --verbose
   ```

2. **Check Specific Files** by staging them:
   ```bash
   git add specific-file.js
   /doc-staged
   ```

3. **Backup Important Files** (automatic, but you can also):
   ```bash
   cp important.js important.js.backup
   /doc-last
   ```

4. **Combine with Linters**:
   ```bash
   /doc-last && npm run lint
   ```

## Next Steps

- Read the [Advanced Tutorial](./advanced-usage.md) for complex scenarios
- Check the [API Documentation](../API.md) for programmatic usage
- See [Troubleshooting Guide](../TROUBLESHOOTING.md) for common issues
- Contribute to the project on GitHub

## Summary

You've learned how to:
- Install and set up the documentation generator
- Generate documentation for JavaScript and Python files
- Use various command options
- Integrate with your development workflow
- Follow best practices for documentation

The Claude Code Documentation Generator helps maintain high-quality documentation with minimal effort. Start using it in your projects today!