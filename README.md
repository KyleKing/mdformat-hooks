# mdformat-mdformat-mdsf

[![Build Status][ci-badge]][ci-link] [![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin for `<placeholder>`

## `mdformat` Usage

Add this package wherever you use `mdformat` and the plugin will be auto-recognized. No additional configuration necessary. See [additional information on `mdformat` plugins here](https://mdformat.readthedocs.io/en/stable/users/plugins.html)

### pre-commit / prek

```yaml
repos:
  - repo: https://github.com/executablebooks/mdformat
    rev: 0.7.19
    hooks:
      - id: mdformat
        additional_dependencies:
          - mdformat-mdformat-mdsf
```

### uvx

```sh
uvx --from mdformat-mdformat-mdsf mdformat
```

Or with pipx:

```sh
pipx install mdformat
pipx inject mdformat mdformat-mdformat-mdsf
```

## HTML Rendering

To generate HTML output, `mdformat_mdsf_plugin` can be imported from `mdit_plugins`. For more guidance on `MarkdownIt`, see the docs: <https://markdown-it-py.readthedocs.io/en/latest/using.html#the-parser>

```py
from markdown_it import MarkdownIt

from mdformat_mdformat_mdsf.mdit_plugins import mdformat_mdsf_plugin

md = MarkdownIt()
md.use(mdformat_mdsf_plugin)

text = "... markdown example ..."
md.render(text)
# <div>
#
# </div>
```

## Contributing

See [CONTRIBUTING.md](https://github.com/kyleking/mdformat-mdformat-mdsf/blob/main/CONTRIBUTING.md)

[ci-badge]: https://github.com/kyleking/mdformat-mdformat-mdsf/workflows/CI/badge.svg?branch=main
[ci-link]: https://github.com/kyleking/mdformat-mdformat-mdsf/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-mdformat-mdsf.svg
[pypi-link]: https://pypi.org/project/mdformat-mdformat-mdsf
