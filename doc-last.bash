#!/bin/bash
# Claude Code Slash Command: /doc-last
# Location: .claude/commands/doc-last
# Make executable: chmod +x .claude/commands/doc-last

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
EXTENSIONS="js|jsx|ts|tsx|mjs|cjs|py|java|go|rs"
DOC_DIR="docs"
REPORT_FILE="documentation-report.md"

# Function to print colored output
print_color() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Function to get recently modified files
get_modified_files() {
    local files=()
    
    # Try different methods to find modified files
    # Method 1: Files changed in last commit
    if git rev-parse HEAD~ &>/dev/null; then
        mapfile -t files < <(git diff --name-only HEAD~ HEAD | grep -E "\.($EXTENSIONS)$" || true)
    fi
    
    # Method 2: Unstaged changes
    if [ ${#files[@]} -eq 0 ]; then
        mapfile -t files < <(git status --porcelain | awk '{print $2}' | grep -E "\.($EXTENSIONS)$" || true)
    fi
    
    # Method 3: Recently modified files (last 5 minutes)
    if [ ${#files[@]} -eq 0 ]; then
        mapfile -t files < <(find . -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \
            -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.rs" \
            -type f -mmin -5 2>/dev/null | grep -v node_modules | grep -v ".git" || true)
    fi
    
    # Filter out non-existent files and remove duplicates
    local valid_files=()
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            valid_files+=("$file")
        fi
    done
    
    # Remove duplicates
    printf '%s\n' "${valid_files[@]}" | sort -u
}

# Function to analyze a file for documentation needs
analyze_file() {
    local file=$1
    local needs_doc=false
    local details=""
    
    if [[ $file =~ \.(js|jsx|ts|tsx)$ ]]; then
        # Check for JavaScript/TypeScript documentation
        if ! grep -q "^\s*/\*\*" "$file"; then
            needs_doc=true
            details="Missing JSDoc comments"
        fi
        
        # Count undocumented functions
        local func_count=$(grep -E "(function\s+\w+|const\s+\w+\s*=\s*\(|=\s*async\s*\()" "$file" | wc -l)
        local jsdoc_count=$(grep -c "^\s*/\*\*" "$file" || true)
        
        if [ $func_count -gt $jsdoc_count ]; then
            needs_doc=true
            details="$((func_count - jsdoc_count)) undocumented functions"
        fi
        
    elif [[ $file =~ \.py$ ]]; then
        # Check for Python docstrings
        if ! grep -q '"""' "$file" && ! grep -q "'''" "$file"; then
            needs_doc=true
            details="Missing docstrings"
        fi
    fi
    
    echo "$needs_doc|$details"
}

# Function to generate documentation prompt
generate_prompt() {
    local files=("$@")
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local prompt_file=".claude/prompts/doc-generation-${timestamp}.md"
    
    mkdir -p "$(dirname "$prompt_file")"
    
    cat > "$prompt_file" << 'EOF'
# Documentation Generation Request

Please generate comprehensive documentation for the files modified by the last command.

## Context
These files were recently modified and need proper documentation to maintain code quality and help future developers understand the changes.

## Files to Document
EOF
    
    # Add file list with analysis
    for file in "${files[@]}"; do
        local analysis=$(analyze_file "$file")
        local needs_doc=$(echo "$analysis" | cut -d'|' -f1)
        local details=$(echo "$analysis" | cut -d'|' -f2)
        
        if [ "$needs_doc" = "true" ]; then
            echo "- **$file** - $details" >> "$prompt_file"
        else
            echo "- $file" >> "$prompt_file"
        fi
    done
    
    cat >> "$prompt_file" << 'EOF'

## Documentation Requirements

### 1. Source Code Documentation
For each file, add appropriate inline documentation:

#### JavaScript/TypeScript Files
```javascript
/**
 * Brief description of what the function does.
 * More detailed explanation if needed.
 * 
 * @param {Type} paramName - Description of parameter
 * @returns {Type} Description of return value
 * @throws {ErrorType} When this error occurs
 * @example
 * // Example usage
 * const result = functionName(params);
 */
```

#### Python Files
```python
def function_name(param: Type) -> ReturnType:
    """
    Brief description of what the function does.
    
    More detailed explanation if needed.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ErrorType: When this error occurs
        
    Example:
        >>> result = function_name(param)
    """
```

### 2. Module Documentation
For each module affected, create or update `docs/modules/[module-name].md`:

```markdown
# Module Name

## Overview
Brief description of the module's purpose.

## API Reference

### functionName(params)
Description of the function.

**Parameters:**
- `param` (Type): Description

**Returns:** Type - Description

**Example:**
```javascript
// Example code
```

## Usage Patterns
Common usage patterns and best practices.

## Error Handling
How errors are handled in this module.
```

### 3. Project Documentation Updates

#### README.md
- Add new features to feature list
- Update usage examples
- Add new dependencies

#### API.md
- Document new endpoints
- Update request/response formats
- Add authentication requirements

#### CHANGELOG.md
- Add entry for changes made
- Follow existing format

### 4. Architecture Documentation
If structural changes were made:
- Update ARCHITECTURE.md
- Add/update diagrams
- Document new patterns

### 5. Testing Documentation
- Document test cases for new functionality
- Update testing guide if needed

## Quality Checklist
- [ ] All public functions have documentation
- [ ] Examples are runnable and correct
- [ ] Documentation matches implementation
- [ ] Cross-references are updated
- [ ] No broken links
- [ ] Consistent formatting

## Special Instructions
- Follow existing documentation patterns in the project
- Keep descriptions clear and concise
- Include both simple and advanced examples
- Document error cases and edge conditions
- Add links to related documentation

Please analyze each file and generate appropriate documentation following these guidelines.
EOF
    
    echo "$prompt_file"
}

# Function to create documentation report
create_report() {
    local files=("$@")
    
    cat > "$REPORT_FILE" << EOF
# Documentation Generation Report
Generated: $(date '+%Y-%m-%d %H:%M:%S')
Command: /doc-last

## Summary
- Files to document: ${#files[@]}
- Documentation scope: Source code + Project docs

## Files Analyzed
EOF
    
    for file in "${files[@]}"; do
        local analysis=$(analyze_file "$file")
        local needs_doc=$(echo "$analysis" | cut -d'|' -f1)
        local details=$(echo "$analysis" | cut -d'|' -f2)
        
        if [ "$needs_doc" = "true" ]; then
            echo "- [ ] **$file** - $details" >> "$REPORT_FILE"
        else
            echo "- [ ] $file - May already be documented" >> "$REPORT_FILE"
        fi
    done
    
    cat >> "$REPORT_FILE" << EOF

## Documentation Tasks
- [ ] Add JSDoc/docstring comments
- [ ] Update/create module documentation
- [ ] Update README.md if needed
- [ ] Update API.md if needed
- [ ] Add CHANGELOG.md entry
- [ ] Verify all examples work
- [ ] Check cross-references

## Next Steps
1. Review generated documentation for accuracy
2. Fill in any TODO placeholders
3. Run tests to ensure examples work
4. Commit documentation changes

## Notes
- Prioritize public APIs and complex functions
- Ensure consistency with project standards
- Consider adding diagrams for complex flows
EOF
}

# Main execution
main() {
    print_color "$BLUE" "🔍 Claude Code Documentation Generator"
    print_color "$BLUE" "====================================="
    
    # Get modified files
    mapfile -t modified_files < <(get_modified_files)
    
    if [ ${#modified_files[@]} -eq 0 ]; then
        print_color "$RED" "❌ No code files were modified recently."
        print_color "$YELLOW" "💡 Tip: This command works best right after making code changes."
        echo ""
        print_color "$YELLOW" "Alternative usage:"
        print_color "$YELLOW" "  /doc-last <file1> <file2> ... - Document specific files"
        print_color "$YELLOW" "  /doc-last src/              - Document all files in a directory"
        exit 1
    fi
    
    print_color "$GREEN" "📝 Found ${#modified_files[@]} file(s) to document:"
    for file in "${modified_files[@]}"; do
        local analysis=$(analyze_file "$file")
        local needs_doc=$(echo "$analysis" | cut -d'|' -f1)
        local details=$(echo "$analysis" | cut -d'|' -f2)
        
        if [ "$needs_doc" = "true" ]; then
            print_color "$YELLOW" "   - $file ($details)"
        else
            echo "   - $file"
        fi
    done
    
    echo ""
    
    # Generate documentation prompt
    prompt_file=$(generate_prompt "${modified_files[@]}")
    print_color "$GREEN" "✅ Documentation prompt created: $prompt_file"
    
    # Create tracking report
    create_report "${modified_files[@]}"
    print_color "$GREEN" "📊 Tracking report created: $REPORT_FILE"
    
    echo ""
    print_color "$BLUE" "🚀 Ready for Documentation Generation!"
    print_color "$BLUE" "===================================="
    
    # Instructions for Claude Code
    echo ""
    echo "Claude Code will now:"
    echo "1. Analyze each modified file"
    echo "2. Add comprehensive inline documentation"
    echo "3. Create/update project documentation"
    echo "4. Ensure all changes are properly documented"
    
    echo ""
    print_color "$YELLOW" "📋 After generation, check:"
    echo "   - $REPORT_FILE for progress tracking"
    echo "   - Source files for new documentation"
    echo "   - $DOC_DIR/ for updated project docs"
    
    # Output the prompt content for Claude Code
    echo ""
    print_color "$BLUE" "Processing documentation request..."
    cat "$prompt_file"
}

# Check if specific files were provided as arguments
if [ $# -gt 0 ]; then
    # Use provided files instead of auto-detection
    modified_files=("$@")
    print_color "$BLUE" "📝 Documenting specified files..."
else
    # Run main auto-detection
    main
fi