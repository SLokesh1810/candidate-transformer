import re


def resolve_path(data, path):
    parts = path.split(".")
    return _resolve(data, parts)


def _resolve(value, parts):

    if value is None:
        return None

    if not parts:
        return value

    part = parts[0]
    remaining = parts[1:]

    if part.endswith("[]"):
        key = part[:-2]

        if not isinstance(value, dict):
            return []

        items = value.get(key, [])

        if not isinstance(items, list):
            return []

        return [
            _resolve(item, remaining)
            for item in items
        ]

    match = re.match(r"(\w+)\[(\d+)\]", part)

    if match:
        key = match.group(1)
        index = int(match.group(2))

        if not isinstance(value, dict):
            return None

        items = value.get(key, [])

        if (
            not isinstance(items, list)
            or index >= len(items)
        ):
            return None

        return _resolve(
            items[index],
            remaining
        )

    if not isinstance(value, dict):
        return None

    return _resolve(
        value.get(part),
        remaining
    )