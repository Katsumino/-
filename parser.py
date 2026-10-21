from lexer import Token


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def consume(self, expected=None):
        tok = self.tokens[self.pos]
        if expected and tok.type != expected:
            raise SyntaxError(f"Ожидался {expected}, получен {tok.type}")
        self.pos += 1
        return tok

    def parse(self):
        node = self.expression()
        if self.peek().type != "EOF":
            raise SyntaxError(f"Лишние символы после выражения: {self.peek()}")
        return node

    def expression(self):
        return self.comparison()

    def comparison(self):
        node = self.additive()
        while self.peek().type in ("LT", "GT", "LE", "GE", "EQ", "NE"):
            op = self.consume().type
            right = self.additive()
            node = ("binop", op, node, right)
        return node

    def additive(self):
        node = self.multiplicative()
        while self.peek().type in ("PLUS", "MINUS"):
            op = self.consume().type
            right = self.multiplicative()
            node = ("binop", op, node, right)
        return node

    def multiplicative(self):
        node = self.unary()
        while self.peek().type in ("MUL", "DIV"):
            op = self.consume().type
            right = self.unary()
            node = ("binop", op, node, right)
        return node

    def unary(self):
        if self.peek().type in ("PLUS", "MINUS"):
            op = self.consume().type
            operand = self.unary()
            return ("unop", op, operand)
        return self.primary()

    def primary(self):
        tok = self.peek()

        if tok.type == "NUMBER":
            self.consume()
            return ("num", tok.value)

        if tok.type == "LPAREN":
            self.consume("LPAREN")
            node = self.expression()
            self.consume("RPAREN")
            return node

        if tok.type == "IDENT":
            name = self.consume().value
            self.consume("LPAREN")
            args = []
            if self.peek().type != "RPAREN":
                args.append(self.expression())
                while self.peek().type == "COMMA":
                    self.consume("COMMA")
                    args.append(self.expression())
            self.consume("RPAREN")
            return ("call", name, args)

        raise SyntaxError(f"Неожиданный токен: {tok}")