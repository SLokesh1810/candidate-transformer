from .merge_helper import merge_list, resolve_scalar


def get_personal_info(sources):
    personal = {}
    provenance = []

    full_name, _, prov = resolve_scalar(
        "full_name",
        sources
    )

    personal["full_name"] = full_name
    provenance.extend(prov)

    emails, prov = merge_list(
        "emails",
        sources
    )

    personal["emails"] = emails or []
    provenance.extend(prov)

    phones, prov = merge_list(
        "phones",
        sources
    )

    personal["phones"] = phones or []
    provenance.extend(prov)

    headline, _, prov = resolve_scalar(
        "headline",
        sources
    )

    personal["headline"] = headline
    provenance.extend(prov)

    return personal, provenance