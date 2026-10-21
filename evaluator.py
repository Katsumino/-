import math


class Evaluator:
    FUNCTIONS = {
        "log10": math.log10,
    }

    def eval(self, node):
        kind = node[0]

        if kind == "num":
            return node[1]

        if kind == "unop":
            _, op, operand = node
            val = self.eval(operand)
            return val if op == "PLUS" else -val

        if kind == "binop":
            _, op, left, right = node
            a = self.eval(left)
            b = self.eval(right)
            if op == "PLUS":
                return a + b
            if op == "MINUS":
                return a - b
            if op == "MUL":
                return a * b
            if op == "DIV":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                return a / b
            if op == "LT":
                return 1.0 if a < b else 0.0
            if op == "GT":
                return 1.0 if a > b else 0.0
            if op == "LE":
                return 1.0 if a <= b else 0.0
            if op == "GE":
                return 1.0 if a >= b else 0.0
            if op == "EQ":
                return 1.0 if a == b else 0.0
            if op == "NE":
                return 0.0 if a == b else 1.0

        if kind == "call":
            _, name, arg_nodes = node
            if name not in self.FUNCTIONS:
                raise NameError(f"Неизвестная функция: {name}")
            args = [self.eval(a) for a in arg_nodes]
            try:
                return self.FUNCTIONS[name](*args)
            except ValueError:
                raise ValueError(
                    f"Функция {name} не может быть вычислена для аргументов {args}"
                )

        raise RuntimeError(f"Неизвестный узел: {node}")