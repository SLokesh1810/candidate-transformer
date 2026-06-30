import os
import pandas as pd
import requests
from dotenv import load_dotenv

from .main_vars import BASE_URL, LANGUAGE_MAP

class GithubAdapter:
    def __init__(self, token=None):
        self.headers = {
            "Accept": "application/vnd.github+json"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def extract_username(self, github_url):
        if pd.isna(github_url):
            return None

        github_url = str(github_url).strip()

        if not github_url:
            return None

        return github_url.rstrip("/").split("/")[-1]

    def normalize_language(self, language: str):
        if not language:
            return None

        return LANGUAGE_MAP.get(language, language)

    def build_profile(self, github_url, candidate_id):
        username = self.extract_username(github_url)

        if not username:
            return empty_github_profile()

        profile = requests.get(
            f"{BASE_URL}/users/{username}",
            headers=self.headers
        )
        profile.raise_for_status()
        profile = profile.json()

        repos = requests.get(
            f"{BASE_URL}/users/{username}/repos?per_page=100&sort=updated",
            headers=self.headers
        )
        repos.raise_for_status()
        repos = repos.json()

        skills = set()
        portfolio_links = set()

        if profile.get("blog"):
            portfolio_links.add(profile["blog"])

        for repo in repos:
            if repo.get("fork"):
                continue
            if repo["name"].lower() == username.lower():
                continue

            language = self.normalize_language(
                repo.get("language")
            )

            if language:
                skills.add(language)

            if repo.get("homepage"):
                portfolio_links.add(repo["homepage"])

            repo_name = repo["name"].lower()

            if any(keyword in repo_name for keyword in (
                "portfolio",
                "website",
                "personal"
            )):
                portfolio_links.add(repo["html_url"])

        return {
            "candidate_id": candidate_id,
            "full_name": profile.get("name"),
            "bio": profile.get("bio"),
            "company": profile.get("company"),
            "location": profile.get("location"),
            "github_profile": profile.get("html_url"),
            "portfolio_links": sorted(portfolio_links),
            "skills": sorted(skills)
        }


def empty_github_profile():
    return {
        "candidate_id": None,
        "full_name": None,
        "bio": None,
        "company": None,
        "location": None,
        "github_profile": None,
        "portfolio_links": [],
        "skills": []
    }


def git_extractor(github_url, candidate_id):
    if not github_url:
        return empty_github_profile()

    try:
        load_dotenv()
        adapter = GithubAdapter(token=os.getenv("GITHUB_TOKEN"))
        return adapter.build_profile(github_url, candidate_id)

    except Exception as e:
        print(f"GitHub extraction failed: {e}")
        return empty_github_profile()