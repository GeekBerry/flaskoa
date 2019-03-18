class Undefined:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __bool__(self):
        return False

    def __getattr__(self, item):
        return self.instance

    def __setattr__(self, key, value):
        raise TypeError('Can not set attr to <undefined>')

    def __repr__(self):
        return '<undefined>'

    def __str__(self):
        return self.__repr__()


class Object(dict):
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, item):
        return self.get(item, Undefined())

    def __setattr__(self, key, value):
        if value is not Undefined():
            self[key] = value


def get(data: Object, path: str, default: object = Undefined()) -> any:
    ret = data

    for name in path.split('.'):
        ret = getattr(ret, name, Undefined())

        if ret is Undefined():
            if default is Undefined():
                raise KeyError(path)
            else:
                return default

    return ret


def set(data: Object, path: str, value: any):
    part = data

    names = path.split('.')
    for i in range(len(names)):
        if i != len(names) - 1:
            next = getattr(part, names[i], Undefined())
            if next is Undefined():
                next = Object()
                setattr(part, names[i], next)
            part = next
        else:
            setattr(part, names[i], value)