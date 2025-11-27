# mdformat Test Refactoring Reference

Complete phase-by-phase guide for refactoring mdformat plugin tests to pytest best practices.

## Prerequisites

- Tox configured for the project
- pytest installed as test runner
- Ruff or similar linter configured
- Reference repository: [mdformat-mkdocs](https://github.com/KyleKing/mdformat-mkdocs)

## Phase 1: Assessment & Analysis

### Step 1.1: Identify Current Issues

```bash
# Run tox to see all errors and warnings
tox

# Focus on linting output (ruff, pylint, etc.)
tox -e ruff
```

**Look for:**

- PLR6301: "Method could be a function, class method, or static method"
- Unittest.TestCase classes that should be functions
- Missing test parametrization
- Duplicate test logic

### Step 1.2: Analyze Current Test Structure

```bash
# Read all test files
fd -e py . tests/

# Review test organization
tree tests/
```

**Document:**

- Which files use unittest.TestCase classes?
- Which tests have similar logic (candidates for parametrization)?
- Are there fixture files or external test data?
- What's the current test count and coverage?

### Step 1.3: Research Best Practices

```bash
# Clone reference repository for patterns
git clone https://github.com/KyleKing/mdformat-mkdocs /tmp/mdformat-mkdocs

# Study test patterns
rg "@pytest.mark.parametrize" /tmp/mdformat-mkdocs/tests/
rg "class Test" /tmp/mdformat-mkdocs/tests/
rg "def test_" /tmp/mdformat-mkdocs/tests/
```

**Key patterns to identify:**

1. How are fixtures loaded from files?
1. How is parametrization structured?
1. When are classes used vs functions?
1. What helper functions exist?
1. How are IDs assigned to parametrized tests?

## Phase 2: Planning

### Step 2.1: Create Refactoring Todo List

Create a todo list with these typical tasks:

```markdown
- [ ] Refactor test_integration.py to use standalone functions
- [ ] Add pytest.mark.parametrize to consolidate similar tests
- [ ] Improve test_mdformat.py with parametrization patterns
- [ ] Create test helpers module if needed
- [ ] Add fixture files for data-driven tests
- [ ] Run tox to verify all fixes
```

### Step 2.2: Identify Test Categories

Categorize tests into:

**A. Conditional Tests (Keep as classes or use skipif on functions)**

- Tests requiring external dependencies (e.g., mdsf binary)
- Platform-specific tests
- Optional feature tests

Example:

```python
@pytest.mark.skipif(not DEPENDENCY_AVAILABLE, reason="dependency not installed")
def test_feature() -> None:
    pass
```

**B. Parametrizable Tests**

- Tests with similar logic but different inputs
- Multiple language/format tests
- Configuration option tests
- Edge case tests

Example:

```python
@pytest.mark.parametrize("language", ["python", "rust", "go"])
def test_languages(language: str) -> None:
    pass
```

**C. Standalone Tests**

- Unique test logic
- Smoke tests
- Idempotency tests

## Phase 3: Refactoring

### Step 3.1: Refactor Integration Tests

**Before (Unittest Class):**

```python
@pytest.mark.skipif(shutil.which("tool") is None, reason="tool not installed")
class TestWithTool:
    def test_feature_one(self) -> None:
        # test code

    def test_feature_two(self) -> None:
        # test code
```

**After (Standalone Functions):**

```python
TOOL_AVAILABLE = shutil.which("tool") is not None

@pytest.mark.skipif(not TOOL_AVAILABLE, reason="tool not installed")
def test_feature_one() -> None:
    # test code

@pytest.mark.skipif(not TOOL_AVAILABLE, reason="tool not installed")
def test_feature_two() -> None:
    # test code
```

### Step 3.2: Apply Parametrization

**Pattern 1: Simple Parametrization**

````python
@pytest.mark.parametrize(
    "language",
    ["python", "javascript", "typescript", "rust"],
    ids=["python", "javascript", "typescript", "rust"],
)
def test_multiple_languages(language: str) -> None:
    unformatted = f"```{language}\ncode\n```"
    result = mdformat.text(unformatted, codeformatters={language})
    assert f"```{language}" in result
````

**Pattern 2: Multiple Parameters**

```python
@pytest.mark.parametrize(
    ("text", "options", "expected"),
    [
        ("input1", {"opt": True}, "output1"),
        ("input2", {"opt": False}, "output2"),
        ("input3", {"opt": True, "other": 5}, "output3"),
    ],
    ids=["with_opt", "without_opt", "multiple_opts"],
)
def test_configurations(text: str, options: dict, expected: str) -> None:
    result = mdformat.text(text, options=options)
    assert expected in result
```

**Pattern 3: Consolidating Edge Cases**

````python
@pytest.mark.parametrize(
    ("description", "code_content"),
    [
        ("empty_block", ""),
        ("whitespace_only", "   \n  "),
        ("single_line", "x = 1"),
        ("with_trailing_newline", "def hello():\n    pass\n\n"),
    ],
    ids=["empty_block", "whitespace_only", "single_line", "with_trailing_newline"],
)
def test_edge_cases(description: str, code_content: str) -> None:
    unformatted = f"```python\n{code_content}```"
    result = format_code(unformatted)
    assert "```python" in result
````

### Step 3.3: Add Essential Tests

**Idempotency Test:**

````python
def test_idempotency() -> None:
    """Test that formatting is idempotent (formatting twice gives same result)."""
    text = """# Example\n\n```python\ncode\n```"""
    result1 = mdformat.text(text, codeformatters={"python"})
    result2 = mdformat.text(result1, codeformatters={"python"})
    assert result1 == result2, "Formatting should be idempotent"
````

**Smoke Test:**

```python
def test_plugin_loads() -> None:
    """Verify that the plugin loads without errors."""
    pth = Path(__file__).parent / "pre-commit-test.md"
    content = pth.read_text()
    result = mdformat.text(content, codeformatters={"python"})
    pth.write_text(result)  # Easier to debug with git
    assert result == content, "Differences found. Review in git."
```

### Step 3.4: Create Test Helpers (Optional)

If tests become complex, create `tests/helpers.py`:

```python
"""Test helper utilities."""

from __future__ import annotations

import os

_SHOW_TEXT = os.environ.get("SHOW_TEST_TEXT", "false").lower() == "true"


def print_text(output: str, expected: str, show_whitespace: bool = False) -> None:
    """Print text for debugging when SHOW_TEST_TEXT=true."""
    if _SHOW_TEXT:
        print("--  Output  --")
        print(repr(output) if show_whitespace else output)
        print("-- Expected --")
        print(repr(expected) if show_whitespace else expected)
        print("--  <End>   --")


def format_with_plugin(
    text: str,
    *,
    codeformatters: set[str] | None = None,
    options: dict[str, object] | None = None,
) -> str:
    """Format text with the plugin using consistent defaults."""
    import mdformat

    return mdformat.text(
        text,
        codeformatters=codeformatters or set(),
        options=options or {},
    )
```

## Phase 4: Verification

### Step 4.1: Run Tests Locally

```bash
# Run all tests
tox

# Run specific test environment
tox -e test

# Run with verbose output
tox -e test -- -vv

# Run specific test file
tox -e test -- tests/test_integration.py

# Run specific test
tox -e test -- tests/test_integration.py::test_python_formatting
```

### Step 4.2: Verify Linting Passes

```bash
# Run linter
tox -e ruff

# Auto-fix issues
tox -e ruff -- --unsafe-fixes

# Run pre-commit hooks
tox -e prek
```

### Step 4.3: Check Coverage

```bash
# Run with coverage
tox -e test -- --cov=your_package --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Step 4.4: Verify Test Count

```bash
# Count tests before refactoring
pytest --collect-only tests/ | grep "test session starts" -A 2

# Count tests after refactoring
pytest --collect-only tests/ | grep "test session starts" -A 2

# Compare: Should have same or more tests after parametrization
```

## Phase 5: Documentation

### Step 5.1: Update Test Documentation

Update `AGENTS.md` or similar with new test patterns:

```markdown
## Testing

### Running Tests

\`\`\`bash
# Run all tests
tox

# Run specific test with parametrized cases
tox -e test -- tests/test_integration.py::test_multiple_languages

# Show all test IDs
pytest --collect-only tests/
\`\`\`

### Test Organization

- `test_mdformat.py`: Core formatting tests with parametrization
- `test_integration.py`: Integration tests (require external dependencies)
- `helpers.py`: Shared test utilities

### Adding New Tests

Use parametrization for related tests:

\`\`\`python
@pytest.mark.parametrize(
    ("input_text", "expected_output"),
    [
        ("case1", "result1"),
        ("case2", "result2"),
    ],
    ids=["case1_description", "case2_description"],
)
def test_new_feature(input_text: str, expected_output: str) -> None:
    result = your_function(input_text)
    assert result == expected_output
\`\`\`
```

### Step 5.2: Update CI/CD

Ensure CI runs all tox environments:

```yaml
# .github/workflows/test.yml
  - name: Run tests
    run: tox -e test,ruff,type,prek
```

## Troubleshooting

### Issue: Tests fail after refactoring

```bash
# Compare test behavior before/after
git stash
tox -e test  # Run old tests
git stash pop
tox -e test  # Run new tests
```

### Issue: Parametrization not working

- Ensure parameter names match function arguments exactly
- Check that IDs list length matches test cases length
- Verify tuples have correct number of elements

### Issue: Skipif not working

- Check condition logic (use `not CONDITION` for skipif)
- Verify constant is defined before decorator
- Test manually: `python -c "import shutil; print(shutil.which('binary'))"`

### Issue: Linter still complains

- Run auto-fix: `tox -e ruff -- --fix`
- Check for leftover class methods not converted
- Verify all functions have type hints

## Verification Checklist

Before considering refactoring complete, verify:

- [ ] All tox environments pass
- [ ] No linter errors (ruff/pylint)
- [ ] Test count is maintained or increased
- [ ] Coverage is maintained or improved
- [ ] All test IDs are meaningful and unique
- [ ] Parametrized tests use clear, descriptive IDs
- [ ] Integration tests properly skip when dependencies unavailable
- [ ] Idempotency test exists for formatting
- [ ] Smoke test verifies plugin loads
- [ ] Documentation updated with new patterns
- [ ] CI/CD updated if needed
- [ ] Git diff shows only test files changed (no accidental source changes)

## Example Commit Message

```
refactor(tests): migrate to pytest best practices

- Convert unittest classes to standalone functions
- Add extensive parametrization for similar test cases
- Consolidate edge case tests using pytest.mark.parametrize
- Add idempotency and smoke tests
- Improve test organization and readability

Changes:
- test_integration.py: 6 class methods → 7 parametrized functions
- test_mdformat.py: Enhanced with 4 new parametrized test cases
- Total test count: 9 → 28 (with parametrization)

Resolves: PLR6301 linter warnings
All tox environments pass: ✓
```
