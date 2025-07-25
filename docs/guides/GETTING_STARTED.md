# Getting Started Guide

## Welcome

The Claude Code Documentation Generation Extension helps you automatically generate comprehensive JSDoc comments for your JavaScript and TypeScript projects. This guide will walk you through installation, basic usage, and common workflows.

## Prerequisites

### System Requirements
- **Node.js**: Version 14.0.0 or higher
- **npm**: Version 6.0.0 or higher (comes with Node.js)
- **Git**: Version 2.0 or higher (recommended for file discovery)
- **Claude Code CLI**: Latest version (for enhanced documentation)

### Supported File Types
- JavaScript: `.js`, `.jsx`, `.mjs`, `.cjs`
- TypeScript: `.ts`, `.tsx`
- React components with JSX/TSX

### Verify Prerequisites
```bash
# Check Node.js version
node --version
# Should output v14.0.0 or higher

# Check npm version
npm --version

# Check Git installation
git --version

# Check Claude Code CLI (optional)
claude --version
```

## Installation

### Quick Install
```bash
# Clone the repository
git clone https://github.com/yourusername/claude-code-doc-generation-ext.git

# Navigate to the project
cd claude-code-doc-generation-ext

# Install dependencies
npm install

# Make scripts executable (Unix/Mac)
chmod +x doc-generator.js
```

### Alternative: NPM Package (if published)
```bash
npm install -g claude-code-doc-generator
```

### Verify Installation
```bash
# Test the installation
node doc-generator.js --help

# Should display help information
```

## Basic Usage

### Your First Documentation Run

1. **Navigate to your project**:
   ```bash
   cd /path/to/your/javascript/project
   ```

2. **Run the documentation generator**:
   ```bash
   # Using the full path
   node /path/to/claude-code-doc-generation-ext/doc-generator.js
   
   # Or if installed globally
   doc-last
   ```

3. **Review the output**:
   - The tool will show you which files it found
   - Display analysis results for each file
   - Show how many functions were documented
   - Create backups in `.doc-last-backups/`

### Understanding the Output

```bash
============================================================
Claude Code Documentation Generator (AST)
============================================================

🔍 Detecting recently modified files...

✓ Found 3 file(s) to process:
  📄 src/utils.js (jsdoc)
  📄 components/Button.tsx (jsdoc)
  📄 lib/helpers.js (jsdoc)

📊 Analyzing files for documentation needs...

Documentation Analysis Results:
============================================================

src/utils.js:
  Total functions/classes: 5
  Documented: 2
  Undocumented: 3 ❌

components/Button.tsx:
  Total functions/classes: 3
  Documented: 3
  Undocumented: 0 ✅

📝 Generating documentation...
Creating backups...

Processing src/utils.js...
  ✓ Added documentation for 3 functions

============================================================
Documentation Generation Complete!
============================================================

✅ Successfully documented 3 functions
Backups saved in: .doc-last-backups
Report saved to: documentation-report.md
```

## Command Options

### Essential Options

#### Preview Mode (Recommended for First Use)
```bash
node doc-generator.js --dry-run
# Shows what would be done without modifying files
```

#### Verbose Output
```bash
node doc-generator.js --verbose
# Shows detailed processing information
```

#### Skip AI Enhancement
```bash
node doc-generator.js --no-enhance
# Generates basic documentation without Claude AI improvement
```

### Combining Options
```bash
# Preview with detailed output
node doc-generator.js --dry-run --verbose

# Generate docs without AI enhancement, with verbose output
node doc-generator.js --no-enhance --verbose
```

## File Discovery

The tool uses smart file discovery to find files that need documentation:

### Git-Based Discovery (Primary)
When in a git repository, the tool looks for:
1. **Files from last commit**: `git diff --name-only HEAD~1 HEAD`
2. **Staged changes**: `git diff --cached --name-only`
3. **Unstaged changes**: `git diff --name-only`

### Filesystem Discovery (Fallback)
When not in a git repository or no git changes found:
- Scans for files modified in the last 5 minutes
- Recursively searches current directory
- Excludes hidden directories (starting with `.`)

### Manual File Selection
For specific files, you can modify them slightly to trigger discovery:
```bash
# Touch a file to make it "recently modified"
touch src/utils.js

# Then run the generator
node doc-generator.js
```

## Understanding Generated Documentation

### Before Documentation
```javascript
function calculateTotal(items, taxRate) {
    return items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
}
```

### After Documentation
```javascript
/**
 * Calculates the total price including tax.
 * @param {*} items - The items.
 * @param {*} taxRate - The tax rate.
 * @returns {*} The result.
 */
function calculateTotal(items, taxRate) {
    return items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
}
```

