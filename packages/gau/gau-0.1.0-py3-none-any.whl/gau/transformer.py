import json
from collections.abc import MutableMapping, MutableSequence
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


def flat(data, parent_key='', sep='.') -> dict:
    """
    Recursively flattens a nested dictionary or list into a single-level dictionary.

    Parameters:
        data (dict or list): The nested dictionary or list to be flattened.
        parent_key (str, optional): The key of the parent dictionary. Defaults to an empty string.
        sep (str, optional): The separator used to concatenate the keys. Defaults to '.'.

    Returns:
        dict: A single-level dictionary where the keys are the flattened keys from the nested dictionary or list, and the values are the corresponding values.

    Examples:
        >>> data = {'a': 1, 'b': {'c': 2, 'd': [3, 4]}}
        >>> flat(data)
        {'a': 1, 'b.c': 2, 'b.d.0': 3, 'b.d.1': 4}

        >>> data = [{'a': 1}, {'b': 2}]
        >>> flat(data)
        {'0.a': 1, '1.b': 2}
    """
    items = []
    if isinstance(data, MutableSequence):
        for i, value in enumerate(data):
            new_key = f'{parent_key}{sep}{i}' if parent_key else str(i)
            if isinstance(value, (MutableMapping, MutableSequence)):
                items.extend(flat(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
    elif isinstance(data, MutableMapping):
        for key, value in data.items():
            new_key = f'{parent_key}{sep}{key}' if parent_key else key
            if isinstance(value, (MutableMapping, MutableSequence)):
                items.extend(flat(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
    return dict(items)


class ExtendedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Decimal, UUID)):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class ExtendedJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        for key, value in obj.items():
            try:
                obj[key] = datetime.fromisoformat(value)
            except (TypeError, ValueError, AttributeError):
                pass
        return obj


def json_compact_dumps(params, sort_keys=True):
    """
    Serialize `params` to a compact JSON string.

    Args:
        params (Any): The data to be serialized.
        sort_keys (bool, optional): Whether to sort the keys in the resulting JSON string. Defaults to True.

    Returns:
        str: The compact JSON string representation of `params`.
    """
    return json.dumps(params, separators=(',', ':'), cls=ExtendedJsonEncoder, sort_keys=sort_keys)


def json_loads(json_str: str) -> dict:
    """
    Parse a JSON string and return the corresponding Python object.

    Args:
        json_str (str): The JSON string to be parsed.

    Returns:
        dict: The Python dictionary representing the parsed JSON object.
    """
    return json.loads(json_str, cls=ExtendedJsonDecoder)
