import json
import traceback
from datetime import datetime

from .field_map import FIELD_MAPPING
from .helper import get_value

from utils.normalizors import (
    normalize_name,
    normalize_email,
    normalize_phone,
    normalize_null,
    normalize_company,
)


class ATSAdapter:

    def build_profile(self, json_path):

        with open(json_path, "r", encoding="utf-8") as file:
            ats_candidates = json.load(file)

        profiles = []

        for ats in ats_candidates:
            profile = {}

            profile["candidate_id"] = get_value(
                ats,
                FIELD_MAPPING["candidate_id"]
            )

            profile["full_name"] = normalize_name(
                get_value(
                    ats,
                    FIELD_MAPPING["full_name"]
                )
            )

            emails = get_value(
                ats,
                FIELD_MAPPING["emails"]
            ) or []

            profile["emails"] = []

            for email in emails:
                profile["emails"].extend(
                    normalize_email(email)
                )

            phones = get_value(
                ats,
                FIELD_MAPPING["phones"]
            ) or []

            profile["phones"] = []

            for phone in phones:
                profile["phones"].extend(
                    normalize_phone(phone)
                )
            

            profile["headline"] = normalize_null(
                get_value(
                    ats,
                    FIELD_MAPPING["headline"]
                )
            )

            skills = get_value(
                ats,
                FIELD_MAPPING["skills"]
            ) or []

            profile["skills"] = sorted(
                {
                    normalize_null(skill).title()
                    for skill in skills
                    if normalize_null(skill)
                }
            )

            experience = get_value(
                ats,
                FIELD_MAPPING["experience"]
            ) or []

            normalized_experience = []

            for exp in experience:

                normalized_experience.append({
                    "company": normalize_company(
                        exp.get("company")
                    ),
                    "title": normalize_null(
                        exp.get("title")
                    ),
                    "start_date": normalize_null(
                        exp.get("start_date")
                    ),
                    "end_date": normalize_null(
                        exp.get("end_date")
                    )
                })

            profile["experience"] = normalized_experience

            education = get_value(
                ats,
                FIELD_MAPPING["education"]
            ) or []

            normalized_education = []

            for edu in education:
                end_year = edu.get("end_year")
                if isinstance(end_year, str) and end_year.isdigit():
                    end_year = int(end_year)
                elif end_year == 0:
                    end_year = None
                    
                normalized_education.append({
                    "institution": normalize_null(
                        edu.get("institution")
                    ),
                    "degree": normalize_null(
                        edu.get("degree")
                    ),
                    "field_of_study": normalize_null(
                        edu.get("field_of_study")
                    ),
                    "end_year": end_year
                })

            profile["education"] = normalized_education

            profile["years_experience"] = (
                self.calculate_years_experience(
                    profile["experience"]
                )
            )

            profiles.append(profile)

        return profiles

    def parse_date(self, date_str):
        if not date_str:
            return None

        formats = [
            "%Y-%m",
            "%Y/%m",
            "%Y-%m-%d",
            "%Y/%m/%d"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return None
    
    def calculate_years_experience(self, experiences):

        if not experiences:
            return None

        start_dates = []
        end_dates = []

        for exp in experiences:

            start = self.parse_date(exp.get("start_date"))
            end = self.parse_date(exp.get("end_date"))

            if start:
                start_dates.append(start)

            if end:
                end_dates.append(end)
            else:
                end_dates.append(datetime.today())

        if not start_dates:
            return None

        earliest = min(start_dates)
        latest = max(end_dates)

        years = (latest - earliest).days / 365.25

        return round(years, 1)


def empty_ats_profile():

    return {
        "candidate_id": None,
        "full_name": None,
        "emails": [],
        "phones": [],
        "headline": None,
        "skills": [],
        "experience": [],
        "education": [],
        "years_experience": None
    }


def ats_extractor(json_path):
    if not json_path:
        return []

    try:
        adapter = ATSAdapter()
        return adapter.build_profile(json_path)

    except Exception:
        traceback.print_exc()
        return []