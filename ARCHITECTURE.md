# System Architecture

## Overview

The Claude Code Documentation Generation Extension is a modular system designed to automatically generate comprehensive documentation for JavaScript, TypeScript, and Python codebases. The architecture emphasizes modularity, extensibility, and integration with Claude Code's workflow.

## Design Philosophy

- **AST-First Approach**: Uses Abstract Syntax Tree parsing for accurate code analysis rather than regex-based parsing
- **Git Integration**: Leverages git history to identify recently changed files for targeted documentation
- **Safe Operations**: Always creates backups before modifying files
- **AI Enhancement**: Optional integration with Claude AI for intelligent documentation improvement
- **Multi-Language Support**: Extensible architecture supporting multiple programming languages

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code CLI                              │
│                  (Slash Commands)                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│               Documentation Router                              │
│            (documentation-slash-command.py)                     │
│  • Command parsing and validation                               │
│  • File discovery coordination                                  │
│  • Multi-language dispatch                                      │
└─────────────┬───────────────────────┬───────────────────────────┘
              │                       │
              ▼                       ▼
┌─────────────────────────┐ ┌─────────────────────────┐
│   JavaScript/TypeScript │ │      Python Handler     │
│     Documentation       │ │   (Future Extension)    │
│     (doc-generator.js)  │ │                         │
└─────────────┬───────────┘ └─────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Core Processing Pipeline                       │
├─────────────────────────────────────────────────────────────────┤
│  1. File Discovery     │  Git integration + filesystem scan     │
│  2. AST Parsing        │  Babel parser with plugin ecosystem    │
│  3. Function Analysis  │  Extract signatures, params, types     │
│  4. Documentation Gen  │  Template-based JSDoc generation       │
│  5. File Modification  │  Safe insertion with backup system     │
│  6. AI Enhancement     │  Optional Claude AI post-processing    │
└─────────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Output Generation                            │
├─────────────────────────────────────────────────────────────────┤
│  • Modified source files with JSDoc comments                   │
│  • Backup files (.doc-last-backups/)                           │
│  • Documentation report (documentation-report.md)              │
│  • Optional enhanced documentation via Claude AI               │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Command Invocation
```
User runs /doc-last command
        ↓
Claude Code executes documentation-slash-command.py
        ↓
Router determines file scope and language handlers
```

### 2. File Discovery
```
Git Repository Detection
        ↓
Changed Files Discovery (last commit, staged, unstaged)
        ↓
Fallback to Recently Modified Files (if no git changes)
        ↓
File Filtering (supported extensions only)
```

### 3. AST Processing Pipeline
```
Source File → Babel Parser → AST
        ↓
AST Traversal (identify functions, classes, methods)
        ↓
Documentation Status Analysis (has JSDoc or not)
        ↓
Function Metadata Extraction
```

### 4. Documentation Generation
```
Function Metadata → Template Engine → JSDoc Comment
        ↓
Intelligent Description Generation (based on naming patterns)
        ↓
Parameter and Return Type Documentation
        ↓
Special Case Handling (React, async/await, generators)
```

### 5. File Modification
```
Backup Creation → Safe File Writing → Report Generation
        ↓
Optional Claude AI Enhancement
        ↓
Final Documentation Report
```

## Key Components

### DocumentationGenerator Class (doc-generator.js)

**Core Methods:**
- `getFilesToProcess()`: File discovery with git integration
- `parseFile()`: AST-based code analysis using Babel
- `generateJSDoc()`: Intelligent JSDoc comment generation
- `run()`: Main orchestration method

**Responsibilities:**
- Abstract Syntax Tree parsing
- Function signature extraction
- JSDoc template generation
- File backup and modification
- Integration with Claude AI enhancement

### File Discovery System

**Strategy Pattern:**
1. **Git-based Discovery**: Primary method for teams using version control
2. **Filesystem Discovery**: Fallback for non-git repositories
3. **Extension Filtering**: Only process supported file types

