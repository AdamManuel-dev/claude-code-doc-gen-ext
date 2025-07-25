# Claude Code Installation Guide

## Overview

This guide explains how to integrate the Claude Code Documentation Generation Extension with your Claude Code CLI installation to enable automatic documentation generation through slash commands and git hooks.

## Prerequisites

Before installing, ensure you have:

- **Claude Code CLI** installed and working
- **Node.js** 14.0.0 or higher
- **Git** 2.0 or higher
- **Python 3.7+** (for slash commands and hooks)
- Basic command line familiarity

### Verify Prerequisites

```bash
# Check Claude Code CLI
claude --version

# Check Node.js
node --version

# Check Python
python3 --version

# Check Git
git --version
```

## Installation Methods

### Method 1: Quick Setup (Recommended)

1. **Clone the repository to a permanent location**:
   ```bash
   # Choose a permanent location (e.g., ~/.claude-extensions/)
   mkdir -p ~/.claude-extensions
   cd ~/.claude-extensions
   
   # Clone the repository
   git clone https://github.com/yourusername/claude-code-doc-generation-ext.git
   cd claude-code-doc-generation-ext
   
   # Install dependencies
   npm install
   ```

2. **Make scripts executable**:
   ```bash
   chmod +x doc-generator.js
   chmod +x documentation-slash-command.py
   chmod +x claude-code-documentation-hooks.py
   ```

3. **Test the installation**:
   ```bash
   # Test the Node.js generator
   node doc-generator.js --help
   
   # Test the Python slash command handler
   python3 documentation-slash-command.py --help
   ```

### Method 2: Global Installation

1. **Install as a global npm package** (if you want system-wide access):
   ```bash
   # From the project directory
   npm install -g .
   
   # Or link for development
   npm link
   ```

2. **Verify global installation**:
   ```bash
   doc-last --help
   ```

## Setting Up Slash Commands

### Option A: Automatic Configuration

Run the provided setup script:

```bash
# From the project directory
python3 setup-claude-integration.py
```

This script will:
- Detect your Claude Code configuration directory
- Install the slash command handlers
- Set up appropriate permissions
- Create necessary configuration files

### Option B: Manual Configuration

1. **Locate your Claude Code configuration directory**:
   ```bash
   # Common locations:
   # macOS: ~/.claude/
   # Linux: ~/.config/claude/ or ~/.claude/
   # Windows: %APPDATA%/claude/ or %USERPROFILE%/.claude/
   
   # Find Claude config
   claude config show
   ```

2. **Create slash commands directory**:
   ```bash
   mkdir -p ~/.claude/slash-commands
   ```

3. **Copy or link the slash command script**:
   ```bash
   # Option 1: Copy the script
   cp documentation-slash-command.py ~/.claude/slash-commands/
   
   # Option 2: Create a symbolic link (recommended for development)
   ln -s $(pwd)/documentation-slash-command.py ~/.claude/slash-commands/doc-commands.py
   ```

4. **Create configuration file**:
   ```bash
   cat > ~/.claude/slash-commands/doc-commands.json << 'EOF'
   {
     "commands": {
       "doc-last": {
         "description": "Document files from the most recent git commit",
         "script": "doc-commands.py",
         "args": ["--mode", "last"]
       },
       "doc-recent": {
         "description": "Document recently modified files (last 5 minutes)",
         "script": "doc-commands.py", 
         "args": ["--mode", "recent"]
       },
       "doc-staged": {
         "description": "Document files currently staged in git",
         "script": "doc-commands.py",
         "args": ["--mode", "staged"]
       },
       "doc-all": {
         "description": "Document all supported files in the project (use with caution)",
         "script": "doc-commands.py",
         "args": ["--mode", "all"]
       }
     }
   }
   EOF
   ```

5. **Update the script with correct paths**:
   ```bash
   # Edit the Python script to point to your installation
   nano ~/.claude/slash-commands/doc-commands.py
   
   # Update the DOC_GENERATOR_PATH variable:
   DOC_GENERATOR_PATH = "/path/to/your/claude-code-doc-generation-ext/doc-generator.js"
   ```

