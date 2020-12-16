from threading import Lock


class SingletonMeta(type):
    """Thread-safe implementation of Singleton."""
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """Possible changes to the value of the `__init__` argument do not
        affect the returned instance."""
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


def only_value_from_dict(lst):
    return [dct['value'] for dct in lst]