import itertools

from threading import Event


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break

        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')
