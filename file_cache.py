import atexit
import shelve


def cached(file_name):
    """
    Decorator which makes function cached to a file
    All func arguments must be strings
    """

    cache = shelve.open(file_name)
    atexit.register(lambda: cache.close())

    def decorator(func):
        def new_func(*args):
            key = "|".join(args)
            try:
                v = cache[key]
            except KeyError:
                v = func(*args)
                cache[key] = v
            return v

        return new_func

    return decorator
