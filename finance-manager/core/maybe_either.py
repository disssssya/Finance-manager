class Maybe:
    def __init__(self, value=None):
        self.value = value

    def is_nothing(self):
        return self.value is None

    def map(self, func):
        if self.is_nothing():
            return self
        try:
            return Maybe(func(self.value))
        except Exception:
            return Maybe(None)

    def bind(self, func):
        if self.is_nothing():
            return self
        try:
            return func(self.value)
        except Exception:
            return Maybe(None)

    def get_or_else(self, default):
        return self.value if not self.is_nothing() else default

    def __repr__(self):
        if self.is_nothing():
            return "Nothing"
        return f"Just({self.value})"


class Just(Maybe):
    def __init__(self, value):
        super().__init__(value)


class Nothing(Maybe):
    def __init__(self):
        super().__init__(None)


class Either:
    def map(self, func):
        if isinstance(self, Left):
            return self
        try:
            return Right(func(self.value))
        except Exception as e:
            return Left({"error": str(e)})

    def bind(self, func):
        if isinstance(self, Left):
            return self
        try:
            return func(self.value)
        except Exception as e:
            return Left({"error": str(e)})

    def get_or_else(self, default):
        if isinstance(self, Right):
            return self.value
        return default


class Left(Either):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Left({self.value})"


class Right(Either):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Right({self.value})"
