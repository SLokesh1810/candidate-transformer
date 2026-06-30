from .resolver import resolve_path
from .normalizers import normalize

class ProjectionError(Exception):
    pass


class Projector:

    def __init__(self, config):
        self.config = config

    def project(self, candidate):

        output = {}

        fields = self.config.get("fields", [])
        on_missing = self.config.get("on_missing", "null")

        for field in fields:

            destination = field["path"]

            source_path = field.get(
                "from",
                destination
            )

            required = field.get(
                "required",
                False
            )

            value = resolve_path(
                candidate,
                source_path
            )

            value = normalize(
                value,
                field.get("normalize")
            )

            missing = (
                value is None
                or value == []
                or value == {}
            )

            if missing:

                if required and on_missing == "error":
                    raise ProjectionError(
                        f"Missing required field: {destination}"
                    )

                if on_missing == "omit":
                    continue

                output[destination] = None
                continue

            output[destination] = value

        if self.config.get(
            "include_confidence",
            False
        ):
            output["overall_confidence"] = (
                candidate.get(
                    "overall_confidence"
                )
            )

        return output