**Supported Extensions:**
- JavaScript: `.js`, `.jsx`, `.mjs`, `.cjs`
- TypeScript: `.ts`, `.tsx`
- Python: `.py`, `.pyw` (future)

### AST Analysis Engine

**Babel Integration:**
- Full plugin ecosystem support
- TypeScript parsing capabilities
- Modern JavaScript feature support
- JSX and React component detection

**Function Detection:**
- Function declarations
- Arrow functions
- Class methods (public, private, static)
- Object methods
- Generator functions
- Async functions

### Template Generation System

**Pattern Recognition:**
- Getter/setter method patterns
- Event handler patterns
- React lifecycle method patterns
- Constructor patterns
- Utility function patterns

**Output Format:**
- Standard JSDoc format
- TypeScript-compatible annotations
- Parameter documentation with types
- Return value documentation
- Error handling documentation

## Technology Stack

### Core Technologies
- **Runtime**: Node.js 14+
- **Parser**: Babel AST (@babel/parser, @babel/traverse, @babel/types)
- **File System**: Node.js fs module with backup management
- **Git Integration**: Child process execution of git commands
- **Process Management**: Node.js child_process for external tool integration

### Python Integration
- **Command Router**: Python script for multi-language support
- **Future Extensions**: Python AST parsing, docstring generation

### External Integrations
- **Claude Code CLI**: Primary interface for user interaction
- **Git**: Version control integration for file discovery
- **Claude AI**: Optional documentation enhancement

## Security Considerations

### File Safety
- **Backup System**: All files backed up before modification
- **Atomic Operations**: File writes are atomic to prevent corruption
- **Permission Checking**: Respects file system permissions
- **Dry-run Mode**: Preview mode for safe testing

### Input Validation
- **File Path Sanitization**: Prevents directory traversal attacks
- **Extension Validation**: Only processes allowlisted file types
- **Content Validation**: AST parsing validates JavaScript syntax

### External Command Execution
- **Git Command Isolation**: Uses specific git commands with minimal privileges
- **Claude AI Integration**: Optional and user-controlled
- **No Arbitrary Code Execution**: All external commands are predefined

## Performance Characteristics

### File Processing
- **Incremental Processing**: Only processes changed files
- **Parallel Analysis**: Concurrent file analysis where possible
- **Memory Efficient**: Streams large files instead of loading entirely
- **Caching**: AST parsing results cached during processing

### Scalability
- **Repository Size**: Handles repositories with thousands of files
- **File Size**: Efficiently processes large individual files
- **Concurrent Operations**: Multiple file processing with resource limits

## Extension Points

### Language Support
- **Plugin Architecture**: New language parsers can be added
- **Template System**: Customizable documentation templates
- **Pattern Recognition**: Extensible function naming pattern system

### Integration Points
- **IDE Integration**: Compatible with VS Code and other editors
- **CI/CD Integration**: Can be run in automated pipelines
- **Custom Workflows**: Configurable via command-line options

## Error Handling Strategy

### Graceful Degradation
- **Parser Errors**: Continue processing other files if one fails
- **File Access Errors**: Skip inaccessible files with warnings
- **Git Errors**: Fallback to filesystem-based discovery

### User Feedback
- **Color-coded Output**: Visual feedback with status indicators
- **Verbose Mode**: Detailed logging for troubleshooting
- **Error Reporting**: Clear error messages with resolution suggestions

## Future Architecture Evolution

### Planned Enhancements
1. **Configuration System**: YAML/JSON configuration files
2. **Custom Templates**: User-defined documentation templates
3. **Plugin System**: Third-party extension support
4. **Web Interface**: Browser-based documentation review
5. **Integration APIs**: REST API for external tool integration

### Scalability Improvements
1. **Distributed Processing**: Multi-process file handling
2. **Caching Layer**: Persistent AST and metadata caching
3. **Incremental Updates**: Only re-process changed functions
4. **Streaming Processing**: Handle extremely large codebases

This architecture provides a solid foundation for automated documentation generation while maintaining flexibility for future enhancements and integrations.