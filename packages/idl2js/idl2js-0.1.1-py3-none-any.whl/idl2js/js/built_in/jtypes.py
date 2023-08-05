class PrimitiveType:
    def __init__(self, builder):
        self._builder = builder

    def build(self):
        return self._builder.build(self)


class LongLong(PrimitiveType):
    pass


class DOMString(PrimitiveType):
    pass


class USVString(PrimitiveType):
    pass


class UnsignedLongLong(PrimitiveType):
    pass