## Setting Up Git Hooks (Optional)

Git hooks automatically generate documentation when you commit code.

### Install Pre-Commit Hook

1. **Copy the hook script**:
   ```bash
   # Navigate to your project's git repository
   cd /path/to/your/project
   
   # Copy the pre-commit hook
   cp ~/.claude-extensions/claude-code-doc-generation-ext/claude-code-documentation-hooks.py .git/hooks/pre-commit
   
   # Make it executable
   chmod +x .git/hooks/pre-commit
   ```

2. **Configure the hook**:
   ```bash
   # Edit the hook to point to your installation
   nano .git/hooks/pre-commit
   
   # Update the paths at the top of the file:
   DOC_GENERATOR_PATH = "/path/to/claude-code-doc-generation-ext/doc-generator.js"
   CLAUDE_COMMAND = "claude"  # or full path if needed
   ```

### Install Post-Commit Hook

For documentation generation after commits:

```bash
# Copy the post-commit hook
cp ~/.claude-extensions/claude-code-doc-generation-ext/claude-code-documentation-hooks.py .git/hooks/post-commit

# Make it executable  
chmod +x .git/hooks/post-commit

# Configure for post-commit mode
nano .git/hooks/post-commit
# Change MODE = "post-commit" in the file
```

## Configuration

### Environment Variables

Set these environment variables for optimal operation:

```bash
# Add to your ~/.bashrc, ~/.zshrc, or ~/.profile

# Path to the documentation generator
export CLAUDE_DOC_GENERATOR="/path/to/claude-code-doc-generation-ext/doc-generator.js"

# Claude Code CLI path (if not in system PATH)
export CLAUDE_CLI_PATH="/path/to/claude"

# Default options for documentation generation
export CLAUDE_DOC_OPTIONS="--verbose"

# Enable debug output
export CLAUDE_DOC_DEBUG=1
```

### Claude Code Configuration

Add to your Claude Code configuration:

```bash
# Edit Claude config
claude config edit

# Add these settings:
[documentation]
auto_generate = true
backup_enabled = true
enhance_with_ai = true
verbose_output = true

[extensions]
doc_generator = "/path/to/claude-code-doc-generation-ext"
```

## Testing the Installation

### Test Slash Commands

1. **Open Claude Code**:
   ```bash
   claude
   ```

2. **Test each slash command**:
   ```
   /doc-last --dry-run
   /doc-recent --help
   /doc-staged --verbose
   ```

3. **Verify output**:
   - Commands should execute without errors
   - Should show file analysis results
   - Should create backup files in dry-run mode

### Test Git Hooks

1. **Create a test file**:
   ```bash
   echo 'function testFunction() { return true; }' > test-file.js
   git add test-file.js
   ```

2. **Commit and observe**:
   ```bash
   git commit -m "Test documentation generation"
   # Should automatically generate documentation
   ```

3. **Verify results**:
   ```bash
   # Check if documentation was added
   cat test-file.js
   
   # Check for backup files
   ls -la .doc-last-backups/
   ```

## Troubleshooting

### Common Issues

#### 1. Slash Commands Not Found
```
Error: Command /doc-last not found
```

**Solutions**:
- Verify slash command configuration: `ls ~/.claude/slash-commands/`
- Check file permissions: `ls -la ~/.claude/slash-commands/`
- Restart Claude Code CLI
- Check Claude Code logs: `claude logs`

#### 2. Permission Denied Errors
```
Permission denied: ~/.claude/slash-commands/doc-commands.py
```

**Solutions**:
```bash
# Fix script permissions
chmod +x ~/.claude/slash-commands/doc-commands.py

# Fix directory permissions
chmod 755 ~/.claude/slash-commands/
```

#### 3. Node.js Module Not Found
```
Error: Cannot find module '@babel/parser'
```

