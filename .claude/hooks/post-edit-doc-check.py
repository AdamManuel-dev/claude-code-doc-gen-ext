#!/usr/bin/env python3
"""
Post-edit hook to check if edited files need documentation.
Receives tool usage data via stdin and can suggest documentation generation.
"""

import sys
import json
import os
from pathlib import Path

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract tool info
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Track which files were edited
        edited_files = []
        
        if tool_name in ['Edit', 'MultiEdit']:
            file_path = tool_input.get('file_path')
            if file_path:
                edited_files.append(file_path)
        elif tool_name == 'Write':
            file_path = tool_input.get('file_path')
            if file_path:
                edited_files.append(file_path)
        
        # Filter for code files that might need documentation
        code_extensions = {'.js', '.jsx', '.ts', '.tsx', '.py', '.mjs', '.cjs'}
        code_files = [f for f in edited_files if Path(f).suffix in code_extensions]
        
        if code_files:
            # Create a state file to track files that may need documentation
            state_dir = Path('.claude/state')
            state_dir.mkdir(parents=True, exist_ok=True)
            
            state_file = state_dir / 'pending-documentation.json'
            
            # Load existing pending files
            pending_files = []
            if state_file.exists():
                with open(state_file, 'r') as f:
                    pending_files = json.load(f)
            
            # Add new files
            pending_files.extend(code_files)
            pending_files = list(set(pending_files))  # Remove duplicates
            
            # Save updated list
            with open(state_file, 'w') as f:
                json.dump(pending_files, f, indent=2)
            
            # Optionally output a suggestion (this will be visible in verbose mode)
            print(f"Files edited that may need documentation: {', '.join(code_files)}", file=sys.stderr)
        
        # Exit successfully (0 = continue with tool execution)
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't block tool execution
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()