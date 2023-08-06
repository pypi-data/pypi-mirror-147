from functools import wraps

from swagger_coverage.coverage import SwaggerCoverage


def swagger(key):
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            res = function(*args, **kwargs)
            try:
                SwaggerCoverage().swagger_check(key, res)
                return res
            except AttributeError:
                return res

        return inner

    return wrapper
