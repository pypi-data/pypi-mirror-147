from setuptools import setup

VERSION = '0.1.6'

setup(
    name="pygments-lexer-pseudocode-fr",
    packages=["pygments_lexer_pseudocode_fr"],
    version=VERSION,
    install_requires=[ "pygments" ],
    keywords='pygments lexer syntax highlight pseudo pseudocode algorithme fr',
    entry_points="""[pygments.lexers]
    pseudocodefr = pygments_lexer_pseudocode_fr:PseudocodefrLexer

    [pygments.styles]
    pseudocodefrstyle = pygments_lexer_pseudocode_fr:PseudocodefrStyle
    """,
    author="Rodrigo Schwencke",
    author_email="rod2ik.dev@gmail.com",
    description="Pygments Lexer for French Pseudocode",
    long_description_content_type="text/markdown",
    long_description="""Project Page : [rod2ik/pygments-lexer-pseudocode-fr](https://gitlab.com/rod2ik/pygments-lexer-pseudocode-fr)

Some examples in these pages:

* MkHack3rs : https://eskool.gitlab.io/mkhack3rs/pseudocode/

This project is one of others mkdocs-related projects.  
Please have a look at this page for a more complete view of all projects compatible with for mkdocs:

* https://eskool.gitlab.io/mkhack3rs/

This project was initially a continuation of the great job of (from newer to older) :

* All newer Credits: [rod2ik/pygments-lexer-pseudocode-fr](https://gitlab.com/rod2ik/pygments-lexer-pseudocode-fr)
* Simon Watcher [svvac/pygments-lexer-pseudocode](https://github.com/svvac/pygments-lexer-pseudocode)
    
In order to get it work with pip, and ultimately with mkdocs and mkdocs-material.

Licences:

* All newer parts (Rodrigo Schwencke) are [GPLv3+](https://opensource.org/licenses/GPL-3.0)
* Older parts (Simon Watcher) are [MIT License](http://www.opensource.org/licenses/mit-license.php)""",
    url="https://gitlab.com/rod2ik/pygments-lexer-pseudocode-fr.git",
    license="GPLv3+",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        "Natural Language :: French",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',

    ]
)