**Solutions**:
```bash
# Reinstall dependencies
cd ~/.claude-extensions/claude-code-doc-generation-ext
npm install

# Or install globally
npm install -g @babel/parser @babel/traverse @babel/types
```

#### 4. Git Hook Not Executing
```
Git commit succeeds but no documentation generated
```

**Solutions**:
```bash
# Check hook permissions
ls -la .git/hooks/pre-commit

# Test hook manually
.git/hooks/pre-commit

# Check git configuration
git config core.hooksPath
```

#### 5. Claude Command Not Found
```
/bin/sh: claude: command not found
```

**Solutions**:
```bash
# Find Claude installation
which claude

# Update PATH in hook script or use full path
export PATH="/path/to/claude:$PATH"
```

### Debug Mode

Enable detailed debugging:

```bash
# Set debug environment variable
export CLAUDE_DOC_DEBUG=1

# Run with verbose output
/doc-last --verbose

# Check Claude Code logs
claude logs --tail -f
```

### Log Files

Check these locations for error information:
- Claude Code logs: `~/.claude/logs/`
- System logs: `/var/log/` (Linux) or Console.app (macOS)
- Hook execution: `.git/hooks/doc-last.log` (if created)

## Uninstallation

To remove the integration:

### Remove Slash Commands
```bash
# Remove slash command files
rm -rf ~/.claude/slash-commands/doc-commands.*

# Remove from Claude config
claude config edit
# Remove [documentation] and [extensions] sections
```

### Remove Git Hooks
```bash
# Remove from specific project
rm .git/hooks/pre-commit .git/hooks/post-commit

# Remove globally (if installed)
git config --global --unset core.hooksPath
```

### Remove Installation
```bash
# Remove the extension directory
rm -rf ~/.claude-extensions/claude-code-doc-generation-ext

# Remove global npm package (if installed)
npm uninstall -g claude-code-doc-generator
```

## Advanced Configuration

### Custom Slash Commands

Create additional slash commands by adding to the configuration:

```json
{
  "commands": {
    "doc-typescript": {
      "description": "Document only TypeScript files",
      "script": "doc-commands.py",
      "args": ["--mode", "custom", "--filter", "*.ts,*.tsx"]
    },
    "doc-preview": {
      "description": "Preview documentation changes without modifying files",
      "script": "doc-commands.py",
      "args": ["--mode", "last", "--dry-run"]
    }
  }
}
```

### Project-Specific Configuration

Create `.claude-doc-config.json` in your project root:

```json
{
  "enabled": true,
  "auto_enhance": true,
  "backup_enabled": true,
  "exclude_patterns": [
    "node_modules/**",
    "dist/**",
    "*.min.js"
  ],
  "include_patterns": [
    "src/**/*.js",
    "src/**/*.ts",
    "lib/**/*.js"
  ],
  "hooks": {
    "pre_commit": true,
    "post_commit": false
  }
}
```

### CI/CD Integration

For automated documentation in CI/CD pipelines:

```yaml
# .github/workflows/documentation.yml
name: Generate Documentation
on: [push, pull_request]

jobs:
  document:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'
      - name: Install dependencies
        run: npm install
      - name: Generate documentation
        run: |
          git clone https://github.com/yourusername/claude-code-doc-generation-ext.git
          cd claude-code-doc-generation-ext
          npm install
          node doc-generator.js --dry-run
```

## Support

### Getting Help

1. **Check the documentation**: [docs/INDEX.md](docs/INDEX.md)
2. **Review troubleshooting**: This guide's troubleshooting section
3. **Check project issues**: GitHub issues page
4. **Enable debug mode**: Use `--verbose` and check logs

### Reporting Issues

When reporting problems, include:
- Claude Code version: `claude --version`
- Node.js version: `node --version`
- Operating system and version
- Complete error messages
- Steps to reproduce the issue
- Configuration files (without sensitive information)

---

**Next Steps**: After successful installation, check out the [Getting Started Guide](docs/guides/GETTING_STARTED.md) to learn how to use the documentation generation features effectively.