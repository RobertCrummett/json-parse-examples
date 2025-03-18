"""
Writing a simple JSON parser:

https://notes.eatonphil.com/writing-a-simple-json-parser.html
"""
#
# Two stages of parsing:
# 1. Lexical Analysis
# 2. Syntactic Analysis
#
# Lexical analysis breaks a source up into its simplest decomposable elements,
# which are often called "tokens"
#
# Syntactic analysis (often called parsing) recieves a list of tokens
# and tries to find patterns in them to meet the specifications of the
# language.
#

#
# Note: Because strings may contain whitespace, simply discarding
# whitespace is not safe in general. Discarding of whitespace must
# occur during the parsing.
#

"""
JSON Lexer
"""
JSON_COMMA = ','
JSON_COLON = ':'
JSON_LEFTBRACKET = '['
JSON_RIGHTBRACKET = ']'
JSON_LEFTBRACE = '{'
JSON_RIGHTBRACE = '}'

JSON_QUOTE = '"'
JSON_WHITESPACE = [' ', '\t', '\b', '\n', '\r']
JSON_SYNTAX = [JSON_COMMA, JSON_COLON, JSON_LEFTBRACKET, JSON_RIGHTBRACKET,
               JSON_LEFTBRACE, JSON_RIGHTBRACE]

FALSE_LEN = len('false')
TRUE_LEN = len('true')
NULL_LEN = len('null')

def lex_string(string):
    json_string = ""
    #
    # Check for a quote
    # If found, great, we have a string!
    # Otherwise, we do not have a string. Return None
    #
    if string[0] == JSON_QUOTE:
        string = string[1:]
    else:
        return None, string

    #
    # Parse the string until an end quote is found
    #
    for c in string:
        if c == JSON_QUOTE:
            return json_string, string[len(json_string)+1:]
        else:
            json_string += c
    
    #
    # If the end quote was not found, this is a syntax error
    # on the user side.
    #
    raise Exception("Expected end-of-string quote")

def lex_number(string):
    json_number = ""

    #
    # Valid JSON number characters
    #
    number_characters = [str(d) for d in range(10)] + ['-', 'e', '.']

    #
    # Essentially, iterate over the characters until an invalid
    # number character is found. At his point, we know that the
    # number is finished.
    #
    for c in string:
        if c in number_characters:
            json_number += c
        else:
            break

    rest = string[len(json_number):]

    if not len(json_number):
        return None, string

    if {'.', 'e'} in json_number:
        return float(json_number), rest

    return int(json_number), rest

def lex_bool(string):
    string_len = len(string)

    if string_len >= TRUE_LEN and string[:TRUE_LEN] == 'true':
        return True, string[TRUE_LEN:] 
    elif string_len >= FALSE_LEN and string[:FALSE_LEN] == 'false':
        return False, string[FALSE_LEN:]

    return None, string

def lex_null(string):
    string_len = len(string)

    if string_len >= NULL_LEN and string[:NULL_LEN] == 'null':
        return True, string[NULL_LEN:] 

    return None, string



def lex(string):
    tokens = []

    while len(string):
        json_string, string = lex_string(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_number, string = lex_number(string)
        if json_number is not None:
            tokens.append(json_number)
            continue

        json_bool, string = lex_bool(string)
        if json_bool is not None:
            tokens.append(json_bool)
            continue

        json_null, string = lex_null(string)
        if json_null is not None:
            tokens.append(json_null)
            continue

        if string[0] in JSON_WHITESPACE:
            string = string[1:]
        elif string[0] in JSON_SYNTAX:
            tokens.append(string[0])
            string = string[1:]
        else:
            raise Exception(f"Unexpected character: {string[0]}")
    
    return tokens

"""
JSON Parser
"""
def parse_array(tokens):
    json_array = []

    t = tokens[0]
    if t == JSON_RIGHTBRACKET:
        return json_array, tokens[1:]

    while True:
        json, tokens = parse(tokens)
        json_array.append(json)

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_array, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception("Ecpected comma after object in array")
        else:
            tokens = tokens[1:]

    raise Exception("Expected end-of-array bracket")

def parse_object(tokens):
    json_object = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception(f"Expected string key, got {json_key}")

        if tokens[0] != JSON_COLON:
            raise Exception(f"Expected colon after key in object, got {t}")

        json_value, tokens = parse(tokens[1:])

        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception(f"Expected comma after pair in object, got: {t}")

        tokens = tokens[1:]

    raise Exception("Expected end-of-object brace")

#
# While a lexer often returns a one-dimensional array of tokens, a
# parsers are defined recursively and return tree like data structures.
#
def parse(tokens):
    t = tokens[0]

    if t == JSON_LEFTBRACKET:
        return parse_array(tokens[1:])
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]

"""
The Interface
"""
def from_string(string):
    tokens = lex(string)
    return parse(tokens)[0]

"""
Testing
"""
if __name__ == "__main__":
    import pathlib
    
    jsonpath = pathlib.Path("share/example.json")
    with open(jsonpath) as jsonfile:
        jsondata = jsonfile.read()
    
    json = from_string(jsondata)
    print(json)
