from tools37.colors import *
from tools37.logger import Log


def main():
    from random import randint
    from tools37.colors import RED, GREEN, YELLOW

    console = Log.Console(styles={
        'session': None,
        'success': Log.Console.Style(bg=BLACK, fg=GREEN),
        'error': Log.Console.Style(bg=BLACK, fg=RED),
        'warning': Log.Console.Style(bg=BLACK, fg=YELLOW),
    })

    log = Log.load('test_log', True, True, console)

    session_start = log.new('session', 'calculating some divisions')

    for _ in range(randint(100, 200)):
        x = randint(-10, 10)
        y = randint(-10, 10)

        try:
            r = x / (x - y)
            log.new('success', f"{x!r} / ({x!r} - {y!r}) = {r!r}")

            # if y * r - x != 0:
            #     log.new('warning', f"({x!r} / {y!r}) * {y!r} != {x!r}")

        except Exception as error:
            log.new('error', f"{x!r} / ({x!r} - {y!r}) -> {error}")

    print()
    print('all log sessions')
    for entry in log.findall(code='session'):
        console.print(entry)

    session_successes = list(log.findall(code='success', after=session_start.at))
    session_errors = list(log.findall(code='error', after=session_start.at))
    session_warnings = list(log.findall(code='warning', after=session_start.at))
    n_successes = len(session_successes)
    n_errors = len(session_errors)
    n_attempts = n_errors + n_successes

    print()
    print('current session errors')
    for entry in session_errors:
        console.print(entry)

    print()
    print('current session warnings')
    for entry in session_warnings:
        console.print(entry)

    print()
    print('current session infos')
    print(f'number of attempts = {n_attempts}')
    print(f'number of errors = {n_errors}')
    print(f'number of successes = {n_successes}')
    print(f'error percent = {int((100 * n_successes) / n_attempts)}%')


if __name__ == '__main__':
    main()