### With Claude AI Enhancement
```javascript
/**
 * Calculates the total price of items including tax.
 * 
 * Computes the sum of all item prices and applies the specified tax rate
 * to return the final total including tax.
 * 
 * @param {Array<{price: number}>} items - Array of items with price properties
 * @param {number} taxRate - Tax rate as decimal (e.g., 0.08 for 8% tax)
 * @returns {number} Total price including tax
 * 
 * @example
 * const items = [{ price: 10 }, { price: 20 }];
 * const total = calculateTotal(items, 0.08);
 * console.log(total); // 32.4 (30 + 8% tax)
 */
function calculateTotal(items, taxRate) {
    return items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
}
```

## Common Workflows

### Daily Development Workflow
```bash
# 1. Write some new functions
# 2. Generate documentation for recent changes
node doc-generator.js

# 3. Review the generated docs
# 4. Commit your changes including the new documentation
git add .
git commit -m "Add new features with documentation"
```

### Code Review Workflow
```bash
# Before submitting PR, ensure all functions are documented
node doc-generator.js --dry-run

# If undocumented functions found, generate docs
node doc-generator.js

# Review the generated documentation
# Enhance manually if needed
```

### Project Setup Workflow
```bash
# For existing projects, document all files (use carefully!)
# First, see what would be done
node doc-generator.js --dry-run

# If comfortable with changes, run for real
node doc-generator.js

# Review and enhance key function documentation manually
```

## Best Practices

### 1. Start with Dry Run
Always preview changes first:
```bash
node doc-generator.js --dry-run
```

### 2. Use Version Control
Ensure your code is committed before running:
```bash
git add .
git commit -m "Code before documentation generation"
node doc-generator.js
```

### 3. Review Generated Documentation
The tool generates basic documentation. Always review and enhance:
- Add more specific descriptions
- Include usage examples for complex functions
- Document error conditions
- Add performance notes where relevant

### 4. Customize for Your Project
Consider the generated documentation as a starting point:
- Replace generic `{*}` types with specific types
- Add `@example` blocks for important functions
- Include `@throws` documentation for error cases
- Add `@deprecated` tags for legacy functions

### 5. Use with Claude AI Enhancement
For better documentation quality:
```bash
# Let Claude AI enhance the basic documentation
node doc-generator.js
# (Review the enhanced documentation)
```

## Configuration

### Command Line Configuration
Create npm scripts in your `package.json`:
```json
{
  "scripts": {
    "doc": "node doc-generator.js",
    "doc:preview": "node doc-generator.js --dry-run",
    "doc:verbose": "node doc-generator.js --verbose",
    "doc:basic": "node doc-generator.js --no-enhance"
  }
}
```

### Environment Setup
For team consistency, consider adding to your project:
```bash
# .gitignore
.doc-last-backups/

# README.md addition
## Documentation Generation
To generate documentation for modified files:
npm run doc:preview  # Preview changes
npm run doc          # Generate documentation
```

## Troubleshooting

### Common Issues

#### 1. No Files Found
```
No files found that need documentation.
```
**Solution**: 
- Make sure you're in a git repository with recent changes, or
- Modify a file and try again, or
- Use `touch filename.js` to mark files as recently modified

#### 2. Parse Errors
```
Warning: Could not parse src/broken.js: Unexpected token
```
**Solution**: 
- Fix syntax errors in the file
- The tool will continue with other files

#### 3. Permission Errors
```
Error inserting documentation: Permission denied
```
**Solution**: 
- Check file permissions: `ls -la filename.js`
- Ensure the file is writable: `chmod +w filename.js`

#### 4. Claude Enhancement Fails
```
⚠️  Claude Code enhancement failed
```
**Solution**: 
- Check if Claude Code CLI is installed: `claude --version`
- Run without enhancement: `node doc-generator.js --no-enhance`

### Getting Help

#### Verbose Mode
For detailed troubleshooting information:
```bash
node doc-generator.js --verbose
```

#### Check Installation
```bash
# Verify dependencies
npm list

# Test with a simple file
echo 'function test() { return true; }' > test.js
node doc-generator.js --dry-run
rm test.js
```

#### Report Issues
If you encounter problems:
1. Run with `--verbose` flag
2. Note the exact error message
3. Include your Node.js version: `node --version`
4. Include file type and size information

## Next Steps

Once you're comfortable with basic usage:

1. **Read the [API Documentation](../API.md)** for programmatic usage
2. **Explore [Advanced Usage](../tutorials/advanced-usage.md)** for complex scenarios  
3. **Learn about [Architecture](../../ARCHITECTURE.md)** for customization
4. **Set up automated workflows** with git hooks or CI/CD integration

## Quick Reference

### Most Common Commands
```bash
# Preview what would be documented
node doc-generator.js --dry-run

# Generate documentation with detailed output
node doc-generator.js --verbose

# Generate basic documentation without AI enhancement
node doc-generator.js --no-enhance

# Show help
node doc-generator.js --help
```

### File Locations
- **Backups**: `.doc-last-backups/`
- **Report**: `documentation-report.md`
- **Generator**: `doc-generator.js`

Congratulations! You're now ready to use the Claude Code Documentation Generation Extension effectively. Start with small files and dry runs to get comfortable with the tool before processing larger codebases.