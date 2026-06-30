from models.canonical import (
    Links,
    Provenance
)


def get_links(sources):
    github = sources.get("github") or {}
    links = Links()
    provenance = []
    
    if github.get("github_profile"):
        links.github = github["github_profile"]
        provenance.append(
            Provenance(
                field="links",
                source="github",
                method="profile"
            )
        )

    portfolio_links = github.get(
        "portfolio_links",
        []
    )

    for link in portfolio_links:
        if "linkedin.com" in link.lower():
            links.linkedin = link
        elif (
            "github.com" not in link.lower()
            and links.portfolio is None
        ):
            links.portfolio = link
        else:
            links.other.append(link)

    if links.portfolio:
        provenance.append(
            Provenance(
                field="links",
                source="github",
                method="homepage"
            )
        )

    if links.linkedin:
        provenance.append(
            Provenance(
                field="links",
                source="github",
                method="homepage"
            )
        )

    return links, provenance