from typing import Union, List, Dict, Set, Tuple, Any, Optional
from collections.abc import Iterable

from .exceptions import UnsupportedTypeError
from .utils import is_iterable, get_iterator

def flatten(
    nested_item: Union[List, Dict, Set, Tuple],
    depth: Optional[int] = None,
    keep_dict_keys: bool = True,
    separator: str = "."
) -> List:
    """
    Flatten a nested data structure (list, tuple, dict, or set) into a 1D list.

    Args:
        nested_item: The nested data structure to flatten
        depth: Maximum depth to flatten. None means flatten completely
        keep_dict_keys: If True, include dictionary keys in the output
        separator: Separator to use when joining dictionary keys

    Returns:
        List containing flattened elements

    Raises:
        UnsupportedTypeError: If input type is not supported
    """
    if not is_iterable(nested_item):
        return [nested_item]

    def _flatten_recursive(item, current_depth=0, parent_key=""):
        if depth is not None and current_depth >= depth:
            return [item]

        if not is_iterable(item):
            return [item]

        flattened = []
        
        if isinstance(item, dict):
            for key, value in item.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                if is_iterable(value):
                    nested_values = _flatten_recursive(value, current_depth + 1, new_key if keep_dict_keys else "")
                    flattened.extend(nested_values)
                else:
                    if keep_dict_keys:
                        flattened.append((new_key, value))
                    else:
                        flattened.append(value)
        else:
            iterator = get_iterator(item)
            for value in iterator:
                flattened.extend(_flatten_recursive(value, current_depth + 1, parent_key))

        return flattened

    try:
        return _flatten_recursive(nested_item)
    except Exception as e:
        raise UnsupportedTypeError(f"Error flattening input: {str(e)}")