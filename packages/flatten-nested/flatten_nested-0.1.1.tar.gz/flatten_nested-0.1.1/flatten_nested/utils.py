def is_iterable(obj):
    """Check if an object is iterable but not a string."""
    try:
        iter(obj)
        return not isinstance(obj, (str, bytes))
    except TypeError:
        return False

def get_iterator(obj):
    """Get the appropriate iterator for different types."""
    if isinstance(obj, dict):
        return obj.items()
    elif isinstance(obj, set):
        return iter(obj)
    return obj