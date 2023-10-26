def try_decorator(original_function):
    def wrapper_function(*args, **kwargs):
        try:
            return original_function(*args, **kwargs)
        except Exception as e:
            print(e)
            pass
    return wrapper_function