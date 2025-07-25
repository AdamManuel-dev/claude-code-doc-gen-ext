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

The extension is designed to work with Claude Code. To install:

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-code-doc-generation-ext.git
cd claude-code-doc-generation-ext

# Install dependencies
npm install

# Make the commands executable
chmod +x doc-generator.js
chmod +x documentation-slash-command.py
```

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

- [Usage Guide](./USAGE.md) - Detailed usage instructions and examples
- [API Documentation](./docs/API.md) - Complete API reference
- [Tutorials](./docs/tutorials/) - Step-by-step tutorials
- [Troubleshooting](./docs/TROUBLESHOOTING.md) - Common issues and solutions

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