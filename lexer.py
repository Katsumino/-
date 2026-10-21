class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def skip_spaces(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def read_number(self):
        start = self.pos
        dots = 0
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            if self.text[self.pos] == '.':
                dots += 1
            self.pos += 1
        if dots > 1:
            raise SyntaxError(f"Некорректное число: {self.text[start:self.pos]}")
        return Token("NUMBER", float(self.text[start:self.pos]))

    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self.pos += 1
        return Token("IDENT", self.text[start:self.pos])

    def read_operator(self):
        two = {"<=": "LE", ">=": "GE", "==": "EQ", "!=": "NE"}
        for text, type_ in two.items():
            if self.text.startswith(text, self.pos):
                self.pos += 2
                return Token(type_)

        one = {
            "+": "PLUS", "-": "MINUS", "*": "MUL", "/": "DIV",
            "(": "LPAREN", ")": "RPAREN", ",": "COMMA",
            "<": "LT", ">": "GT",
        }
        ch = self.text[self.pos]
        if ch in one:
            self.pos += 1
            return Token(one[ch])
        raise SyntaxError(f"Неизвестный символ: {ch!r} на позиции {self.pos}")

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            self.skip_spaces()
            if self.pos >= len(self.text):
                break
            ch = self.text[self.pos]
            if ch.isdigit() or ch == '.':
                tokens.append(self.read_number())
            elif ch.isalpha() or ch == '_':
                tokens.append(self.read_identifier())
            else:
                tokens.append(self.read_operator())
        tokens.append(Token("EOF"))
        return tokens