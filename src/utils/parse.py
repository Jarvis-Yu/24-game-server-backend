__all__ = ["parse_int"]


def parse_int(number: str) -> int | None:
    try:
        return int(number)
    except ValueError:
        return None