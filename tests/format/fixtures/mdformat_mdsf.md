basic code block formatting
.
```python
x=1
```
.
```python
x = 1
```
.

code block with multiple lines
.
```python
def hello():
    x=1+2
    return x
```
.
```python
def hello():
    x = 1 + 2
    return x
```
.

empty code block
.
```python
```
.
```python
```
.

code block with trailing newline
.
```python
def foo():
    pass

```
.
```python
def foo():
    pass
```
.

multiple code blocks
.
```python
x = 1
```

Some text

```javascript
const y = 2;
```
.
```python
x = 1
```

Some text

```javascript
const y = 2;
```
.

nested lists with code
.
- Item 1
  - Nested item
    ```python
    code_here()
    ```
  - Another nested
- Item 2
.
- Item 1
  - Nested item
    ```python
    code_here()
    ```
  - Another nested
- Item 2
.

code in blockquote
.
> Here's some code:
>
> ```python
> def example():
>     pass
> ```
.
> Here's some code:
>
> ```python
> def example():
>     pass
> ```
.

mixed content with headers
.
# Header 1

```python
import os
```

## Header 2

Some **bold** and *italic* text.

```javascript
console.log("test");
```

### Header 3

- List item
.
# Header 1

```python
import os
```

## Header 2

Some **bold** and *italic* text.

```javascript
console.log("test");
```

### Header 3

- List item
.

code with info string variations
.
```py
x = 1
```

```PYTHON
y = 2
```
.
```py
x = 1
```

```PYTHON
y = 2
```
.

code with link in paragraph
.
See [documentation](https://example.com) for details.

```python
result = process()
```
.
See [documentation](https://example.com) for details.

```python
result = process()
```
.

indented code in list
.
1. First item with code:
   ```python
   def step_one():
       return True
   ```
2. Second item
   ```python
   def step_two():
       return False
   ```
.
1. First item with code:
   ```python
   def step_one():
       return True
   ```
1. Second item
   ```python
   def step_two():
       return False
   ```
.

table with code blocks after
.
| Column 1 | Column 2 |
| -------- | -------- |
| Value 1  | Value 2  |

```python
table_data = load_data()
```
.
| Column 1 | Column 2 |
| -------- | -------- |
| Value 1 | Value 2 |

```python
table_data = load_data()
```
.
