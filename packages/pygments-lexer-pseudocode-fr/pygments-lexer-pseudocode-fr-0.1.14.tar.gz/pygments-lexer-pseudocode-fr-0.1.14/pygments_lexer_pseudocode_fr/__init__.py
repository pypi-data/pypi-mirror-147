import re

from pygments.lexer import RegexLexer, include, bygroups, using, this
# from pygments.style import Style
from pygments.token import Error, Punctuation, Text, Comment, Operator, Keyword, Name, String, Number, Generic

# class PseudocodefrStyle(Style):
#     """Custom Style for Pseudocode fr"""
#     default_style = ""
#     styles = {
#         Comment:                'italic #888',
#         Keyword:                'bold #005',
#         Name:                   '#f00',
#         Name.Function:          '#0f0',
#         Name.Class:             'bold #0f0',
#         String:                 'bg:#eee #111'
#     }

class PseudocodefrLexer(RegexLexer):
    '''
    A Pseudo code (fr) lexer
    '''
    name = 'Pseudocode'
    aliases = ['pseudocode', 'pseudo', 'pseudofr', 'algorithme', 'algo']
    filenames = ['*.algo', '*.pseudocode']
    mimetypes = []
    flags = re.IGNORECASE

    def op_replace(lexer, match):
        op = match.group(0)
        # S = ('<=', '>=', '<>', '!=', '<-', '->', '^')
        # R = ('≤',  '≥',  '≠',  '≠', '←', '→', '↑')
        S = ('<=', '>=', '<>', '!=', '<-', '->')
        R = ('≤',  '≥',  '≠',  '≠', '←', '→')

        if op in S:
            op = R[S.index(op)]

        yield match.start(), Operator, op

    def greek_replace(lexer, match):
        greek_letter = match.group(0)
        
        S = ('\\alpha', '\\beta','\\gamma','\\delta','\\epsilon','\\zeta','\\eta','\\theta','\\iota','\\kappa','\\lambda','\\mu','\\nu','\\xi', '\omicron', '\\pi','\\rho','\\sigma','\\tau','\\upsilon','\\phi', '\\chi','\\psi','\\omega',
        '\\Alpha', '\\Beta','\\Gamma','\\Delta','\\Epsilon','\\Zeta','\\Eta','\\Theta','\\Iota','\\Kappa','\\Lambda','\\Mu','\\Nu','\\Xi', '\Omicron', '\\Pi','\\Rho','\\Sigma','\\Tau','\\Upsilon','\\Phi', '\\Chi','\\Psi','\\Omega')
        R = ('α'      , 'β'     , 'γ'     , 'δ'     , 'ε'       , 'ζ'    , 'η'   , 'θ'     , 'ι'    , 'κ'     , 'λ'      , 'μ'   , 'ν' , 'ξ'  , 'ο'       , 'π'   , 'ρ'   , 'σ'     , 'τ'   , 'υ'       , 'φ'   , 'χ'    , 'ψ'   , 'ω',
             'Α'      , 'Β'     , 'Γ'     , 'Δ'     , 'Ε'       , 'Ζ'    , 'Η'   , 'Θ'     , 'Ι'    , 'Κ'     , 'Λ'      , 'Μ'   , 'Ν' , 'Ξ'  , 'Ο'       , 'Π'   , 'Ρ'   , 'Σ'     , 'Τ'   , 'Υ'       , 'Φ'   , 'Χ'    , 'Ψ'   , 'Ω')

        if greek_letter in S:
            greek_letter = R[S.index(greek_letter)]

        yield match.start(), Name.Constant, greek_letter

    def symb_replace(lexer, match):
        symbol = match.group(0)
        
        S = ('\\varnothing', '\\void', '\\in', '\\notin', '\\subset', '\\supset', '\\cap', '\\cup')
        R = ('∅'          , '∅'     , '∈'   , '∉'       , '⊂'       , '⊃'       , '⋂'  , '⋃')

        if symbol in S:
            symbol = R[S.index(symbol)]

        yield match.start(), Name.Constant, symbol

    def scomment(lexer, match):
        s = match.group(1).lower().strip()
        c = Comment

        directives = ['passage par copie', 'passage par valeur', 'passage par référence', 'passage par reference', 'passage par adresse', 've', 'vs', 've/s']

        if s in directives:
            c = Comment.Special

        yield match.start(), c, match.group(0)

    tokens = {
            'root': [
                    (r'\/\*.*\*\/', Comment),
                    (r'(\/\/|#).*\n', Comment),
                    (r'\|', Comment),
                    (r'\{(.*)\}', scomment),
                    include('strings'),
                    include('core'),
                    (r'[a-zéàèùçâêîôûÉÀÈÒÙÇÂÊÎÔÛ][a-z0-9éàèùçâêîôûÉÀÈÙÒÇÂÊÎÔÛ_]*', Name.Variable),
                    include('nums'),
                    (r'[\s]+', Text)
            ],
            'core':[ # Statements
                    (r'\b(debut|début|fin|si|alors|sinon|fin[_ ]?si|tant[ _]?que|tantque|fin[ _]?tant[ _]?que|faire|répéter|'
                    r'repeter|type|structure|fin[ _]?structure|fonction|procédure|procedure|retourner|renvoyer|'
                    r'pour|variant|allant|de|fin[ _]?pour|à|déclarations?|jusque|spécialise|specialise|comporte|super|public|privé|protégé|'
                    r'est|vaut|prend la valeur|affecter|'
                    r'classe'
                    r')\s*\b', Keyword),

                    # Data Types
                    (r'\b(entiers?|chaines?|chaînes?|réels?|reels?|flottants?|caractères?|caracteres?|booléens?|'
                    r'booleens?|tableaux?|listes?|files?|piles?|verrous?|sémaphores?|semaphores?|rien)\s*\b', 
                    Keyword.Type),

                    # Greek Letters Replace
                    (r'(\\alpha|\\beta|\\gamma|\\delta|\\epsilon|\\zeta|\\eta|\\theta|\\iota|\\kappa|\\lambda|\\mu|\\nu|\\xi|\\pi|\\rho|\\sigma|\\tau|\\upsilon|\\phi|\\chi|\\psi|\\omega|'
                    r'\\Alpha|\\Beta|\\Gamma|\\Delta|\\Epsilon|\\Zeta|\\Eta|\\Theta|\\Iota|\\Kappa|\\Lambda|\\Mu|\\Nu|\\Xi|\\Pi|\\Rho|\\Sigma|\\Tau|\\Upsilon|\\Phi|\\Chi|\\Psi|\\Omega)',
                    greek_replace),

                    # Symbols Replace
                    (r'(\\varnothing|\\void|\\in|\\notin|\\subset|\\supset|\\cap|\\cup)',
                    symb_replace),

                    (r'\b(variable|var|vrai|faux|nil|nul|vide)\s*\b',
                    Name.Constant),
                    
                    # Operators
                    # (r'(<=|>=|<>|!=|<-|\^|\*|\+|-|\/|<|>|=|\\\\|mod|←|↑|→|≤|≥|≠|÷|×|\.\.|\[|\]|\.|non|xou|et|ou)',
                    # op_replace),
                    (r'(<=|>=|<>|!=)',
                    op_replace),

                    (r'(\(|\)|\,|\;|:)',
                    Punctuation),

                    #(r'\b(\[(VE|VS|VE/S)\])\s*\b',
                    # Keyword.Declaration),

                    # Intrinsics
                    (r'\b(sqrt|pow|cos|sin|tan|arccos|arcsin|arctan|arctan2|lire|ecrire|écrire|'
                    r'pi|saisir|afficher|'
                    r'exp|ln|log|log2|détruire|detruire'
                    r')\s*\b', Name.Builtin)
                    ],

            'strings': [
                    (r'"([^"])*"', String.Double),
                    (r"'([^'])*'", String.Single),
                    ],

            'nums': [
                    (r'\d+(?![.Ee])', Number.Integer),
                    (r'[+-]?\d*\.\d+([eE][-+]?\d+)?', Number.Float),
                    (r'[+-]?\d+\.\d*([eE][-+]?\d+)?', Number.Float)
                    ],
            }
