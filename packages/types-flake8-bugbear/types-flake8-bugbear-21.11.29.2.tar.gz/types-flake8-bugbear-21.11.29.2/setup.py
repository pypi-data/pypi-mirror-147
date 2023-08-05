from setuptools import setup

name = "types-flake8-bugbear"
description = "Typing stubs for flake8-bugbear"
long_description = '''
## Typing stubs for flake8-bugbear

This is a PEP 561 type stub package for the `flake8-bugbear` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `flake8-bugbear`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/flake8-bugbear. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `7a3eb5a4818664d7619ea6ec664c280d0a64c7ee`.
'''.lstrip()

setup(name=name,
      version="21.11.29.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-bugbear.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['bugbear-stubs'],
      package_data={'bugbear-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
