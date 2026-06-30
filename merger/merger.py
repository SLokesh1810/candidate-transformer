from models.canonical import CanonicalCandidate

from .personals import get_personal_info
from .professional import get_professional_info
from .location import get_location
from .links import get_links


class CandidateMerger:

    def merge(self, sources):
        candidate = CanonicalCandidate()

        candidate.candidate_id = (
            (sources.get("csv") or {}).get("candidate_id")
            or (sources.get("github") or {}).get("candidate_id")
            or (sources.get("ats") or {}).get("candidate_id")
        )

        personal, provenance = get_personal_info(sources)

        for key, value in personal.items():
            setattr(candidate, key, value)

        candidate.provenance.extend(provenance)

        professional, provenance = get_professional_info(sources)

        candidate.skills.extend(
            professional.get("skills", [])
        )
        candidate.experience.extend(
            professional.get("experience", [])
        )
        candidate.education.extend(
            professional.get("education", [])
        )
        candidate.years_experience = (
            professional.get("years_experience")
        )
        candidate.provenance.extend(provenance)

        location, provenance = get_location(sources)
        candidate.location = location
        candidate.provenance.extend(provenance)

        links, provenance = get_links(sources)
        candidate.links = links
        candidate.provenance.extend(provenance)

        candidate.overall_confidence = (
            self.calculate_confidence(candidate)
        )
        return candidate

    def calculate_confidence(self, candidate):
        score = 0

        if candidate.full_name:
            score += 1.0

        if candidate.emails:
            score += 1.0

        if candidate.phones:
            score += 1.0

        if candidate.headline:
            score += 0.95

        if candidate.skills:
            score += 0.90

        if candidate.experience:
            score += 0.90

        if candidate.education:
            score += 0.90

        if candidate.links.github:
            score += 1.0

        if candidate.location.city:
            score += 0.80

        MAX_SCORE = 8.45

        return round(score / MAX_SCORE, 2)