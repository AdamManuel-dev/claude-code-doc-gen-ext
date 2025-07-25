# Bug Report

## Bug #1: Python Docstrings Placement Issue
**Date:** 2025-07-25
**Severity:** Medium
**Status:** Open

### Description
Python docstrings are being placed above the function definition instead of inside the function body after the def line. This violates PEP 257 conventions.

### Current Behavior
```python
"""
Calculate average.
"""
def calculate_average(numbers):
    # function body
```

### Expected Behavior
```python
def calculate_average(numbers):
    """
    Calculate average.
    """
    # function body
```

### Affected Files
- `.claude/commands/doc-last` - `insert_documentation()` function
- `.claude/commands/doc-last` - `detect_python_functions()` function

### Root Cause
The insertion logic treats Python docstrings the same as JSDoc comments, placing them before the function declaration. Python docstrings should be inserted as the first statement inside the function body.

### Fix Required
1. Modify `insert_documentation()` to handle Python files differently
2. For Python files, insert the docstring after the function/class declaration line
3. Ensure proper indentation is maintained

### Test Case
Test with `test-samples/test-python.py` to verify fix.