# Claude Code Documentation Generation Extension

A powerful documentation generator for Claude Code that automatically creates JSDoc comments and Python docstrings for your code. This extension helps maintain comprehensive documentation by detecting recently modified files and generating appropriate documentation based on the code structure.

## 🚀 Features

- **Automatic Documentation Generation**: Generate JSDoc for JavaScript/TypeScript and docstrings for Python
- **Smart File Detection**: Automatically detects recently modified files using git or filesystem timestamps
- **AST-Based Analysis**: Uses Abstract Syntax Tree parsing for accurate code analysis
- **Multiple Commands**: Various slash commands for different documentation workflows
- **Claude Integration**: Optional enhancement using Claude AI for more intelligent documentation
- **Safe Operation**: Creates backups before modifying files
- **Extensible**: Support for multiple programming languages and documentation formats

## 📦 Installation

### Quick Setup with Claude Code Integration

For automatic setup with Claude Code CLI integration:

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-code-doc-generation-ext.git
cd claude-code-doc-generation-ext

# Run the automatic setup script
python3 setup-claude-integration.py
```

This will:
- Install all dependencies
- Configure slash commands (/doc-last, /doc-recent, /doc-staged, /doc-all)
- Set up git hooks templates
- Test the installation
- Create environment configuration

### Manual Installation

For manual setup or standalone usage:

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-code-doc-generation-ext.git
cd claude-code-doc-generation-ext

# Install dependencies
npm install

# Make the commands executable
chmod +x doc-generator.js
chmod +x documentation-slash-command.py
chmod +x setup-claude-integration.py
```

### Detailed Installation Guide

For complete installation instructions, including troubleshooting and advanced configuration options, see:

**[📖 Claude Code Installation Guide](./CLAUDE_CODE_INSTALLATION.md)**

This comprehensive guide covers:
- Prerequisites and system requirements
- Step-by-step Claude Code integration
- Slash command configuration
- Git hooks setup
- Troubleshooting common issues
- Advanced configuration options

## 🛠️ Usage

### Basic Commands

The extension provides several slash commands for different documentation scenarios:

#### `/doc-last`
Documents files from the most recent git commit. If no commit is found, falls back to recently modified files.

```bash
/doc-last
```

#### `/doc-recent`
Documents files modified in the last 5 minutes.

```bash
/doc-recent
```

#### `/doc-staged`
Documents files currently staged in git.

```bash
/doc-staged
```

#### `/doc-all`
Documents all supported files in the project (use with caution on large projects).

```bash
/doc-all
```

### Command Options

All commands support the following options:

- `--help, -h`: Show help message
- `--verbose, -v`: Show detailed output during processing
- `--dry-run, -n`: Preview changes without modifying files
- `--no-enhance`: Skip Claude AI enhancement step
- `--version`: Show version information

### Examples

```bash
# Preview documentation changes
/doc-last --dry-run

# Generate documentation with verbose output
/doc-last --verbose

# Document staged files without AI enhancement
/doc-staged --no-enhance
```

## 📚 Supported Languages

### JavaScript/TypeScript
- **Extensions**: `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`
- **Documentation Format**: JSDoc
- **Detects**: Functions, arrow functions, classes, methods, exports

### Python
- **Extensions**: `.py`, `.pyw`
- **Documentation Format**: Google-style docstrings
- **Detects**: Functions, methods, classes

## 🏗️ Architecture

The extension consists of several key components:

1. **doc-generator.js**: Main documentation generator using Babel AST parser
2. **documentation-slash-command.py**: Python implementation with additional features
3. **claude-code-documentation-hooks.py**: Git hooks for automatic documentation
4. **Test samples**: Example files for testing documentation generation

## 🔧 Configuration

Currently configured through command-line options. Future versions will support:
- Configuration files
- Custom documentation templates
- File pattern exclusions
- Documentation style preferences

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Documentation

### Getting Started
- [Claude Code Installation Guide](./CLAUDE_CODE_INSTALLATION.md) - Complete installation with Claude Code integration
- [Getting Started Guide](./docs/guides/GETTING_STARTED.md) - Basic usage and first steps
- [Usage Guide](./USAGE.md) - Detailed usage instructions and examples

### Technical Reference
- [API Documentation](./docs/API.md) - Complete API reference for programmatic usage
- [Architecture Guide](./ARCHITECTURE.md) - System design and component overview
- [Core Generator Module](./docs/modules/core-generator.md) - Detailed module documentation

### Tutorials & Examples
- [Advanced Usage Tutorial](./docs/tutorials/advanced-usage.md) - Complex scenarios and workflows
- [Basic Tutorial](./docs/tutorials/getting-started.md) - Step-by-step walkthrough

### Project Information
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md) - Technical implementation details
- [Claude Code Integration](./CLAUDE_CODE_INTEGRATION.md) - Integration with Claude Code CLI
- [Completed Features](./COMPLETED_TODOS.md) - Feature completion tracking

## 🐛 Known Issues

See [BUGS.md](./BUGS.md) for known issues and their workarounds.

## 📋 Project Status

See [TODO.md](./TODO.md) for planned features and improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for use with [Claude Code](https://claude.ai/code)
- Uses [Babel](https://babeljs.io/) for JavaScript/TypeScript parsing
- Inspired by documentation best practices from the developer community