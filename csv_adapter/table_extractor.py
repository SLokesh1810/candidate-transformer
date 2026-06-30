import pandas as pd
from pathlib import Path
import pprint

from utils.normalizors import (
    safe_normalize,
    normalize_email,
    normalize_company,
    normalize_name,
    normalize_phone,
    normalize_title
)

def validate_candidate(candidate: dict) -> tuple[bool, list]:
    errors = []

    if not candidate.get("full_name"):
        errors.append("Missing candidate name.")

    if len(candidate.get("emails", [])) == 0:
        errors.append("No valid email found.")

    return len(errors) == 0, errors


def build_candidate(raw: dict) -> dict:
    candidate = {
        "candidate_id": raw.get('candidate_id'),
        "full_name": safe_normalize(normalize_name, raw.get("name"), None),
        "emails": safe_normalize(normalize_email, raw.get("email"), []),
        "phones": safe_normalize(normalize_phone, raw.get("phone"), []),
        "current_company": safe_normalize(normalize_company, raw.get("current_company"), None),
        "title": safe_normalize(normalize_title, raw.get("title"), None),
    }
    return candidate


def transform_candidate(raw: dict):
    candidate = build_candidate(raw)

    valid, errors = validate_candidate(candidate)

    return {
        "candidate": candidate,
        "is_valid": valid,
        "errors": errors
    }

if __name__ == "__main__":

    data = pd.read_csv(Path(rf"D:\Lokesh files\Projects\Eightfold_multisource_candidate_transformer\candidate-transformer\data\noisy_candidate_data.csv"))

    for _, row in data.iterrows():
        result = transform_candidate(row)
        pprint(result)