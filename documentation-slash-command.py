#!/usr/bin/env python3
"""
Claude Code Slash Command: /doc-last
Generates documentation for files modified by the last command

Place this file in your project as: .claude/commands/doc-last.py
Make it executable: chmod +x .claude/commands/doc-last.py
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

def get_last_modified_files():
    """Get files modified in the last git operation or unstaged changes"""
    try:
        # Try to get files from last commit
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~', 'HEAD'],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip():
            files = result.stdout.strip().split('\n')
        else:
            # Fall back to unstaged changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                check=True
            )
            files = [
                line[3:] for line in result.stdout.strip().split('\n')
                if line and line[0] in 'MA'
            ]
        
        # Filter for code files
        extensions = {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.py', '.java', '.go', '.rs'}
        return [f for f in files if Path(f).suffix in extensions and os.path.exists(f)]
        
    except subprocess.CalledProcessError:
        return []

def create_documentation_prompt(files):
    """Create the documentation generation prompt"""
    
    prompt = f"""# Generate Documentation for Modified Files

The following files were modified by the last command and need documentation:

## Files to Document:
{chr(10).join(f'- {f}' for f in files)}

## Documentation Tasks:

### 1. JSDoc/Docstring Generation
For each file, add comprehensive documentation:
- All functions, classes, and methods need documentation
- Include parameter types, descriptions, and return values
- Add usage examples for complex functions
- Document error cases and exceptions
- Follow the project's existing documentation style

### 2. File-Level Documentation
For complex files, add a file header comment explaining:
- Purpose and responsibilities of the file
- Main exports and their uses
- Dependencies and relationships
- Any important implementation notes

### 3. Update Project Documentation

#### Create/Update Module Documentation
For each module affected, update `docs/modules/[module-name].md`:
- Add new functions to the API reference
- Update usage examples
- Document any breaking changes

#### Update Main Documentation
- If new features: Update README.md
- If API changes: Update docs/API.md
- If architecture changes: Update docs/ARCHITECTURE.md

### 4. Generate Implementation Examples
- Add code examples showing typical usage
- Include edge cases and error handling
- Show integration with other components

### 5. Cross-Reference Documentation
- Link between related docs
- Update table of contents
- Ensure all new functionality is discoverable

## Quality Requirements:
- All examples must be runnable
- Documentation must be consistent with code
- Follow existing project conventions
- Include both basic and advanced usage

## Special Handling by File Type:
"""

    # Add file-specific instructions
    for file in files:
        ext = Path(file).suffix
        if ext in ['.jsx', '.tsx']:
            prompt += f"""
### React Component: {file}
- Document all props with types and defaults
- Add usage examples with different prop combinations
- Document any context or state management
- Consider creating Storybook stories
"""
        elif ext in ['.js', '.ts'] and 'api' in file.lower():
            prompt += f"""
### API Endpoint: {file}
- Document request/response formats
- Add curl examples
- Document authentication requirements
- Include error response examples
"""
        elif ext in ['.js', '.ts'] and 'test' in file.lower():
            prompt += f"""
### Test File: {file}
- Document what is being tested
- Explain any complex test setups
- Document mock data structures
"""

    prompt += """
## Output Requirements:
1. First, update the source files with inline documentation
2. Then create/update markdown documentation files
3. Finally, provide a summary of all documentation added

Please analyze each file carefully and generate comprehensive documentation that will help future developers understand and use this code effectively.
"""

    return prompt

def main():
    """Main execution function"""
    print("🔍 Claude Code Documentation Generator")
    print("=" * 50)
    
    # Get modified files
    files = get_last_modified_files()
    
    if not files:
        print("❌ No code files were modified by the last command.")
        print("💡 Tip: This command works best immediately after code changes.")
        sys.exit(1)
    
    print(f"📝 Found {len(files)} modified file(s):")
    for f in files:
        print(f"   - {f}")
    
    # Create documentation prompt
    prompt = create_documentation_prompt(files)
    
    # Save prompt for Claude Code to process
    prompt_file = f".claude/prompts/doc-generation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
    
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    
    print(f"\n✅ Documentation prompt created: {prompt_file}")
    
    # Create tracking file
    tracking_file = "documentation-report.md"
    with open(tracking_file, 'w') as f:
        f.write(f"""# Documentation Generation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Files to Document:
{chr(10).join(f'- [ ] {f}' for f in files)}

## Documentation Tasks:
- [ ] Add JSDoc/docstring comments
- [ ] Update module documentation
- [ ] Update API documentation
- [ ] Add usage examples
- [ ] Cross-reference documentation
- [ ] Verify all examples work

## Notes:
- Review generated documentation for accuracy
- Ensure consistency with project standards
- Run tests to verify examples
""")
    
    print(f"📊 Tracking file created: {tracking_file}")
    
    # Output for Claude Code to process
    print("\n🚀 Ready for documentation generation!")
    print("Claude Code will now analyze the files and generate comprehensive documentation.")
    
    # Return the prompt for Claude Code to process
    return prompt

if __name__ == "__main__":
    # When run as a slash command, output the prompt
    prompt = main()
    print("\n" + "=" * 50)
    print("PROMPT FOR CLAUDE CODE:")
    print("=" * 50)
    print(prompt)