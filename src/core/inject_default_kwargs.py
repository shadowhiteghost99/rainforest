def inject_default_kwarg(name, default):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            kwargs[name] = kwargs.get(name, default)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
