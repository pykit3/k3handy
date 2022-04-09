# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3handy",
    packages=["k3handy"],
    version="0.1.7",
    license='MIT',
    description='handy alias of mostly used functions',
    long_description='# k3handy\n\n[![Action-CI](https://github.com/pykit3/k3handy/actions/workflows/python-package.yml/badge.svg)](https://github.com/pykit3/k3handy/actions/workflows/python-package.yml)\n[![Build Status](https://travis-ci.com/pykit3/k3handy.svg?branch=master)](https://travis-ci.com/pykit3/k3handy)\n[![Documentation Status](https://readthedocs.org/projects/k3handy/badge/?version=stable)](https://k3handy.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3handy)](https://pypi.org/project/k3handy)\n\nhandy alias of mostly used functions\n\nk3handy is a component of [pykit3] project: a python3 toolkit set.\n\n\nk3handy is collection of mostly used  utilities.\n\n\n\n# Install\n\n```\npip install k3handy\n```\n\n# Synopsis\n\n```python\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3handy',
    keywords=['handy', 'shortcut'],
    python_requires='>=3.0',

    install_requires=['k3fs<0.2,>=0.1.5', 'k3proc<0.3,>=0.2.13', 'k3str<0.2,>=0.1.4', 'k3ut>=0.1.15,<0.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
