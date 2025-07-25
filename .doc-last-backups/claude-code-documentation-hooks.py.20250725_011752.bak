#!/usr/bin/env python3
"""
Claude Code Hooks for Automatic Documentation
Place in: .claude/hooks/post-command.py

This hook automatically tracks file changes and offers to generate documentation
after each command execution.
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class DocumentationHook:
    def __init__(self):
        self.state_file = ".claude/state/last-modified-files.json"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        os.makedirs(".claude/prompts", exist_ok=True)
    
    def get_modified_files(self):
        """Track files modified since last check"""
        try:
            # Get current git status
            result = subprocess.run(
                ['git', 'ls-files', '-m', '-o', '--exclude-standard'],
                capture_output=True,
                text=True,
                check=True
            )
            
            current_files = set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
            
            # Load previous state
            previous_files = set()
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    previous_files = set(json.load(f))
            
            # Find newly modified files
            modified = current_files - previous_files
            
            # Filter for code files
            extensions = {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.py', '.java', '.go', '.rs'}
            code_files = [f for f in modified if Path(f).suffix in extensions and os.path.exists(f)]
            
            # Save current state
            with open(self.state_file, 'w') as f:
                json.dump(list(current_files), f)
            
            return code_files
            
        except subprocess.CalledProcessError:
            return []
    
    def should_generate_docs(self, files):
        """Determine if documentation should be generated"""
        if not files:
            return False
        
        # Check if any files lack documentation
        for file in files:
            if self.needs_documentation(file):
                return True
        
        return False
    
    def needs_documentation(self, filepath):
        """Check if a file needs documentation"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Simple heuristics - can be made more sophisticated
            if filepath.endswith(('.js', '.jsx', '.ts', '.tsx')):
                # Check for JSDoc
                has_jsdoc = '/**' in content and '*/' in content
                # Check for functions without docs
                has_undocumented_functions = (
                    'function ' in content or 
                    'const ' in content and '= (' in content
                ) and not has_jsdoc
                return has_undocumented_functions
            
            elif filepath.endswith('.py'):
                # Check for docstrings
                has_docstring = '"""' in content or "'''" in content
                has_functions = 'def ' in content
                return has_functions and not has_docstring
                
        except Exception:
            return False
        
        return False
    
    def generate_documentation_prompt(self, files):
        """Generate the documentation prompt"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        prompt_file = f".claude/prompts/auto-doc-{timestamp}.md"
        
        prompt = f"""# Automatic Documentation Generation

The following files were modified and need documentation:

## Modified Files:
{chr(10).join(f'- {f}' for f in files)}

## Quick Documentation Tasks:

1. **Add Missing Documentation**:
   - Add JSDoc/docstrings to undocumented functions
   - Document complex logic with inline comments
   - Add file headers for complex modules

2. **Update Existing Docs**:
   - Update README.md if new features added
   - Update API.md if endpoints changed
   - Add entries to CHANGELOG.md

3. **Examples**:
   - Add usage examples for new functions
   - Update existing examples if APIs changed

Please analyze and add appropriate documentation.
"""
        
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        return prompt_file
    
    def run(self, command_context=None):
        """Main hook execution"""
        modified_files = self.get_modified_files()
        
        if self.should_generate_docs(modified_files):
            print("\n📝 Documentation Suggestion")
            print("=" * 40)
            print(f"Found {len(modified_files)} file(s) that may need documentation:")
            for f in modified_files[:5]:  # Show first 5
                print(f"  - {f}")
            if len(modified_files) > 5:
                print(f"  ... and {len(modified_files) - 5} more")
            
            prompt_file = self.generate_documentation_prompt(modified_files)
            print(f"\n💡 Run '/doc-last' to generate documentation")
            print(f"   or view prompt: {prompt_file}")

# Hook entry point
def post_command_hook(context):
    """Called after each Claude Code command"""
    hook = DocumentationHook()
    hook.run(context)

if __name__ == "__main__":
    # Test the hook
    hook = DocumentationHook()
    hook.run()