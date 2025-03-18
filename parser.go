/*
Source:
https://medium.com/@bradford_hamilton/building-a-json-parser-and-query-tool-with-go-8790beee239a
*/
//
// Lexical analysis is sometimes referred to as scanning or tokenization
//
package main

import "fmt"

//
// `Type` is an alias for `string`
//
type Type string

//
// The token's literal holds the actual value of the token
// The token's line field is for better error reporting
// The start and end fields represent indices within the JSON where the token lives
//
type Token struct {
	Type Type
	Literal string
	Line int
	Start int
	End int
}

const (
	Illegal Type = "ILLEGAL"

	EOF Type = "EOF"

	String Type = "STRING"
	Number Type = "NUMBER"

	LeftBrace Type = "{"
	RightBrace Type = "}"
	LeftBracket Type = "["
RightBracket Type = "]"
	Comma Type = ","
	Colon Type = ":"

	True Type = "TRUE"
	False Type = "FALSE"
	Null Type = "NULL"
)

//
// Lexer Implementation
//
type Lexer struct {
	Input []rune
	char rune // current char under examination
	position int // current positinon in input (points to current char)
	readPosition int // current reading position in input (after current char)
	line int // line number for better error reporting, etc
}

//
// Create a lexer
//
func New(input string) *Lexer {
	l := &Lexer{Input: []rune(input)}
	l.readChar()
	return l
}

func (l *Lexer) readChar() {
	if l.readPosition >= len(l.Input) {
		// End of input (haven't read anything yet or EOF)
		// 0 is ASCII code for "NUL" character
		l.char = 0
	} else {
		l.char = l.Input[l.readPosition]
	}

	l.position = l.readPosition
	l.readPosition++
}

var validJSONIdentifiers = map[string]Type {
	"true": True,
	"false": False,
	"null": Null,
}

func LookupIdentifier(identifier string) (Type, error) {
	if token, ok := validJSONIdentifiers[identifier]; ok {
		return token, nil
	}
	return "", fmt.Errorf("Expected a valid JSON identifier. Found: %s", identifier)
}

//
// NextToken switches through the lexer's current char and creates a new token
// It then calls readChar() to advance the lexer and it returns the token
//
func (l *Lexer) NextToken() Token {
	var t Token

	l.skipWhitespace()

	switch l.char {
	case '{':
		t = newToken(LeftBrace, l.line, l.position, l.position+1, l.char)
	case '}':
		t = newToken(RightBrace, l.line, l.position, l.position+1, l.char)
	case '[':
		t = newToken(LeftBracket, l.line, l.position, l.position+1, l.char)
	case ']':
		t = newToken(RightBracket, l.line, l.position, l.position+1, l.char)
	case ':':
		t = newToken(Colon, l.line, l.position, l.position+1, l.char)
	case ',':
		t = newToken(Comma, l.line, l.position, l.position+1, l.char)
	case '"':
		t.Type = String
		t.Literal = l.readString()
		t.Line = l.line
		t.Start = l.position
		t.End = l.position + 1
	case 0:
		t.Literal = ""
		t.Type = EOF
		t.Line = l.line
	default:
		if isLetter(l.char) {
			t.Start = l.position
			ident := l.readIdentifier()
			t.Literal = ident
			t.Line = l.line
			t.End = l.position

			tokenType, err := LookupIdentifier(ident)
			if err != nil {
				t.Type = Illegal
				return t
			}
			t.Type = tokenType
			t.End = l.position
			return t
		} else if isNumber(l.char) {
			t.Start = l.position
			t.Literal = l.readNumber()
			t.Type = Number
			t.Line = l.line
			t.End = l.position
			return t
		}
		t = newToken(Illegal, l.line, 1, 2, l.char)
	}

	l.readChar()

	return t
}

func (l *Lexer) skipWhitespace() {
	for l.char == ' ' || l.char == '\t' || l.char == '\n' || l.char == '\r' {
		if l.char == '\n' {
			l.line++;
		}
		l.readChar()
	}
}

func newToken(tokenType Type, line, start, end int, char ...rune) Token {
	return Token {
		Type: tokenType,
		Literal: string(char),
		Line: line,
		Start: start,
		End: end,
	}
}

//
// readString sets a start position and reads through characters
// When it finds a closing `"`, it stops consuming characters and
// returns the string between the start and end positions.
//
func (l *Lexer) readString() string {
	position := l.position + 1
	for {
		prevChar := l.char
		l.readChar()
		if (l.char == '"' && prevChar != '\\') || l.char == 0 {
			break
		}
	}
	return string(l.Input[position:l.position])
}

//
// readNumber sets a start position and read through characters. When it
// finds a char that isn't a number, it stops consuming characters and
// returns the string between the start and end positions.
//
func (l *Lexer) readNumber() string {
	position := l.position

	for isNumber(l.char) {
		l.readChar()
	}
	
	return string(l.Input[position:l.position])
}

func isNumber(char rune) bool {
	return '0' <= char && char <= '9' || char == '.' || char == '-'
}

func isLetter(char rune) bool {
	return 'a' <= char && char <= 'z'
}

func (l *Lexer) readIdentifier() string {
	position := l.position

	for isLetter(l.char) {
		l.readChar()
	}
	
	return string(l.Input[position:l.position])
}

func main() {
	fmt.Println("Hello world")
}
