from urllib.parse import urlparse


def ensure_list(var):
    if isinstance(var, list):
        return var
    elif isinstance(var, str):
        return [x.strip() for x in var.split(',')]
    else:
        raise TypeError(f"Unsupported type: {type(var)}")


def is_url(string: str) -> bool:
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
