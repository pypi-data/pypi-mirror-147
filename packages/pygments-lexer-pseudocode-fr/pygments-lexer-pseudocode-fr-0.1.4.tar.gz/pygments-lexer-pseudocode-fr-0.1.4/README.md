# (French) Pseudocode syntax lexer for Pygments

This package contains a Pygments Lexer for some basic pseudocode algorithmics.

## Installation

The lexer is available as a Pip package:

    pip install pygments-lexer-pseudocode

Alternatively, to install from the git repository: (you may need to sudo depending on your Python environment)

    python setup.py install

## Usage

After installation the Pseudocode lexer automatically registers itself for files with the `.algo` and `.pseudocode` extensions. Therefore, usage is easy:

    pygmentize document.algo

You can also manally indicate you want to use the Pseudocode lexer by using a command line flag:

    pygmentize -l pseudocode somefile 

## Contribute

If you found a bug, don't hesitate to make a pull request.

## License

The Pseudocode lexer is licensed under the terms of the MIT licence
