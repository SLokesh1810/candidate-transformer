from utils.normalizors import normalize_phone


class NormalizationError(Exception):
    pass


def canonical(value):
    """
    Generic normalization.

    - Removes duplicates
    - Trims whitespace
    - Keeps original order
    """

    if value is None:
        return None

    if isinstance(value, list):
        seen = set()
        result = []

        for item in value:

            if item is None:
                continue

            item = str(item).strip()

            key = item.lower()

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result

    return str(value).strip()


def normalize(value, method):
    """
    Dispatch normalization based on config.
    """

    if value is None:
        return None

    if method is None:
        return value

    method = method.lower()

    if method == "canonical":
        return canonical(value)

    if method == "e164":

        if isinstance(value, list):
            return [
                normalize_phone(v)[0]
                for v in value
                if normalize_phone(v)
            ]

        phones = normalize_phone(value)

        if phones:
            return phones[0]

        return None

    raise NormalizationError(
        f"Unknown normalization method: {method}"
    )