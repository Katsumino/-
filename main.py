from lexer import Lexer
from parser import Parser
from evaluator import Evaluator


def calculate(text):
    tokens = Lexer(text).tokenize()
    ast = Parser(tokens).parse()
    return Evaluator().eval(ast)


def main():
    print("Интерпретатор арифметических выражений")
    print("Поддерживается: + - * / ( ) , числа, log10(x), != и другие сравнения")
    print("Для выхода введите 'exit'")
    print()

    while True:
        text = input("Введите выражение: ").strip()

        if text.lower() == "exit":
            print("Выход.")
            break

        try:
            result = calculate(text)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            print(f"Результат: {result}")
        except (ValueError, ZeroDivisionError, NameError) as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

        print()


if __name__ == "__main__":
    main()
