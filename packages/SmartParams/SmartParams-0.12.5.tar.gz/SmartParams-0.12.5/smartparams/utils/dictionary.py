from typing import Any, Dict, List, Tuple

import smartparams.utils.string as strutil


def flatten_keys(
    obj: Any,
    prefix: str = '',
) -> List[str]:
    if not isinstance(obj, dict):
        return [prefix]

    keys = []
    for k, v in obj.items():
        keys.extend(flatten_keys(v, strutil.join_keys(prefix, k)))

    return keys


def find_nested(
    dictionary: Dict[str, Any],
    name: str,
    set_mode: bool = False,
    required: bool = False,
) -> Tuple[Dict[str, Any], str]:
    *nested_keys, last_key = name.split(strutil.KEY_SEPARATOR)

    key_list = list()
    for key in nested_keys:
        key_list.append(key)
        if key not in dictionary:
            if set_mode:
                dictionary[key] = dict()
            else:
                location = strutil.KEY_SEPARATOR.join(key_list)
                raise KeyError(f"Param '{location}' is not in dictionary.")

        if not isinstance(dictionary[key], dict):
            if set_mode:
                dictionary[key] = dict()
            else:
                location = strutil.KEY_SEPARATOR.join(key_list)
                raise ValueError(f"Param '{location}' is not dictionary.")

        dictionary = dictionary[key]

    if required and last_key not in dictionary:
        key_list.append(last_key)
        location = strutil.KEY_SEPARATOR.join(key_list)
        raise KeyError(f"Param '{location}' is not in dictionary.")

    return dictionary, last_key


def check_key_is_in(
    key: str,
    dictionary: Dict[str, Any],
) -> bool:
    key, _, sub_key = key.partition(strutil.KEY_SEPARATOR)
    if key not in dictionary:
        return False

    if not sub_key:
        return True

    dictionary = dictionary[key]

    if not isinstance(dictionary, dict):
        return True

    return check_key_is_in(
        key=sub_key,
        dictionary=dictionary,
    )
