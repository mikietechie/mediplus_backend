def dict_fetch_all(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]

def clean_filters(filters: dict) -> dict:
    cleaned_filters = {}
    for (key, value) in filters.items():
        try:
            cleaned_filters[f'{key}'] = eval(value)
        except:
            cleaned_filters[f'{key}'] = value
    return cleaned_filters

def get_and_pop_from_dict(dictionary: dict, key: str):
    return dictionary.pop(key) if dictionary.get(key) else None

def get_attr_or_none(obj, attr_name, is_func=None, **kwargs):
    try:
        if not is_func:
            return getattr(obj, attr_name)
        kwargs.pop("is_func")
        attr = getattr(obj, attr_name)
        return attr(**kwargs)
    except:
        return None