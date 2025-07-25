#!/usr/bin/env python3
"""
Hook that runs at the end of a Claude session to remind about documentation.
Checks if any files were edited that might need documentation.
"""

import sys
import json
import os
from pathlib import Path

def main():
    try:
        # Check if there are pending files that need documentation
        state_file = Path('.claude/state/pending-documentation.json')
        
        if state_file.exists():
            with open(state_file, 'r') as f:
                pending_files = json.load(f)
            
            # Filter files that still exist
            existing_files = [f for f in pending_files if os.path.exists(f)]
            
            if existing_files:
                print("\n📝 Documentation Reminder", file=sys.stderr)
                print("=" * 40, file=sys.stderr)
                print(f"The following files were edited and may need documentation:", file=sys.stderr)
                for file in existing_files[:5]:  # Show max 5 files
                    print(f"  - {file}", file=sys.stderr)
                if len(existing_files) > 5:
                    print(f"  ... and {len(existing_files) - 5} more files", file=sys.stderr)
                print("\nRun `/doc-last` to generate documentation for recent changes.", file=sys.stderr)
                print("=" * 40, file=sys.stderr)
                
                # Clear the pending files after reminder
                with open(state_file, 'w') as f:
                    json.dump([], f)
        
        # Always exit successfully
        sys.exit(0)
        
    except Exception as e:
        # Don't block on errors
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()