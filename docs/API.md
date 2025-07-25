# API Reference

## Overview

The Claude Code Documentation Generation Extension provides a comprehensive Node.js API for programmatic documentation generation. Built around the `DocumentationGenerator` class, it offers AST-based analysis, intelligent JSDoc generation, and seamless integration with git workflows.

**Key Features:**
- AST-based code analysis using Babel parser
- Intelligent JSDoc comment generation with pattern recognition
- Git integration for file discovery
- Safe file modification with automatic backups
- Optional Claude AI enhancement
- TypeScript and modern JavaScript support

## Table of Contents

- [DocumentationGenerator Class](#documentationgenerator-class)
- [AST Parser Methods](#ast-parser-methods)
- [File Detection Methods](#file-detection-methods)
- [Documentation Generation Methods](#documentation-generation-methods)
- [Utility Functions](#utility-functions)
- [Error Handling](#error-handling)

## DocumentationGenerator Class

The main class for generating documentation.

### Constructor

```javascript
new DocumentationGenerator(options)
```

Creates a new instance of the DocumentationGenerator.

#### Parameters

- `options` (Object): Configuration options
  - `verbose` (boolean): Enable verbose output. Default: `false`
  - `dryRun` (boolean): Preview mode without file modifications. Default: `false`
  - `noEnhance` (boolean): Skip Claude AI enhancement. Default: `false`

#### Example

```javascript
const generator = new DocumentationGenerator({
  verbose: true,
  dryRun: false,
  noEnhance: false
});
```

### Methods

#### getFilesToProcess()

Retrieves files that need documentation based on git status or recent modifications.

```javascript
getFilesToProcess(): string[]
```

**Returns**: Array of file paths to process

**Example**:
```javascript
const files = generator.getFilesToProcess();
console.log(`Found ${files.length} files to document`);
```

#### processFile(filePath)

Processes a single file and generates documentation.

```javascript
processFile(filePath: string): ProcessResult
```

**Parameters**:
- `filePath` (string): Path to the file to process

**Returns**: ProcessResult object containing:
- `success` (boolean): Whether processing succeeded
- `functionsFound` (number): Total functions found
- `functionsDocumented` (number): Functions that were documented
- `error` (string|null): Error message if failed

**Example**:
```javascript
const result = generator.processFile('./src/utils.js');
if (result.success) {
  console.log(`Documented ${result.functionsDocumented} functions`);
}
```

#### analyzeFile(filePath, content)

Analyzes a file's AST to find undocumented functions.

```javascript
analyzeFile(filePath: string, content: string): AnalysisResult
```

**Parameters**:
- `filePath` (string): Path to the file
- `content` (string): File content

**Returns**: AnalysisResult object containing:
- `undocumentedItems` (Array): Items needing documentation
- `totalItems` (number): Total documentable items found

#### generateJSDoc(funcInfo)

Generates JSDoc comment for a function.

```javascript
generateJSDoc(funcInfo: FunctionInfo): string
```

**Parameters**:
- `funcInfo` (Object): Function information
  - `name` (string): Function name
  - `params` (Array): Parameter information
  - `isAsync` (boolean): Whether function is async
  - `isGenerator` (boolean): Whether function is generator
  - `leadingComments` (Array): Existing comments

**Returns**: Generated JSDoc comment string

**Example**:
```javascript
const jsdoc = generator.generateJSDoc({
  name: 'calculateTotal',
  params: [{name: 'items'}, {name: 'taxRate'}],
  isAsync: false,
  isGenerator: false
});
```

## AST Parser Methods

### parseJavaScriptFile(content, filePath)

Parses JavaScript/TypeScript content into an AST.

```javascript
parseJavaScriptFile(content: string, filePath: string): AST
```

**Parameters**:
- `content` (string): File content
- `filePath` (string): File path (used for determining parser options)

**Returns**: Babel AST object

### extractFunctionInfo(path)

Extracts function information from an AST node path.

```javascript
extractFunctionInfo(path: NodePath): FunctionInfo
```

**Parameters**:
- `path` (NodePath): Babel traverse path object

**Returns**: Function information object

## File Detection Methods

### isGitRepository()

Checks if the current directory is a git repository.

```javascript
isGitRepository(): boolean
```

**Returns**: `true` if in a git repository, `false` otherwise

### getGitChangedFiles()

Gets files changed in git (last commit, staged, unstaged).

```javascript
getGitChangedFiles(): string[]
```

**Returns**: Array of changed file paths

### getRecentlyModifiedFiles(minutes)

Gets files modified within the specified time period.

```javascript
getRecentlyModifiedFiles(minutes: number = 5): string[]
```

**Parameters**:
- `minutes` (number): Time window in minutes. Default: 5

**Returns**: Array of recently modified file paths

### filterSupportedFiles(files)

Filters files to only include supported extensions.

```javascript
filterSupportedFiles(files: string[]): string[]
```

**Parameters**:
- `files` (Array): File paths to filter

**Returns**: Filtered array of supported file paths

## Documentation Generation Methods

### insertDocumentation(content, position, documentation)

Inserts documentation at the specified position in the content.

```javascript
insertDocumentation(content: string, position: number, documentation: string): string
```

**Parameters**:
- `content` (string): Original file content
- `position` (number): Character position to insert at
- `documentation` (string): Documentation to insert

**Returns**: Modified content with documentation inserted

### createBackup(filePath)

Creates a backup of a file before modification.

```javascript
createBackup(filePath: string): string
```

**Parameters**:
- `filePath` (string): Path to file to backup

**Returns**: Path to backup file

### enhanceWithClaude(filePath)

Enhances documentation using Claude AI (if available).

```javascript
enhanceWithClaude(filePath: string): Promise<boolean>
```

**Parameters**:
- `filePath` (string): Path to file to enhance

**Returns**: Promise resolving to success boolean

## Utility Functions

### formatParameter(param)

Formats a parameter for JSDoc.

```javascript
formatParameter(param: Parameter): string
```

**Parameters**:
- `param` (Object): Parameter information
  - `name` (string): Parameter name
  - `type` (string|null): Parameter type
  - `optional` (boolean): Whether parameter is optional
  - `defaultValue` (any): Default value

**Returns**: Formatted JSDoc parameter string

### getIndentation(content, position)

Determines the indentation at a specific position.

```javascript
getIndentation(content: string, position: number): string
```

**Parameters**:
- `content` (string): File content
- `position` (number): Position in content

**Returns**: Indentation string (spaces/tabs)

### log(message, level)

Logs a message with color coding.

```javascript
log(message: string, level: 'info'|'success'|'warning'|'error' = 'info'): void
```

**Parameters**:
- `message` (string): Message to log
- `level` (string): Log level

## Error Handling

The API uses standard JavaScript error handling with custom error types:

### DocumentationError

Base error class for documentation-related errors.

```javascript
class DocumentationError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}
```

### Error Codes

- `PARSE_ERROR`: Failed to parse file AST
- `FILE_NOT_FOUND`: File does not exist
- `UNSUPPORTED_FILE`: File type not supported
- `WRITE_ERROR`: Failed to write to file
- `BACKUP_ERROR`: Failed to create backup

### Example Error Handling

```javascript
try {
  const result = generator.processFile('./src/app.js');
  if (!result.success) {
    console.error(`Failed: ${result.error}`);
  }
} catch (error) {
  if (error instanceof DocumentationError) {
    console.error(`Documentation error [${error.code}]: ${error.message}`);
  } else {
    console.error('Unexpected error:', error);
  }
}
```

## Complete Example

```javascript
const { DocumentationGenerator } = require('./doc-generator');

async function documentProject() {
  const generator = new DocumentationGenerator({
    verbose: true,
    dryRun: false
  });
  
  // Get files to process
  const files = generator.getFilesToProcess();
  
  console.log(`Found ${files.length} files to document`);
  
  // Process each file
  for (const file of files) {
    try {
      const result = generator.processFile(file);
      
      if (result.success) {
        console.log(`✓ ${file}: Documented ${result.functionsDocumented}/${result.functionsFound} functions`);
      } else {
        console.error(`✗ ${file}: ${result.error}`);
      }
    } catch (error) {
      console.error(`Failed to process ${file}:`, error.message);
    }
  }
  
  // Generate report
  generator.generateReport();
}

// Run the documentation
documentProject().catch(console.error);
```

## TypeScript Support

The API is written in JavaScript but includes TypeScript type definitions for better IDE support:

```typescript
interface DocumentationOptions {
  verbose?: boolean;
  dryRun?: boolean;
  noEnhance?: boolean;
}

interface ProcessResult {
  success: boolean;
  functionsFound: number;
  functionsDocumented: number;
  error?: string;
}

interface FunctionInfo {
  name: string;
  params: Parameter[];
  isAsync: boolean;
  isGenerator: boolean;
  leadingComments?: Comment[];
}

class DocumentationGenerator {
  constructor(options?: DocumentationOptions);
  getFilesToProcess(): string[];
  processFile(filePath: string): ProcessResult;
  // ... other methods
}
```

## Integration with Claude Code

The API can be integrated with Claude Code through:

1. **Slash Commands**: Already implemented in `documentation-slash-command.py`
2. **Git Hooks**: Use `claude-code-documentation-hooks.py`
3. **Custom Scripts**: Import and use the API directly

Example Claude Code integration:

```javascript
// In a Claude Code extension
const { DocumentationGenerator } = require('claude-code-doc-generator');

export function activate(context) {
  context.registerCommand('doc-last', async () => {
    const generator = new DocumentationGenerator();
    const files = generator.getFilesToProcess();
    
    for (const file of files) {
      await generator.processFile(file);
    }
  });
}
```