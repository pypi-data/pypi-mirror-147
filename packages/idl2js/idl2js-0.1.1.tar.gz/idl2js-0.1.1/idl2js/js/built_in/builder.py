import string
from random import randint, choice

from .primitive_types import INT_RANGES, UNSIGNED_LONG_LONG, LONG_LONG
from .jtypes import LongLong, UnsignedLongLong, USVString, DOMString


def generate_int(int_type):
    return randint(*INT_RANGES[int_type])


def generate_string():
    return ''.join(
        choice(string.ascii_lowercase)
        for _ in range(randint(1, 10))
    )


class STDBuilder:
    def build(self, type_):
        match type_:
            case LongLong():
                return generate_int(LONG_LONG)
            case UnsignedLongLong():
                return generate_int(UNSIGNED_LONG_LONG)
            case DOMString():
                return generate_string()
            case USVString():
                return generate_string()
            case _:
                raise TypeError('Unsupported')
