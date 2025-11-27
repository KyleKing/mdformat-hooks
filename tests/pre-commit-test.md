# mdformat-mdsf Pre-commit Test File

This file tests various markdown structures with code blocks.

## Basic Code Blocks

### Python Example

```python
def hello():
    print("world")
```

### JavaScript Example

```javascript
function hello() {
   console.log("world");
}
```

### JSON Example

```json
{
   "name": "test",
   "version": "1.0.0"
}
```

## Nested Structures

### Code in Lists

1. First item with code:

   ```python
   def step_one():
       return True
   ```

1. Second item with multiple paragraphs

   Some explanation text.

   ```python
   def step_two():
       return False
   ```

1. Third item with nested list:

   - Nested item A
   - Nested item B with code:
     ```python
     nested_code = "value"
     ```
   - Nested item C

### Code in Blockquotes

> This is a quote with code:
>
> ```python
> def example():
>     pass
> ```

> Multiple blockquotes
>
> ```javascript
> const example = () => {};
> ```

## Complex Nesting

### Code in Definition Lists

- **Term 1**: Definition with code

  ```python
  def term_one():
      return "definition"
  ```

- **Term 2**: Another definition

  ```javascript
  function termTwo() {
     return "definition";
  }
  ```

### Mixed Content

Here's a paragraph with **bold** and _italic_ text, followed by code:

```python
import os
import sys


def main():
    print("Hello, World!")
    return 0
```

And another paragraph with [a link](https://example.com).

```javascript
// JavaScript example
const greet = (name) => {
   console.log(`Hello, ${name}!`);
};

greet("World");
```

## Tables with Code

| Language | Example |
| ---------- | ------------------------ |
| Python | `print("hello")` |
| JavaScript | `console.log("hello")` |
| Ruby | `puts "hello"` |

After the table, some code:

```python
table_data = [
    {"language": "Python", "example": 'print("hello")'},
    {"language": "JavaScript", "example": 'console.log("hello")'},
]
```

## Edge Cases

### Empty Code Block

```python
```

### Code Block with Only Whitespace

```python

```

### Multiple Languages

```python
x = 1
y = 2
```

```javascript
const x = 1;
const y = 2;
```

```rust
let x = 1;
let y = 2;
```

### Code with Backticks Inside

```python
code = """
Some multiline string
with `backticks` inside
"""
```

## Deeply Nested Example

1. Level 1
   1. Level 2
      1. Level 3 with code:
         ```python
         def deeply_nested():
             return "works"
         ```
   1. Back to level 2
      - Bullet in level 2
      - Another bullet with code:
        ```javascript
        const nested = true;
        ```
1. Back to level 1

## Horizontal Rules and Code

______________________________________________________________________

```python
after_hr = "code after horizontal rule"
```

______________________________________________________________________

## Multiple Code Blocks in Sequence

```python
block1 = "first"
```

```python
block2 = "second"
```

```python
block3 = "third"
```

## End of Test File

This file should remain idempotent when formatted with mdformat-mdsf.
