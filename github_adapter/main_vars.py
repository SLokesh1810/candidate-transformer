import re

LANGUAGE_MAP = {
    "Dockerfile": "Docker",
    "Jupyter Notebook": "Python",
    "HTML": "HTML",
    "CSS": "CSS",
    "SCSS": "CSS",
    "TypeScript": "TypeScript",
    "JavaScript": "JavaScript",
    "Python": "Python",
    "C++": "C++",
    "C": "C",
    "Java": "Java",
    "Go": "Go",
    "Shell": "Shell",
    "PowerShell": "PowerShell",
    "Batchfile": "Windows Batch",
    "Makefile": "Make",
    "YAML": "YAML",
    "Markdown": "Markdown"
}

BASE_URL = "https://api.github.com"

URL_REGEX = re.compile(r"https?://[^\s)\]]+")