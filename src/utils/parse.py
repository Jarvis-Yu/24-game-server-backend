__all__ = ["parse_int"]


def parse_int(number_str: str | int) -> int | None:
    try:
        return int(number_str)
    except ValueError:
        return None

def parse_bool(bool_str: str | bool) -> bool | None:
    if isinstance(bool_str, bool):
        return bool_str
    if bool_str.lower() == "true":
        return True
    if bool_str.lower() == "false":
        return False
    return None

def parse_to_bool_dict(data: dict[str, str | bool], default_val: bool = False) -> dict[str, bool]:
    return {
        key: b if (b := parse_bool(value)) is not None else default_val
        for key, value in data.items()
    }
