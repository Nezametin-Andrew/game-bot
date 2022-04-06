

class BaseHandler:
    """
    The BaseHandler class provides a minimal class which may be used
    for writing custom handler implementations.

    In particular, if a `method=` argument is passed then:

    .process() - Available.

    Dictionary `.methods` must be contain callback methods
    where argument `method=` is the key  and value  instance.method.

    {'method': instance.callback}
    """

    def __init__(self, *args, **kwargs):
        self.method = None
        self.methods = {}

        for key, value in kwargs.items():
            setattr(self, key, value)

    def returns_error(self, msg: str, logger, data: str = None) -> object:
        logger.debug(str(msg) + data if data is not None else '')
        self.data = {'error': str(msg)}
        return self

    def process(self):
        if not self.methods:
            raise CannotBeEmptyException('Attribute "methods" cannot be empty')

        if self.method not in self.methods:
            raise MethodNotAllowedException("Method not allowed")
        return self.methods[self.method]()


class CannotBeEmptyException(Exception):
    ...


class MethodNotAllowedException(Exception):
    ...
