"""
Flask参数简介
:see https://blog.csdn.net/weixin_41829272/article/details/80498329
"""

from flask import Flask, Blueprint, jsonify, request, current_app

__all__ = ['App', 'Router']


class Error(Exception):
    def __init__(self, body: any, code: int = 500):
        self.__body = body
        self.__code = code

    @property
    def body(self) -> any:
        return self.__body

    @property
    def code(self) -> int:
        return self.__code


class Method:
    """
    Http 方法
    """

    @staticmethod
    def dump(ret):
        if ret is None:
            return b'', 204

        if isinstance(ret, (tuple, set)):  # 返回 tuple 不再视为指定 status code
            ret = list(ret)
        if isinstance(ret, (bool, int, float, dict, list)):
            return jsonify(ret), 200

        return ret

    def __init__(self, cls_func: callable, rule: str, methods, **options: dict):
        self.router = None
        self.function = cls_func
        self.rule = rule
        self.methods = methods
        self.options = options

    def bind(self, router: 'RouterInterface', *, url_prefix: str = ''):
        self.router = router
        router.route(f'{url_prefix}{self.rule}', methods=self.methods, **self.options)(self)

    def __call__(self, **params):
        ctx = {
            **params,
            'request': request,
            'method': request.method,
            'query': request.args.to_dict(),
            'header': dict(request.headers),
            'body': request.json or request.data,
            'cookies': request.cookies,
            'files': request.files,
        }

        try:
            ret = self.function(self.router, **ctx)
            return self.dump(ret)
        except Exception as e:
            if isinstance(e, Error):
                return e.body, e.code
            else:
                return 'Internal Error', 500


class RouterInterface:
    """
    路由接口
    """
    Error = Error  # short cut for Router.Error or App.Error
    METHODS = ('GET', 'HEAD', 'POST', 'PATCH', 'PUT', 'DELETE', 'OPTIONS')

    # 为了逻辑更清晰以及IDE友好, 将所有 METHODS 显示实现
    @classmethod
    def all(cls, rule, methods=METHODS, **options) -> callable:
        def decorator(cls_func):
            class R(Method):
                __name__ = cls_func.__name__

            return R(cls_func, rule, methods, **options)

        return decorator

    @classmethod
    def get(cls, rule, **options):
        return cls.all(rule, methods=('GET',), **options)

    @classmethod
    def head(cls, rule, **options):
        return cls.all(rule, methods=('HEAD',), **options)

    @classmethod
    def post(cls, rule, **options):
        return cls.all(rule, methods=('POST',), **options)

    @classmethod
    def patch(cls, rule, **options):
        return cls.all(rule, methods=('PATCH',), **options)

    @classmethod
    def put(cls, rule, **options):
        return cls.all(rule, methods=('PUT',), **options)

    @classmethod
    def delete(cls, rule, **options):
        return cls.all(rule, methods=('DELETE',), **options)

    @classmethod
    def options(cls, rule, **options):
        return cls.all(rule, methods=('OPTIONS',), **options)

    def __init__(self):
        for method in self.__class__.__dict__.values():
            if isinstance(method, Method):
                method.bind(self)

    @NotImplementedError
    def route(self, rule: str, methods: list, **kwargs):
        pass  # 注册一个路由

    @property
    def logger(self):
        return current_app.logger


class Router(Blueprint, RouterInterface):
    def __init__(self, name=None, import_name=__name__, **kwargs):
        name = self.__class__.__name__ if name is None else name  # 默认为类名

        Blueprint.__init__(self, name, import_name, **kwargs)
        RouterInterface.__init__(self)

        self._sub_router_table = {}  # 子路由表 {str: Router, ...}

    def use(self, prefix: str, router: 'RouterInterface') -> 'Router':
        self._sub_router_table[prefix] = router
        return self


class App(Flask, RouterInterface):
    def __init__(self, name=__name__, **kwargs):
        Flask.__init__(self, name, **kwargs)
        RouterInterface.__init__(self)

    def use(self, prefix: str, router: [Method, Router]) -> 'App':
        if isinstance(router, Method):
            router.bind(self, url_prefix=prefix)
        elif isinstance(router, Router):  # 递归注册子路由
            for sub_prefix, sub_router in router._sub_router_table.items():
                self.use(f'{prefix}{sub_prefix}', sub_router)
            self.register_blueprint(router, url_prefix=prefix)
        else:
            raise TypeError

        return self
