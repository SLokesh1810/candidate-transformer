class CandidateMatcher:
    def __init__(self):
        self.matches = {}

    def _add_source(self, source_name, candidates):
        for candidate in candidates:
            candidate_id = candidate.get("candidate_id")

            if not candidate_id:
                continue

            if candidate_id not in self.matches:
                self.matches[candidate_id] = {
                    "csv": None,
                    "github": None,
                    "ats": None
                }

            self.matches[candidate_id][source_name] = candidate

    def match(
        self,
        csv_candidates,
        github_candidates,
        ats_candidates
    ):

        self.matches = {}

        self._add_source("csv", csv_candidates)
        self._add_source("github", github_candidates)
        self._add_source("ats", ats_candidates)

        return self.matches