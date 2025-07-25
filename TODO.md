# Claude Code Documentation Extension - TODO List

## Overview
Simple TODO list for the `/doc-last` command extension that generates documentation for recently modified files.

**Priority:** 🔴 High | 🟡 Medium | 🟢 Low  
**Effort:** S (1-2h) | M (2-4h) | L (4-8h)

---

## Phase 1: Core Command Setup
- [ ] 🔴 **Create command file structure** (S)
  - Create `.claude/commands/doc-last` executable
  - Add basic command template with help text
  - Test command registration in Claude Code

- [ ] 🔴 **Setup Python/Shell script base** (S)
  - Choose implementation language (Python recommended)
  - Add shebang and basic imports
  - Create main function structure

## Phase 2: File Detection
- [ ] 🔴 **Implement git-based file detection** (M)
  - Get files from last commit: `git diff --name-only HEAD~1`
  - Fallback to unstaged: `git diff --name-only`
  - Filter by supported extensions (.js, .ts, .py)

- [ ] 🟡 **Add time-based detection fallback** (S)
  - Find files modified in last 5 minutes
  - Use when not in git repo or no recent changes

## Phase 3: Documentation Analysis
- [ ] 🔴 **Create simple function detector** (M)
  - Regex-based function/class detection
  - Check for existing JSDoc/docstrings
  - Count undocumented functions

- [ ] 🟡 **Generate documentation report** (S)
  - List files needing documentation
  - Show count of undocumented functions
  - Format as readable output

## Phase 4: Documentation Generation
- [ ] 🔴 **Implement JSDoc generator** (L)
  - Template for function documentation
  - Parse function signatures
  - Output formatted JSDoc comments

- [ ] 🔴 **Implement Python docstring generator** (L)
  - Template for Python docstrings
  - Support Google-style format
  - Handle class and function docs

- [ ] 🟡 **Add file update logic** (M)
  - Insert documentation at correct positions
  - Preserve existing code formatting
  - Create backup before modifying

## Phase 5: User Experience
- [ ] 🔴 **Create progress output** (S)
  - Show files being processed
  - Display success/error messages
  - Add color coding for clarity

- [ ] 🟡 **Generate final report** (S)
  - Summary of changes made
  - Checklist of remaining tasks
  - Save report to `documentation-report.md`

- [ ] 🟢 **Add configuration options** (M)
  - Support custom documentation styles
  - Allow file pattern exclusions
  - Configure output verbosity

## Phase 6: Testing & Polish
- [ ] 🔴 **Test with sample projects** (M)
  - JavaScript/TypeScript project
  - Python project
  - Mixed language project

- [ ] 🟡 **Handle edge cases** (M)
  - Empty files
  - Files with existing docs
  - Non-standard code patterns

- [ ] 🟡 **Write usage documentation** (S)
  - Installation instructions
  - Usage examples
  - Troubleshooting tips

## Phase 7: Future Enhancements
- [ ] 🟢 **Add more language support** (L)
  - Java with Javadoc
  - Go with godoc
  - Rust with rustdoc

- [ ] 🟢 **Create VS Code integration** (L)
  - Command palette integration
  - Status bar indicator
  - Quick fix suggestions

- [ ] 🟢 **Add hook system** (M)
  - Auto-detect when docs needed
  - Suggest running command
  - Post-commit integration

---

## Quick Start Tasks (Do First!)
1. Create `.claude/commands/doc-last` file
2. Make it executable: `chmod +x .claude/commands/doc-last`
3. Add basic Python script structure
4. Implement git file detection
5. Create simple JSDoc generator
6. Test with a real project

## Total: ~20 tasks | Estimated effort: ~40-50 hours