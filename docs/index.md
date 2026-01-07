# k3handy

[![Action-CI](https://github.com/pykit3/k3handy/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3handy/actions/workflows/python-package.yml)
[![Documentation Status](https://readthedocs.org/projects/k3handy/badge/?version=stable)](https://k3handy.readthedocs.io/en/stable/?badge=stable)
[![Package](https://img.shields.io/pypi/pyversions/k3handy)](https://pypi.org/project/k3handy)

Handy alias of mostly used functions. A collection of utility shortcuts for common operations.

k3handy is a component of [pykit3](https://github.com/pykit3) project: a python3 toolkit set.

## Installation

```bash
pip install k3handy
```

## Quick Start

```python
from k3handy import fread, fwrite, cmdx, dd

# File operations
fwrite('/tmp/hello.txt', 'Hello World')
content = fread('/tmp/hello.txt')

# Command execution
cmdx('ls', '-la')

# Debug output
dd('debug message')
```

## API Reference

::: k3handy

## License

The MIT License (MIT) - Copyright (c) 2015 Zhang Yanpo (张炎泼)
