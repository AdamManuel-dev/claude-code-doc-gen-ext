# Advanced Usage Tutorial

This tutorial covers advanced features and use cases for the Claude Code Documentation Generator. You'll learn how to handle complex scenarios, customize documentation, and integrate the tool into your development pipeline.

## Table of Contents

- [Working with Complex Code Structures](#working-with-complex-code-structures)
- [Customizing Documentation Output](#customizing-documentation-output)
- [Git Hooks Integration](#git-hooks-integration)
- [CI/CD Integration](#cicd-integration)
- [Handling Large Codebases](#handling-large-codebases)
- [Multi-Language Projects](#multi-language-projects)
- [Team Workflows](#team-workflows)
- [Performance Optimization](#performance-optimization)

## Working with Complex Code Structures

### React Components

The generator handles React components intelligently:

```javascript
// Before documentation
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const UserProfile = ({ userId, onUpdate }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(data => {
      setUser(data);
      setLoading(false);
    });
  }, [userId]);

  const handleEdit = () => {
    // Edit logic
  };

  return (
    <div>
      {loading ? <Spinner /> : <Profile user={user} onEdit={handleEdit} />}
    </div>
  );
};

UserProfile.propTypes = {
  userId: PropTypes.string.isRequired,
  onUpdate: PropTypes.func
};
```

After running the generator:

```javascript
/**
 * User profile.
 * @param {Object} props - The component props.
 * @param {string} props.userId - The user id.
 * @param {Function} props.onUpdate - The on update.
 * @returns {JSX.Element} The component.
 */
const UserProfile = ({ userId, onUpdate }) => {
  // ... rest of component
};
```

### TypeScript Interfaces and Types

For TypeScript files with complex types:

```typescript
// Before
interface UserData {
  id: string;
  name: string;
  email: string;
  roles: Role[];
}

type Role = 'admin' | 'user' | 'guest';

class UserService {
  async getUser(id: string): Promise<UserData> {
    // Implementation
  }
  
  updateUserRoles(userId: string, roles: Role[]): Promise<void> {
    // Implementation
  }
}
```

The generator creates appropriate JSDoc with type information preserved.

### Async/Generator Functions

The tool recognizes special function types:

```javascript
// Async function
async function fetchDataWithRetry(url, maxRetries = 3) {
  // Implementation
}

// Generator function  
function* fibonacci(n) {
  let a = 0, b = 1;
  for (let i = 0; i < n; i++) {
    yield a;
    [a, b] = [b, a + b];
  }
}

// Async generator
async function* asyncDataStream(source) {
  for await (const chunk of source) {
    yield processChunk(chunk);
  }
}
```

## Customizing Documentation Output

### Using Templates (Future Feature)

While not yet implemented, you can prepare for template support:

```javascript
// .doc-templates/function.jsdoc
/**
 * ${description}
 * @since ${version}
 * @param {${paramType}} ${paramName} - ${paramDescription}
 * @returns {${returnType}} ${returnDescription}
 * @example
 * ${example}
 */
```

### Manual Enhancement Workflow

For now, use this workflow for custom documentation:

```bash
# 1. Generate basic documentation
/doc-last --no-enhance

# 2. Review and enhance manually
vim src/complex-module.js

# 3. Use Claude to enhance specific files
claude "Enhance the JSDoc comments in this file with detailed descriptions" < src/complex-module.js
```

### Documentation Styles

Adapt the output to your project's style:

```javascript
// Detailed style (manually enhance after generation)
/**
 * Calculates the compound interest on an investment.
 * 
 * This function uses the compound interest formula: A = P(1 + r/n)^(nt)
 * where:
 * - A is the final amount
 * - P is the principal amount
 * - r is the annual interest rate (as a decimal)
 * - n is the number of times interest is compounded per year
 * - t is the time in years
 * 
 * @param {number} principal - The initial investment amount in dollars
 * @param {number} rate - The annual interest rate as a decimal (e.g., 0.05 for 5%)
 * @param {number} time - The investment period in years
 * @param {number} [compound=12] - How often interest is compounded per year (default: monthly)
 * @returns {number} The final amount after interest
 * @throws {Error} If any parameter is negative
 * @example
 * // Calculate interest on $1000 at 5% for 10 years, compounded monthly
 * const finalAmount = calculateCompoundInterest(1000, 0.05, 10);
 * console.log(finalAmount); // 1647.01
 */
function calculateCompoundInterest(principal, rate, time, compound = 12) {
  if (principal < 0 || rate < 0 || time < 0) {
    throw new Error('Parameters cannot be negative');
  }
  return principal * Math.pow(1 + rate / compound, compound * time);
}
```

## Git Hooks Integration

### Pre-commit Hook

Set up automatic documentation on commit:

```bash
# Create .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Auto-document staged files before commit

# Get staged JS/TS/Python files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|jsx|ts|tsx|py)$')

if [ -n "$STAGED_FILES" ]; then
  echo "Generating documentation for staged files..."
  
  # Run documentation generator
  python3 .claude/commands/doc-staged --no-enhance
  
  # Re-stage the documented files
  for file in $STAGED_FILES; do
    git add "$file"
  done
  
  echo "Documentation generated and staged."
fi
EOF

chmod +x .git/hooks/pre-commit
```

### Post-merge Hook

Update documentation after merging:

```bash
# Create .git/hooks/post-merge
cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash
# Check for undocumented functions after merge

echo "Checking documentation coverage..."
./doc-generator.js --dry-run > .doc-coverage-report.txt

if grep -q "undocumented" .doc-coverage-report.txt; then
  echo "Warning: Undocumented functions found after merge."
  echo "Run '/doc-all' to generate missing documentation."
  cat .doc-coverage-report.txt
fi
EOF

chmod +x .git/hooks/post-merge
```

## CI/CD Integration

### GitHub Actions

Add documentation checks to your workflow:

```yaml
# .github/workflows/documentation.yml
name: Documentation Check

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Check documentation coverage
        run: |
          ./doc-generator.js --dry-run > doc-report.txt
          if grep -q "undocumented" doc-report.txt; then
            echo "::warning::Undocumented functions found"
            cat doc-report.txt
            exit 1
          fi
      
      - name: Upload documentation report
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: documentation-report
          path: doc-report.txt
```

### GitLab CI

```yaml
# .gitlab-ci.yml
documentation:
  stage: test
  script:
    - npm install
    - ./doc-generator.js --dry-run > doc-coverage.txt
    - |
      if grep -q "undocumented" doc-coverage.txt; then
        echo "Documentation missing for some functions"
        cat doc-coverage.txt
        exit 1
      fi
  artifacts:
    when: on_failure
    paths:
      - doc-coverage.txt
```

## Handling Large Codebases

### Incremental Documentation

For large projects, document incrementally:

```bash
# Document by directory
find src -type d -maxdepth 1 | while read dir; do
  echo "Documenting $dir..."
  cd "$dir"
  /doc-all --no-enhance
  cd ..
done

# Document by feature
git log --oneline --grep="feat:" | head -20 | while read commit; do
  git checkout $commit
  /doc-last
done
git checkout main
```

### Parallel Processing

Use GNU Parallel for faster processing:

```bash
# Install GNU Parallel
brew install parallel  # macOS
sudo apt-get install parallel  # Ubuntu

# Process files in parallel
find . -name "*.js" -type f | parallel -j 4 './doc-generator.js {}'
```

### Filtering Strategies

Document only critical files:

```bash
# Create a priority list
cat > .doc-priority << 'EOF'
src/api/
src/auth/
src/core/
src/utils/
EOF

# Document priority directories
while read dir; do
  find "$dir" -name "*.js" -exec ./doc-generator.js {} \;
done < .doc-priority
```

## Multi-Language Projects

### Language-Specific Workflows

Handle different languages appropriately:

```bash
# JavaScript/TypeScript
find . -name "*.js" -o -name "*.ts" | xargs ./doc-generator.js

# Python
find . -name "*.py" | xargs python3 documentation-slash-command.py

# Mixed project script
cat > document-all.sh << 'EOF'
#!/bin/bash
echo "Documenting JavaScript/TypeScript files..."
./doc-generator.js $(find . -name "*.js" -o -name "*.ts")

echo "Documenting Python files..."
python3 documentation-slash-command.py $(find . -name "*.py")

echo "Documentation complete!"
EOF
chmod +x document-all.sh
```

### Cross-Language Documentation Standards

Maintain consistency across languages:

```javascript
// JavaScript: Follow JSDoc conventions
/**
 * Validates user input according to schema.
 * @param {Object} data - The input data to validate
 * @param {Object} schema - The validation schema
 * @returns {ValidationResult} The validation result
 */
```

```python
# Python: Use Google-style docstrings
def validate_input(data: dict, schema: dict) -> ValidationResult:
    """Validates user input according to schema.
    
    Args:
        data: The input data to validate
        schema: The validation schema
        
    Returns:
        The validation result
    """
```

## Team Workflows

### Documentation Standards

Create a team documentation guide:

```markdown
# Documentation Standards

1. All public functions must be documented
2. Use descriptive parameter names
3. Include at least one example for complex functions
4. Document error conditions and exceptions
5. Keep descriptions concise but complete

## Documentation Checklist
- [ ] Function purpose is clear
- [ ] All parameters are documented
- [ ] Return value is described
- [ ] Exceptions are documented
- [ ] Example is provided (if applicable)
```

### Code Review Integration

Add documentation checks to your review process:

```bash
# Pre-review script
cat > check-pr-docs.sh << 'EOF'
#!/bin/bash
# Check documentation for PR files

# Get changed files in PR
CHANGED_FILES=$(git diff origin/main...HEAD --name-only | grep -E '\.(js|ts|py)$')

echo "Checking documentation for PR files..."
for file in $CHANGED_FILES; do
  if [ -f "$file" ]; then
    echo "Checking $file..."
    ./doc-generator.js "$file" --dry-run
  fi
done
EOF
chmod +x check-pr-docs.sh
```

### Documentation Metrics

Track documentation coverage:

```javascript
// doc-metrics.js
const { DocumentationGenerator } = require('./doc-generator');

async function calculateMetrics() {
  const generator = new DocumentationGenerator({ dryRun: true });
  const files = generator.getFilesToProcess();
  
  let totalFunctions = 0;
  let documentedFunctions = 0;
  
  for (const file of files) {
    const result = generator.analyzeFile(file);
    totalFunctions += result.totalItems;
    documentedFunctions += (result.totalItems - result.undocumentedItems.length);
  }
  
  const coverage = (documentedFunctions / totalFunctions * 100).toFixed(2);
  
  console.log(`Documentation Coverage: ${coverage}%`);
  console.log(`Total Functions: ${totalFunctions}`);
  console.log(`Documented: ${documentedFunctions}`);
  console.log(`Missing: ${totalFunctions - documentedFunctions}`);
}

calculateMetrics();
```

## Performance Optimization

### Caching Strategies

Implement caching for large codebases:

```javascript
// cache-manager.js
const fs = require('fs');
const crypto = require('crypto');

class DocumentationCache {
  constructor(cacheDir = '.doc-cache') {
    this.cacheDir = cacheDir;
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir);
    }
  }
  
  getCacheKey(filePath, content) {
    const hash = crypto.createHash('md5').update(content).digest('hex');
    return `${filePath.replace(/\//g, '_')}_${hash}`;
  }
  
  get(filePath, content) {
    const key = this.getCacheKey(filePath, content);
    const cachePath = `${this.cacheDir}/${key}`;
    
    if (fs.existsSync(cachePath)) {
      return JSON.parse(fs.readFileSync(cachePath, 'utf8'));
    }
    return null;
  }
  
  set(filePath, content, result) {
    const key = this.getCacheKey(filePath, content);
    const cachePath = `${this.cacheDir}/${key}`;
    fs.writeFileSync(cachePath, JSON.stringify(result));
  }
}
```

### Selective Processing

Process only what's needed:

```bash
# Skip already documented files
find . -name "*.js" | while read file; do
  if ! grep -q "@param\|@returns" "$file"; then
    echo "Processing $file (no docs found)..."
    ./doc-generator.js "$file"
  fi
done
```

### Memory Management

For very large files:

```javascript
// Process in chunks
const stream = fs.createReadStream(largeFile, { encoding: 'utf8' });
let buffer = '';

stream.on('data', chunk => {
  buffer += chunk;
  // Process complete functions
  const functions = extractCompleteFunctions(buffer);
  processFunctions(functions);
  // Keep only incomplete function at end
  buffer = extractIncompletePart(buffer);
});
```

## Advanced Examples

### Custom Documentation Pipeline

```bash
#!/bin/bash
# advanced-doc-pipeline.sh

# 1. Analyze current state
echo "📊 Analyzing documentation coverage..."
./doc-generator.js --dry-run > initial-report.txt

# 2. Generate basic documentation
echo "📝 Generating basic documentation..."
./doc-generator.js --no-enhance

# 3. Enhance with Claude (if available)
if command -v claude &> /dev/null; then
  echo "🤖 Enhancing with Claude AI..."
  find . -name "*.js" -newer initial-report.txt | while read file; do
    claude enhance-docs "$file"
  done
fi

# 4. Validate documentation
echo "✅ Validating documentation..."
npx jsdoc -t ./node_modules/better-docs -c jsdoc.json -d docs

# 5. Generate final report
echo "📈 Generating final report..."
./doc-generator.js --dry-run > final-report.txt

# 6. Show improvements
echo "📊 Documentation improvements:"
diff initial-report.txt final-report.txt
```

## Summary

You've learned advanced techniques for:
- Handling complex code structures
- Customizing documentation output
- Integrating with git hooks and CI/CD
- Managing large codebases efficiently
- Working with multi-language projects
- Implementing team workflows
- Optimizing performance

These advanced features help you maintain high-quality documentation at scale, ensuring your codebase remains maintainable and well-documented as it grows.