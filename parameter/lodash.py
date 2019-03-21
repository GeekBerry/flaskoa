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
    def __new__(cls, data=Undefined(), **kwargs):
        if isinstance(data, dict) or data is Undefined():
            return super().__new__(cls)
        elif isinstance(data, (tuple, list)):
            return Object({str(index): each for index, each in enumerate(data)})
        elif isinstance(data, set):
            return Object({str(each): each for each in data})
        else:
            return data

    def __init__(self, data=None, **kwargs):
        super().__init__()

        if isinstance(data, dict):
            for key, value in data.items():
                self[key] = value

        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f'key must be str, get {key}')

        if value is Undefined():
            return

        obj = self
        names = key.split('.')
        for index, name in enumerate(names):
            if index == len(names) - 1:
                dict.__setitem__(obj, name, Object(value))
            else:
                obj = dict.setdefault(obj, name, Object())

    def __getattribute__(self, item):
        return self[item]

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(f'key must be str, get {key}')

        obj = self
        for name in key.split('.'):
            obj = dict.get(obj, name, Undefined())
        return obj
