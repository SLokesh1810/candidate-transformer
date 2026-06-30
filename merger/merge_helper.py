from models.canonical import Provenance

from .similarity import similarity

SOURCE_PRIORITY = [
    "csv",
    "ats",
    "github"
]


def resolve_scalar(field_name, sources, method="normalized"):
    """
    Merge a scalar field (str/int/float).
    """

    selected_value = None
    provenance = []
    scores = []

    for source in SOURCE_PRIORITY:

        candidate = sources.get(source)

        if not candidate:
            continue

        value = candidate.get(field_name)

        if value:
            selected_value = value
            break

    if selected_value is None:
        return None, None, []

    for source in SOURCE_PRIORITY:

        candidate = sources.get(source)

        if not candidate:
            continue

        value = candidate.get(field_name)

        if not value:
            continue

        score = similarity(
            selected_value,
            value
        )

        if score is not None:
            scores.append(score)

        provenance.append(
            Provenance(
                field=field_name,
                source=source,
                method=method
            )
        )

    confidence = (
        round(sum(scores) / len(scores), 2)
        if scores
        else None
    )

    return (
        selected_value,
        confidence,
        provenance
    )


def merge_list(field_name, sources, method="normalized"):
    """
    Merge list fields like emails, phones.
    """

    merged = []
    provenance = []

    seen = set()

    for source in SOURCE_PRIORITY:

        candidate = sources.get(source)

        if not candidate:
            continue

        values = candidate.get(field_name, [])

        if not values:
            continue

        provenance.append(
            Provenance(
                field=field_name,
                source=source,
                method=method
            )
        )

        for value in values:

            if value not in seen:
                seen.add(value)
                merged.append(value)

    return merged, provenance