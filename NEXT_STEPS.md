# Next steps

- CI is red on `prek-hook` and on `tests (3.14, windows-latest)`, and was already red on `main` before the 2.10.0 copier update (same failure on `0a591dd`), so it is unrelated to that update
    - `prek-hook`: `mdsf format --stdin | typos - --write-changes` fails with `typos: not found`. `.config/mise.ci.toml` pins `cargo:typos-cli`, but the `jdx/mise-action` step in `tests.yml` reports "all tools are installed" without actually installing it, so `typos` is missing from `PATH` when `.mdformat.toml`'s `post_command` runs. Root cause not confirmed, the local repro attempts (mirroring the same `.config/mise.toml` + inline root `mise.toml` MISE_ENV split) did not reproduce it
    - Windows: `test_mdformat_post_command_receives_trailing_newline` fails with `AssertionError` and `The filename, directory name, or volume label syntax is incorrect`, a separate, likely shell-quoting related failure specific to `windows-latest`
- The known `POSTPROCESSORS` keyed on `"document"` instead of `"root"` bug is not present in this repo. `mdformat_hooks/plugin.py` already keys `POSTPROCESSORS` on `ROOT_NODE_TYPE = "root"`
