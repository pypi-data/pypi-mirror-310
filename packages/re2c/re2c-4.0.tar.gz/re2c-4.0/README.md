# re2c Python Distributions

[![PyPI Release](https://img.shields.io/pypi/v/re2c.svg)](https://pypi.org/project/re2c)

[re2c](https://re2c.org/) is a free and open-source lexer generator for C, C++, D, Go, Haskell, Java, JS, OCaml, Python, Rust, V and Zig with a focus on generating fast code.

This project packages the `re2c` utility (aliases for other languages such as `re2go` are also provided) as a Python package, enabling `re2c` to be installed from PyPI:

```
pip install re2c
```

or used as part of `build-system.requires` in a pyproject.toml file:

```toml
[build-system]
requires = ["re2c"]
```

PyPI package versions will follow the `major.minor.patch` version numbers of re2c releases.

Binary wheels for Windows, macOS, and Linux for most CPU architectures supported on PyPI are provided. ARM wheels for Raspberry Pi available at https://www.piwheels.org/project/re2c/.

[re2c PyPI Package Homepage](https://github.com/nightlark/re2c-python-distributions)

[re2c Homepage](https://re2c.org/)

[re2c Source Code](https://github.com/skvadrik/re2c)

[re2c License](https://github.com/skvadrik/re2c/blob/master/LICENSE): Public domain

Installing re2c
===============

re2c can be installed by pip with:

```sh
pip install re2c
```

or:

```sh
python -m pip install re2c
```

Building from the source dist package requires internet access in order to download a copy of the re2c source code.

Using with pipx
===============

Using `pipx run re2c <args>` will run re2c without any install step, as long as the machine has pipx installed (which includes GitHub Actions runners).

Using with pyproject.toml
=========================

re2c can be added to the `build-system.requires` key in a pyproject.toml file for building Python extensions that use re2c to generate code.

```toml
[build-system]
requires = ["re2c"]
```
