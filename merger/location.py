from models.canonical import Location

from .merge_helper import merge_list, resolve_scalar


def get_location(sources):
    location = Location()

    value, _, provenance = resolve_scalar(
        "location",
        sources
    )

    if value:
        location.city = value

    return location, provenance