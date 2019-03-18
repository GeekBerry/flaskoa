from parameter.lodash import Undefined, Object, get


class Type:
    def __init__(self, path, *,
            default: object = Undefined(),
            enum=None,
            conditions: dict = None
    ):
        self.path = path
        self.default = default
        self.enum = enum
        self.conditions = conditions or {}

    def parse(self, data: str) -> any:
        return data

    def check(self, data) -> bool:
        return True

    def __call__(self, data):
        try:
            data = get(data, self.path, self.default)
        except KeyError:
            raise KeyError(f'"{self.path}" is required')

        try:
            data = self.parse(data)
        except Exception:
            raise TypeError(f'"{self.path}" parse to type="{self.__class__.__name__}" failed')

        if (self.enum is not None) and (data not in self.enum):
            raise AssertionError(f'"{self.path}" must in {list(self.enum)}')

        if not self.check(data):
            raise TypeError(f'"{self.path}" do not match type="{self.__class__.__name__}"')

        for name, func in self.conditions.items():
            if not func(data):
                raise TypeError(f'"{self.path}" do not match condition: "{name}"')

        return data


class Int(Type):
    def check(self, value):
        return isinstance(value, int)


class Obj(Type):
    def parse(self, data: dict):
        return Object(**data)
