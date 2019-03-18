from parameter.lodash import Object, set


class parameter:
    def __init__(self, schema: dict):
        self.schema = schema

    def __call__(self, func: callable):
        def _(**kwargs):
            kwargs = Object(**kwargs)
            data = Object()

            for field, Type in self.schema.items():
                try:
                    value = Type(data)  # 检查已验证过的参数
                except Exception:
                    value = Type(kwargs)  # 检查原始参数

                set(data, field, value)

            return func(**data)

        return _
