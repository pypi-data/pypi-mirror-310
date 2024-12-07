class FlattenError(Exception):
    """Base exception for flatten_nested package"""
    pass

class UnsupportedTypeError(FlattenError):
    """Raised when an unsupported type is passed to flatten function"""
    pass