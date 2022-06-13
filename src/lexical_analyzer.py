import constants
import re
import hash_tables


def analyze_file(filename):
    try:
        final = []
        file = open(filename, 'r')
        lines = file.readlines()
        i = 0
        for line in lines:
            (tokens, error_stack) = tokenize(line)
            print(
                f'\nProgram line number: {i+1}\n'
                f'Input statement: {line.strip()}\n'
                f'Tokens: {" * ".join(tokens)}'
            )
            for err in error_stack:
                print(err)
            i += 1

            # for return value
            final += tokens

        print(f'\nEOF Token {constants.EOF}\n')
        final += [constants.EOF]

        return final
    except FileNotFoundError:
        print(f'{constants.WARNING} Invalid filename')


def tokenize(line):
    '''
    takes a line of the program and returns a string of tokens and an array of errors
    '''
    i = 0
    character = None
    tokens = []
    error_stack = []

    while i < len(line):
        character = line[i]

        is_char = re.search(constants.REGEX_CHAR, character)
        is_num = re.search(constants.REGEX_NUM, character)
        is_blank = re.search(constants.REGEX_WHITESPACE, character)

        operator = None
        is_dbl_operator = False
        for operator_key in hash_tables.OPERATOR_HASH_TABLE:
            if character == hash_tables.OPERATOR_HASH_TABLE.get(operator_key):
                operator = operator_key
                if i+1 < len(line) and operator in hash_tables.DOUBLE_CHAR_OPERATORS_FIRST:
                    double_operator_key = (operator, line[i+1])
                    if double_operator_key in hash_tables.DOUBLE_CHAR_OPERATORS_SECOND:
                        operator = hash_tables.DOUBLE_CHAR_OPERATORS_SECOND[double_operator_key]
                        is_dbl_operator = True
                break

        if (is_char):
            word = character
            while i+1 < len(line) and re.search(constants.REGEX_CHAR, line[i+1]):
                word += line[i+1]
                i += 1

            # check if program defined or reserved
            keyword = None
            for keyword_key in hash_tables.KEYWORD_HASH_TABLE:
                if word == hash_tables.KEYWORD_HASH_TABLE.get(keyword_key):
                    keyword = keyword_key
                    break

            if keyword:
                tokens.append(keyword)
            else:
                # check identifier
                identifier = word
                is_trunc = False
                if len(identifier) > constants.IDENTIFIER_MAX:
                    identifier = word[:constants.IDENTIFIER_MAX]
                    error_stack.append(
                        f'{constants.WARNING} Identifier {word} exceeded {constants.IDENTIFIER_MAX}. Truncated to {identifier}')
                    is_trunc = True

                (identifier_hashed, exists) = hash_identifier(
                    identifier, lambda err: error_stack.append(err))

                if is_trunc and exists:
                    error_stack.append(
                        f'{constants.WARNING} The truncated identifier {identifier} may reference an unstripped version'
                    )

                tokens.append(f'0 {identifier_hashed}')

        elif (is_num):
            integer = character
            while i+1 < len(line) and re.search(constants.REGEX_NUM, line[i+1]):
                integer += line[i+1]
                i += 1

            fractional = ''
            if i+1 < len(line) and line[i+1] == constants.DECIMAL:
                fractional += line[i+1]
                i += 1
                while i+1 < len(line) and re.search(constants.REGEX_NUM, line[i+1]):
                    fractional += line[i+1]
                    i += 1

            exponent = ''
            if i+1 < len(line) and line[i+1] == constants.EXPONENT:
                exponent += line[i+1]
                i += 1
                while i+1 < len(line) and re.search(constants.REGEX_NUM, line[i+1]):
                    exponent += line[i+1]
                    i += 1

            invalid_identifier = ''
            while i+1 < len(line) and re.search(constants.REGEX_CHAR, line[i+1]):
                invalid_identifier += line[i+1]
                i += 1

            numeral = integer + fractional + exponent + invalid_identifier

            if len(invalid_identifier) > 0:
                error_stack.append(
                    f'{constants.WARNING} {numeral} is an invalid identifier')
                tokens.append(constants.INVALID_TOKEN)
            else:
                if len(numeral) > constants.NUMERAL_MAX:
                    error_stack.append(
                        f'{constants.WARNING} {numeral} exceeded {constants.NUMERAL_MAX} characters')

                tokens.append(f'1 {numeral}')

        elif operator:
            tokens.append(operator)

        elif operator == None and not is_char and not is_num and not is_blank:
            tokens.append(constants.INVALID_TOKEN)

        i += 1
        if is_dbl_operator:
            i += 1

    tokens.append(constants.EOL)

    return (tokens, error_stack)


def hash_identifier(identifier, error_stack_append):
    '''
    takes a string
    returns a hashed index, and whether it exists
    '''

    total = 0
    for character in identifier:
        total += ord(character)
    index = total % 449
    if hash_tables.IDENTIFIER_HASH_TABLE[index] == None or hash_tables.IDENTIFIER_HASH_TABLE[index] == identifier:
        exists = index in hash_tables.IDENTIFIER_HASH_TABLE
        hash_tables.IDENTIFIER_HASH_TABLE[index] = identifier
        return (index, exists)

    # resolve collisions
    j = 450
    found = False
    exists = False
    while j < 500 and not found:
        if hash_tables.IDENTIFIER_HASH_TABLE[j] == None or hash_tables.IDENTIFIER_HASH_TABLE[index] == identifier:
            exists = index in hash_tables.IDENTIFIER_HASH_TABLE
            found = True
        else:
            j += 1
    if found:
        hash_tables.IDENTIFIER_HASH_TABLE[j] = identifier
        return (j,  exists)

    error_stack_append(f'{constants.WARNING} Hash table overflow full')
    return (None,  False)
