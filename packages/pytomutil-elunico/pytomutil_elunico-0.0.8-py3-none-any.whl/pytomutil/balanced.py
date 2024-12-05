class TooManyBracketsError(ValueError):
    ...


class NotEnoughBracketsError(ValueError):
    ...


class WrongBracketsError(ValueError):
    ...


import functools
from collections import namedtuple

Result = namedtuple("Result", ["exception", "result"])


def resultify(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return Result(None, fn(*args, **kwargs))
        except Exception as e:
            return Result(e, None)

    return wrapper


def balanced(s):
    tk = []
    bracs = {"(": ")", "{": "}", "[": "]"}
    for c in s:
        if c in bracs:
            tk.append(bracs[c])
        elif c in bracs.values():
            if not tk:
                raise TooManyBracketsError("No open bracket to match " + c)
            if not ((t := tk.pop()) == c):
                raise WrongBracketsError(f"Wrong close bracket: expected {t}; got {c}")
    if tk:
        raise TooManyBracketsError(f"Too many open brackets. Expected {tk[-1]}")


balanced("((()()(([[()(([]))]]))))")


@resultify
def is_balanced(b):
    return balanced(b)


print(is_balanced("((()()(([[()(([]))]]))))"))
print(is_balanced("((()()(([[()(([]))]])))))"))
print(is_balanced("((()()(([[()(([]))]])))"))
print(is_balanced("((()()(([[()(([]))]])))])"))
print(is_balanced("((()()(([[()]]))))"))
