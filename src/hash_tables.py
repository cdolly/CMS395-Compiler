
# IDENTIFIER HASH TABLE
IDENTIFIER_HASH_TABLE = {x: None for x in range(500)}

# KEYWORD HASH TABLE
KEYWORD_HASH_TABLE = {
    '2': 'program',
    '3': 'begin',
    '4': 'end',
    '6': 'declare',
    '10': 'if',
    '11': 'then',
    '12': 'else',
    '13': 'end_if',
    '14': 'odd',
    '18': 'while',
    '19': 'loop',
    '20': 'end_loop',
    '21': 'input',
    '22': 'output',
    '30': 'Real',
    '31': 'Integer',
    '32': 'Boolean',
    '36': 'var',
    '37': 'const',
    '38': 'call',
    '39': 'procedure',
}

OPERATOR_HASH_TABLE = {
    '5': ';',
    '7': ',',
    '8': ':=',
    '9': '.',
    '15': ':',
    '16': '{',
    '17': '}',
    '23': '+',
    '24': '-',
    '25': '*',
    '26': '/',
    '27': '(',
    '28': ')',
    '33': '=',
    '34': 'EOL',
    '35': 'EOF',
    '40': '<>',
    '41': '<',
    '42': '>',
    '43': '>=',
    '44': '<=',
}


DOUBLE_CHAR_OPERATORS_FIRST = ['15', '41', '42']
DOUBLE_CHAR_OPERATORS_SECOND = {
    ('15', '='): '8',
    ('41', '>'): '40',
    ('41', '='): '44',
    ('42', '='): '43'
}
