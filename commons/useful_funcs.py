def replace_dict_none_values_to_empty_string(d):
    if not isinstance(d, dict):
        return None
    return {k: '' if v is None else v for k, v in d.items()}

