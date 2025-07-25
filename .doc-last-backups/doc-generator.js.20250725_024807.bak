#!/usr/bin/env node
/**
 * Claude Code Documentation Generator - Node.js Implementation
 * 
 * Uses proper AST parsing for JavaScript, TypeScript, JSX, and TSX files
 * Requires: @babel/parser, @babel/traverse, @babel/types
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const t = require('@babel/types');

// ANSI color codes
const Colors = {
  HEADER: '\x1b[95m',
  BLUE: '\x1b[94m',
  CYAN: '\x1b[96m',
  GREEN: '\x1b[92m',
  WARNING: '\x1b[93m',
  FAIL: '\x1b[91m',
  ENDC: '\x1b[0m',
  BOLD: '\x1b[1m',
  UNDERLINE: '\x1b[4m'
};

// Supported file extensions
const SUPPORTED_EXTENSIONS = {
  '.js': 'jsdoc',
  '.jsx': 'jsdoc',
  '.ts': 'jsdoc',
  '.tsx': 'jsdoc',
  '.mjs': 'jsdoc',
  '.cjs': 'jsdoc'
};

class DocumentationGenerator {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.dryRun = options.dryRun || false;
    this.noEnhance = options.noEnhance || false;
  }

  /**
   * Get recently modified files from git or filesystem
   */
  getFilesToProcess() {
    let files = [];
    
    // Try git first
    if (this.isGitRepository()) {
      if (this.verbose) {
        console.log(`${Colors.BLUE}  Git repository detected${Colors.ENDC}`);
      }
      
      files = this.getGitChangedFiles();
      
      if (files.length === 0) {
        console.log(`${Colors.WARNING}  No changed files in git, checking recently modified files...${Colors.ENDC}`);
        files = this.getRecentlyModifiedFiles();
      }
    } else {
      if (this.verbose) {
        console.log(`${Colors.BLUE}  Not a git repository, checking recently modified files...${Colors.ENDC}`);
      }
      files = this.getRecentlyModifiedFiles();
    }
    
    return files;
  }

  isGitRepository() {
    try {
      execSync('git rev-parse --git-dir', { stdio: 'ignore' });
      return true;
    } catch {
      return false;
    }
  }

  getGitChangedFiles() {
    const files = new Set();
    
    try {
      // Files from last commit
      const lastCommit = execSync('git diff --name-only HEAD~1 HEAD', { encoding: 'utf8' })
        .trim()
        .split('\n')
        .filter(Boolean);
      lastCommit.forEach(f => files.add(f));
    } catch {}
    
    try {
      // Unstaged changes
      const unstaged = execSync('git diff --name-only', { encoding: 'utf8' })
        .trim()
        .split('\n')
        .filter(Boolean);
      unstaged.forEach(f => files.add(f));
    } catch {}
    
    try {
      // Staged changes
      const staged = execSync('git diff --cached --name-only', { encoding: 'utf8' })
        .trim()
        .split('\n')
        .filter(Boolean);
      staged.forEach(f => files.add(f));
    } catch {}
    
    return Array.from(files).filter(file => {
      const ext = path.extname(file).toLowerCase();
      return SUPPORTED_EXTENSIONS[ext] && fs.existsSync(file);
    });
  }

  getRecentlyModifiedFiles(minutes = 5) {
    const cutoffTime = Date.now() - (minutes * 60 * 1000);
    const files = [];
    
    const scanDir = (dir) => {
      try {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        
        for (const entry of entries) {
          const fullPath = path.join(dir, entry.name);
          
          if (entry.isDirectory() && !entry.name.startsWith('.')) {
            scanDir(fullPath);
          } else if (entry.isFile()) {
            const ext = path.extname(entry.name).toLowerCase();
            if (SUPPORTED_EXTENSIONS[ext]) {
              const stats = fs.statSync(fullPath);
              if (stats.mtimeMs > cutoffTime) {
                files.push(path.relative(process.cwd(), fullPath));
              }
            }
          }
        }
      } catch {}
    };
    
    scanDir('.');
    return files;
  }

  /**
   * Parse JavaScript/TypeScript file using Babel
   */
  parseFile(filepath) {
    const content = fs.readFileSync(filepath, 'utf8');
    const lines = content.split('\n');
    
    // Determine if it's TypeScript
    const isTypeScript = filepath.endsWith('.ts') || filepath.endsWith('.tsx');
    
    try {
      const ast = parser.parse(content, {
        sourceType: 'module',
        plugins: [
          'jsx',
          ...(isTypeScript ? ['typescript'] : []),
          'decorators-legacy',
          'classProperties',
          'classPrivateProperties',
          'classPrivateMethods',
          'asyncGenerators',
          'objectRestSpread',
          'dynamicImport',
          'optionalChaining',
          'nullishCoalescingOperator',
          'exportDefaultFrom',
          'exportNamespaceFrom',
          'optionalCatchBinding',
          'throwExpressions',
          'logicalAssignment',
          'numericSeparator',
          'bigInt'
        ]
      });
      
      const functions = [];
      let currentClass = null;
      let classDepth = 0;
      
      const self = this;
      
      traverse(ast, {
        enter(path) {
          const node = path.node;
          
          // Track class entry/exit
          if (t.isClassDeclaration(node) || t.isClassExpression(node)) {
            classDepth++;
            currentClass = node.id ? node.id.name : '<anonymous>';
            
            const hasDoc = self.hasJSDoc(node, lines);
            
            functions.push({
              name: currentClass,
              line: node.loc.start.line,
              type: 'class',
              hasDoc,
              signature: `class ${currentClass}`,
              params: [],
              decorators: self.getDecorators(node)
            });
          }
          
          // Function declarations
          if (t.isFunctionDeclaration(node)) {
            const funcInfo = self.extractFunctionInfo(node, path, lines, currentClass);
            if (funcInfo) functions.push(funcInfo);
          }
          
          // Function expressions and arrow functions
          if (t.isFunctionExpression(node) || t.isArrowFunctionExpression(node)) {
            const funcInfo = self.extractFunctionInfo(node, path, lines, currentClass);
            if (funcInfo) functions.push(funcInfo);
          }
          
          // Class methods
          if (t.isClassMethod(node) || t.isClassPrivateMethod(node)) {
            const funcInfo = self.extractMethodInfo(node, lines);
            if (funcInfo) functions.push(funcInfo);
          }
          
          // Object methods
          if (t.isObjectMethod(node)) {
            const funcInfo = self.extractMethodInfo(node, lines);
            if (funcInfo) functions.push(funcInfo);
          }
        },
        exit(path) {
          if (t.isClassDeclaration(path.node) || t.isClassExpression(path.node)) {
            classDepth--;
            if (classDepth === 0) {
              currentClass = null;
            }
          }
        }
      });
      
      return functions;
      
    } catch (error) {
      console.error(`${Colors.WARNING}Warning: Could not parse ${filepath}: ${error.message}${Colors.ENDC}`);
      return [];
    }
  }
  
  hasJSDoc(node, lines) {
    if (!node.loc) return false;
    
    const lineAbove = node.loc.start.line - 2; // -1 for 0-indexed, -1 for line above
    if (lineAbove >= 0 && lineAbove < lines.length) {
      const line = lines[lineAbove];
      return line.includes('*/');
    }
    
    // Check leadingComments
    if (node.leadingComments) {
      return node.leadingComments.some(comment => 
        comment.type === 'CommentBlock' && comment.value.startsWith('*')
      );
    }
    
    return false;
  }
  
  getDecorators(node) {
    if (!node.decorators) return [];
    return node.decorators.map(dec => {
      if (t.isIdentifier(dec.expression)) {
        return dec.expression.name;
      }
      if (t.isCallExpression(dec.expression) && t.isIdentifier(dec.expression.callee)) {
        return dec.expression.callee.name;
      }
      return 'decorator';
    });
  }
  
  extractFunctionInfo(node, path, lines, currentClass) {
    let name = '<anonymous>';
    let type = currentClass ? 'method' : 'function';
    
    // Get function name
    if (node.id) {
      name = node.id.name;
    } else {
      // Check parent for variable declarator
      const parent = path.parent;
      if (t.isVariableDeclarator(parent) && t.isIdentifier(parent.id)) {
        name = parent.id.name;
      } else if (t.isProperty(parent) || t.isObjectProperty(parent)) {
        if (t.isIdentifier(parent.key)) {
          name = parent.key.name;
        } else if (t.isStringLiteral(parent.key)) {
          name = parent.key.value;
        }
      } else if (t.isAssignmentExpression(parent) && t.isIdentifier(parent.left)) {
        name = parent.left.name;
      }
    }
    
    // Skip anonymous functions
    if (name === '<anonymous>') return null;
    
    // Get parameters
    const params = node.params.map(param => {
      if (t.isIdentifier(param)) return param.name;
      if (t.isRestElement(param) && t.isIdentifier(param.argument)) return `...${param.argument.name}`;
      if (t.isObjectPattern(param)) return '{}';
      if (t.isArrayPattern(param)) return '[]';
      if (t.isAssignmentPattern(param) && t.isIdentifier(param.left)) return param.left.name;
      return 'param';
    });
    
    // Check for JSDoc
    const hasDoc = this.hasJSDoc(node, lines);
    
    // Build signature
    const isAsync = node.async || false;
    const isGenerator = node.generator || false;
    const asyncPrefix = isAsync ? 'async ' : '';
    const generatorSuffix = isGenerator ? '*' : '';
    
    let signature;
    if (t.isArrowFunctionExpression(node)) {
      const paramStr = params.length === 1 && !params[0].includes('.') ? params[0] : `(${params.join(', ')})`;
      signature = `${asyncPrefix}${paramStr} =>`;
      if (path.parent && t.isVariableDeclarator(path.parent)) {
        signature = `const ${name} = ${signature}`;
      }
    } else {
      signature = `${asyncPrefix}function${generatorSuffix} ${name}(${params.join(', ')})`;
    }
    
    return {
      name,
      line: node.loc.start.line,
      type,
      hasDoc,
      signature,
      params,
      isAsync,
      isGenerator,
      decorators: []
    };
  }
  
  extractMethodInfo(node, lines) {
    let name = '<anonymous>';
    
    if (t.isIdentifier(node.key)) {
      name = node.key.name;
    } else if (t.isStringLiteral(node.key)) {
      name = node.key.value;
    } else if (t.isPrivateName(node.key)) {
      name = '#' + node.key.id.name;
    }
    
    // Get parameters
    const params = node.params.map(param => {
      if (t.isIdentifier(param)) return param.name;
      if (t.isRestElement(param) && t.isIdentifier(param.argument)) return `...${param.argument.name}`;
      if (t.isObjectPattern(param)) return '{}';
      if (t.isArrayPattern(param)) return '[]';
      if (t.isAssignmentPattern(param) && t.isIdentifier(param.left)) return param.left.name;
      return 'param';
    });
    
    const hasDoc = this.hasJSDoc(node, lines);
    const isAsync = node.async || false;
    const isGenerator = node.generator || false;
    const isStatic = node.static || false;
    
    const asyncPrefix = isAsync ? 'async ' : '';
    const staticPrefix = isStatic ? 'static ' : '';
    const generatorSuffix = isGenerator ? '*' : '';
    
    const signature = `${staticPrefix}${asyncPrefix}${name}${generatorSuffix}(${params.join(', ')})`;
    
    return {
      name,
      line: node.loc.start.line,
      type: 'method',
      hasDoc,
      signature,
      params,
      isAsync,
      isGenerator,
      decorators: this.getDecorators(node)
    };
  }

  /**
   * Analyze a file for undocumented functions
   */
  analyzeFile(filepath) {
    const functions = this.parseFile(filepath);
    const undocumented = functions.filter(f => !f.hasDoc);
    
    return {
      filepath,
      total: functions.length,
      documented: functions.length - undocumented.length,
      undocumented: undocumented.length,
      functions,
      undocumentedFunctions: undocumented
    };
  }

  /**
   * Generate JSDoc for a function
   */
  generateJSDoc(func) {
    const lines = ['/**'];
    
    // Generate description based on function name
    const name = func.name;
    let description = '';
    
    if (name.startsWith('get')) {
      description = `Gets the ${this.camelToWords(name.substring(3))}.`;
    } else if (name.startsWith('set')) {
      description = `Sets the ${this.camelToWords(name.substring(3))}.`;
    } else if (name.startsWith('is') || name.startsWith('has')) {
      description = `Checks if ${this.camelToWords(name.substring(2))}.`;
    } else if (name === 'constructor') {
      description = 'Creates a new instance.';
    } else if (name.startsWith('handle')) {
      description = `Handles ${this.camelToWords(name.substring(6))} events.`;
    } else if (name.startsWith('on')) {
      description = `Handler for ${this.camelToWords(name.substring(2))} events.`;
    } else if (name === 'render') {
      description = 'Renders the component.';
    } else if (name === 'componentDidMount') {
      description = 'Lifecycle method called after component is mounted.';
    } else if (name === 'componentWillUnmount') {
      description = 'Lifecycle method called before component is unmounted.';
    } else if (name === 'shouldComponentUpdate') {
      description = 'Determines if component should re-render.';
    } else {
      description = `${this.camelToWords(name)}.`;
    }
    
    lines.push(` * ${description}`);
    
    // Add @param tags
    if (func.params && func.params.length > 0) {
      func.params.forEach(param => {
        if (param && !['props', 'state'].includes(param)) {
          let paramDesc = this.camelToWords(param.replace('...', ''));
          
          // Special handling for common React params
          if (param === 'event' || param === 'e') {
            lines.push(` * @param {Event} ${param} - The event object.`);
          } else if (param === 'children') {
            lines.push(` * @param {React.ReactNode} ${param} - The child elements.`);
          } else if (param.startsWith('...')) {
            lines.push(` * @param {...any} ${param} - The ${paramDesc}.`);
          } else {
            lines.push(` * @param {*} ${param} - The ${paramDesc}.`);
          }
        }
      });
    }
    
    // Add @returns tag
    if (func.type !== 'class' && func.name !== 'constructor') {
      if (func.name === 'render') {
        lines.push(' * @returns {React.ReactElement} The rendered element.');
      } else if (func.isGenerator) {
        lines.push(' * @yields {*} The yielded values.');
      } else {
        lines.push(' * @returns {*} The result.');
      }
    }
    
    // Add decorators note
    if (func.decorators && func.decorators.length > 0) {
      lines.push(` * @decorator ${func.decorators.join(', ')}`);
    }
    
    lines.push(' */');
    
    return lines.join('\n');
  }
  
  camelToWords(str) {
    if (!str) return '';
    return str
      .replace(/([A-Z])/g, ' $1')
      .replace(/^./, s => s.toLowerCase())
      .trim();
  }

  /**
   * Insert documentation into file
   */
  insertDocumentation(filepath, func, docText) {
    try {
      const content = fs.readFileSync(filepath, 'utf8');
      const lines = content.split('\n');
      
      // Get indentation from the target line
      const targetLine = lines[func.line - 1] || '';
      const indentMatch = targetLine.match(/^(\s*)/);
      const indent = indentMatch ? indentMatch[1] : '';
      
      // Add indentation to doc lines
      const docLines = docText.split('\n').map(line => 
        line ? indent + line : ''
      );
      
      // Insert documentation
      lines.splice(func.line - 1, 0, ...docLines);
      
      // Write back
      fs.writeFileSync(filepath, lines.join('\n'));
      return true;
      
    } catch (error) {
      console.error(`${Colors.FAIL}Error inserting documentation: ${error.message}${Colors.ENDC}`);
      return false;
    }
  }

  /**
   * Process file and add documentation
   */
  processFile(analysis) {
    const results = { processed: 0, failed: 0 };
    
    // Sort by line number descending to avoid line shift issues
    const funcs = [...analysis.undocumentedFunctions].sort((a, b) => b.line - a.line);
    
    for (const func of funcs) {
      const docText = this.generateJSDoc(func);
      
      if (this.dryRun) {
        console.log(`    Would add documentation for ${func.type} ${func.name} at line ${func.line}`);
        results.processed++;
      } else {
        if (this.insertDocumentation(analysis.filepath, func, docText)) {
          results.processed++;
        } else {
          results.failed++;
        }
      }
    }
    
    return results;
  }

  /**
   * Create backup of files
   */
  createBackups(files) {
    const backupDir = '.doc-last-backups';
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir);
    }
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
    
    for (const file of files) {
      const filename = path.basename(file);
      const backupPath = path.join(backupDir, `${filename}.${timestamp}.bak`);
      fs.copyFileSync(file, backupPath);
      
      if (this.verbose) {
        console.log(`  Backed up ${file} to ${backupPath}`);
      }
    }
    
    return backupDir;
  }

  /**
   * Enhance documentation with Claude
   */
  enhanceWithClaude(files) {
    const promptPath = '.claude-doc-enhance-prompt.md';
    
    try {
      // Create prompt file
      const prompt = `# Enhance Documentation

I've added basic JSDoc templates to the following files. Please enhance them with meaningful descriptions based on the actual code logic:

${files.map(f => `## ${f}
- Review the generated documentation
- Replace generic descriptions with specific ones based on the code
- Add @example tags for complex functions  
- Add @throws tags where appropriate
- Add proper TypeScript types instead of {*}
- For React components, describe props and behavior
- Ensure parameter descriptions are meaningful
- Update return descriptions to be specific`).join('\n\n')}

Guidelines:
- Keep descriptions concise but informative
- Use proper grammar and punctuation
- Focus on the 'why' and 'what' rather than the 'how'
- Add proper type information
- Include edge cases where relevant
- For React components, describe the UI and behavior`;

      fs.writeFileSync(promptPath, prompt);
      
      // Build claude command
      const args = ['claude'];
      files.forEach(f => args.push('-f', f));
      args.push('-f', promptPath);
      args.push('Please enhance the documentation in the files listed in the prompt.');
      
      if (this.verbose) {
        console.log(`${Colors.BLUE}Running: ${args.join(' ')}${Colors.ENDC}`);
      }
      
      console.log(`${Colors.CYAN}Calling Claude Code to enhance documentation...${Colors.ENDC}`);
      const result = spawnSync(args[0], args.slice(1), { encoding: 'utf8' });
      
      if (result.status === 0) {
        console.log(`${Colors.GREEN}✓ Claude Code successfully enhanced the documentation${Colors.ENDC}`);
      } else {
        console.log(`${Colors.WARNING}⚠️  Claude Code enhancement failed${Colors.ENDC}`);
        if (result.stderr) {
          console.log(`${Colors.FAIL}Error: ${result.stderr}${Colors.ENDC}`);
        }
        
        // Check if claude exists
        const which = spawnSync('which', ['claude']);
        if (which.status !== 0) {
          console.log(`${Colors.CYAN}Note: 'claude' command not found. Make sure Claude Code CLI is installed.${Colors.ENDC}`);
        }
      }
      
      // Clean up
      if (fs.existsSync(promptPath)) {
        fs.unlinkSync(promptPath);
      }
      
    } catch (error) {
      console.log(`${Colors.WARNING}Could not enhance with Claude Code: ${error.message}${Colors.ENDC}`);
    }
  }

  /**
   * Main run method
   */
  run() {
    console.log(`${Colors.HEADER}${'='.repeat(60)}${Colors.ENDC}`);
    console.log(`${Colors.BOLD}Claude Code Documentation Generator (AST)${Colors.ENDC}`);
    console.log(`${Colors.HEADER}${'='.repeat(60)}${Colors.ENDC}\n`);
    
    // Get files to process
    console.log(`${Colors.CYAN}🔍 Detecting recently modified files...${Colors.ENDC}`);
    const files = this.getFilesToProcess();
    
    if (files.length === 0) {
      console.log(`\n${Colors.WARNING}No files found that need documentation.${Colors.ENDC}`);
      console.log(`${Colors.CYAN}Try modifying some JavaScript/TypeScript files and run this command again.${Colors.ENDC}`);
      return;
    }
    
    // Display files
    console.log(`\n${Colors.GREEN}✓ Found ${files.length} file(s) to process:${Colors.ENDC}`);
    files.forEach(file => {
      const ext = path.extname(file);
      console.log(`  📄 ${file} (${SUPPORTED_EXTENSIONS[ext]})`);
    });
    
    // Analyze files
    console.log(`\n${Colors.CYAN}📊 Analyzing files for documentation needs...${Colors.ENDC}`);
    
    const analyses = [];
    let totalUndocumented = 0;
    
    for (const file of files) {
      if (this.verbose) {
        console.log(`  Analyzing ${file}...`);
      }
      
      const analysis = this.analyzeFile(file);
      analyses.push(analysis);
      totalUndocumented += analysis.undocumented;
    }
    
    // Display analysis results
    console.log(`\n${Colors.BOLD}Documentation Analysis Results:${Colors.ENDC}`);
    console.log(`${Colors.HEADER}${'='.repeat(60)}${Colors.ENDC}`);
    
    for (const analysis of analyses) {
      const { filepath, total, documented, undocumented } = analysis;
      const status = undocumented > 0 ? `${Colors.FAIL}❌` : `${Colors.GREEN}✅`;
      
      console.log(`\n${Colors.BOLD}${filepath}:${Colors.ENDC}`);
      console.log(`  Total functions/classes: ${total}`);
      console.log(`  ${Colors.GREEN}Documented: ${documented}${Colors.ENDC}`);
      console.log(`  ${undocumented > 0 ? Colors.FAIL : Colors.GREEN}Undocumented: ${undocumented} ${status}${Colors.ENDC}`);
      
      if (this.verbose && analysis.undocumentedFunctions.length > 0) {
        console.log(`  ${Colors.WARNING}Missing documentation:${Colors.ENDC}`);
        analysis.undocumentedFunctions.forEach(func => {
          console.log(`    - Line ${func.line}: ${func.type} ${func.name}`);
        });
      }
    }
    
    // Summary
    console.log(`\n${Colors.HEADER}${'='.repeat(60)}${Colors.ENDC}`);
    console.log(`${Colors.BOLD}Summary:${Colors.ENDC}`);
    console.log(`  Total files: ${files.length}`);
    console.log(`  ${totalUndocumented > 0 ? Colors.FAIL : Colors.GREEN}Total undocumented functions: ${totalUndocumented}${Colors.ENDC}`);
    
    if (totalUndocumented === 0) {
      console.log(`\n${Colors.GREEN}✅ All functions are documented! Great job!${Colors.ENDC}`);
      return;
    }
    
    // Dry run
    if (this.dryRun) {
      console.log(`\n${Colors.BLUE}Dry run mode - no files will be modified${Colors.ENDC}`);
      console.log(`${Colors.CYAN}Would generate documentation for ${totalUndocumented} functions:${Colors.ENDC}\n`);
      
      for (const analysis of analyses) {
        if (analysis.undocumented > 0) {
          console.log(`${Colors.BOLD}${analysis.filepath}:${Colors.ENDC}`);
          this.processFile(analysis);
        }
      }
      return;
    }
    
    // Process files
    console.log(`\n${Colors.CYAN}📝 Generating documentation...${Colors.ENDC}`);
    
    // Create backups
    console.log(`${Colors.BLUE}Creating backups...${Colors.ENDC}`);
    const filesToBackup = analyses
      .filter(a => a.undocumented > 0)
      .map(a => a.filepath);
    const backupDir = this.createBackups(filesToBackup);
    
    // Process each file
    let totalProcessed = 0;
    let totalFailed = 0;
    
    for (const analysis of analyses) {
      if (analysis.undocumented > 0) {
        console.log(`\n${Colors.BOLD}Processing ${analysis.filepath}...${Colors.ENDC}`);
        
        const results = this.processFile(analysis);
        totalProcessed += results.processed;
        totalFailed += results.failed;
        
        if (results.processed > 0) {
          console.log(`  ${Colors.GREEN}✓ Added documentation for ${results.processed} functions${Colors.ENDC}`);
        }
        if (results.failed > 0) {
          console.log(`  ${Colors.FAIL}✗ Failed to document ${results.failed} functions${Colors.ENDC}`);
        }
      }
    }
    
    // Final report
    console.log(`\n${Colors.HEADER}${'='.repeat(60)}${Colors.ENDC}`);
    console.log(`${Colors.BOLD}Documentation Generation Complete!${Colors.ENDC}`);
    console.log(`${Colors.HEADER}${'='.repeat(60)}${Colors.ENDC}\n`);
    
    console.log(`${Colors.GREEN}✅ Successfully documented ${totalProcessed} functions${Colors.ENDC}`);
    if (totalFailed > 0) {
      console.log(`${Colors.FAIL}❌ Failed to document ${totalFailed} functions${Colors.ENDC}`);
    }
    
    console.log(`\n${Colors.CYAN}Backups saved in: ${backupDir}${Colors.ENDC}`);
    
    // Generate report
    const reportPath = 'documentation-report.md';
    const report = `# Documentation Report

**Generated:** ${new Date().toISOString()}
**Parser:** Babel AST

## Summary

- Total files processed: ${filesToBackup.length}
- Functions documented: ${totalProcessed}
- Functions failed: ${totalFailed}

## Files Processed

${analyses
  .filter(a => a.undocumented > 0)
  .map(a => `### ${a.filepath}\n- Functions documented: ${a.undocumented}\n`)
  .join('\n')}`;
    
    fs.writeFileSync(reportPath, report);
    console.log(`${Colors.CYAN}Report saved to: ${reportPath}${Colors.ENDC}`);
    
    // Enhance with Claude
    if (totalProcessed > 0 && !this.noEnhance) {
      console.log(`\n${Colors.CYAN}🤖 Using Claude Code to enhance documentation...${Colors.ENDC}`);
      this.enhanceWithClaude(filesToBackup);
    } else if (this.noEnhance) {
      console.log(`\n${Colors.BLUE}Skipping Claude Code enhancement (--no-enhance flag)${Colors.ENDC}`);
    }
  }
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  
  const options = {
    verbose: args.includes('-v') || args.includes('--verbose'),
    dryRun: args.includes('-n') || args.includes('--dry-run'),
    noEnhance: args.includes('--no-enhance'),
    help: args.includes('-h') || args.includes('--help')
  };
  
  if (options.help) {
    console.log(`
Claude Code Documentation Generator

Usage: node doc-generator.js [options]

Options:
  -h, --help       Show this help message
  -v, --verbose    Show detailed output
  -n, --dry-run    Show what would be done without making changes
  --no-enhance     Skip Claude Code enhancement step

Examples:
  node doc-generator.js              # Document files from last commit
  node doc-generator.js --dry-run    # Preview changes
  node doc-generator.js --verbose    # Show detailed progress
`);
    process.exit(0);
  }
  
  // Check dependencies
  try {
    require('@babel/parser');
    require('@babel/traverse');
    require('@babel/types');
  } catch (error) {
    console.error(`${Colors.FAIL}Missing required dependencies!${Colors.ENDC}`);
    console.error('Please install: npm install @babel/parser @babel/traverse @babel/types');
    process.exit(1);
  }
  
  const generator = new DocumentationGenerator(options);
  generator.run();
}

module.exports = DocumentationGenerator;