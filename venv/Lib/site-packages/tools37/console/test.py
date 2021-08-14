from tools37.console import Console
from tools37.colors import BLACK, GRAY, GREEN, RED, WHITE


def main():
    console = Console(5, 5, 40)

    INFO = Console.Style(bg=BLACK, fg=GRAY)
    TEXT = Console.Style(bg=BLACK, fg=WHITE)
    VALID = Console.Style(bg=BLACK, fg=GREEN)
    ERROR = Console.Style(bg=BLACK, fg=RED)

    console.display(['x', 'y', 'x / y'], [INFO, INFO, INFO])
    for x in range(10):
        for y in range(10):
            try:
                r = x / y
                console.display([x, y, r], [TEXT, TEXT, VALID])
            except ZeroDivisionError as error:
                console.display([x, y, error], [TEXT, ERROR, ERROR])


if __name__ == '__main__':
    main()
