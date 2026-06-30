from models.canonical import (
    Skill,
    Provenance,
    Experience,
    Education
)

from .score_vars import (
    SKILL_CONFIDENCE,
    MAX_CONFIDENCE
)


def get_professional_info(sources):
    github = sources.get("github", {}) or {}
    ats = sources.get("ats", {}) or {}

    professional = {}
    provenance = []

    skill_map = {}

    for source_name, skills in [
        ("github", github.get("skills", [])),
        ("ats", ats.get("skills", [])),
    ]:
        for skill in skills:
            if not skill:
                continue

            key = skill.strip().lower()

            if key not in skill_map:
                skill_map[key] = {
                    "display": skill.strip(),
                    "sources": []
                }

            if source_name not in skill_map[key]["sources"]:
                skill_map[key]["sources"].append(source_name)

    professional["skills"] = []

    for key in sorted(skill_map.keys()):
        skill_name = skill_map[key]["display"]
        sources_used = skill_map[key]["sources"]
        confidence = (
            MAX_CONFIDENCE
            if len(sources_used) > 1
            else SKILL_CONFIDENCE
        )
        professional["skills"].append(
            Skill(
                name=skill_name,
                confidence=confidence,
                sources=sources_used
            )
        )

    if professional["skills"]:
        provenance.append(
            Provenance(
                field="skills",
                source="github, ats",
                method="merged"
            )
        )

    professional["experience"] = [
        Experience(**exp)
        for exp in ats.get("experience", [])
    ]
    if professional["experience"]:
        provenance.append(
            Provenance(
                field="experience",
                source="ats",
                method="normalized"
            )
        )

    professional["education"] = [
        Education(**edu)
        for edu in ats.get("education", [])
    ]

    if professional["education"]:
        provenance.append(
            Provenance(
                field="education",
                source="ats",
                method="normalized"
            )
        )

    professional["years_experience"] = ats.get(
        "years_experience"
    )

    if professional["years_experience"] is not None:
        provenance.append(
            Provenance(
                field="years_experience",
                source="ats",
                method="calculated"
            )
        )

    return professional, provenance