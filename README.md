# Candidate Multi-Source Transformer

A configurable CLI tool that consolidates candidate information from multiple data sources into a single canonical profile.

The project demonstrates data integration, normalization, provenance tracking, configurable field projection, and confidence scoring.

---

# Features

- Merge candidate information from:
  - Candidate CSV
  - GitHub profile dataset
  - ATS JSON dataset
- Canonical candidate schema
- Provenance tracking for every merged field
- Confidence scoring
- Configurable output projection
- Command Line Interface (CLI)
- JSON output generation
- Modular architecture using adapters

---

# Project Structure

```
candidate-transformer/
│
├── ats_adapter/
├── csv_adapter/
├── github_adapter/
├── matcher/
├── merger/
├── models/
├── projector/
├── utils/
│
├── cli.py
├── main.py
├── requirements.txt
│
├── data/
│   ├── small_candidates.csv
│   ├── small_github_links.csv
│   ├── small_sample_ats_with_ids.json
│   └── output.json
│
└── projection.json
```

---

# Architecture

```
Candidate CSV
        │
        │
GitHub CSV
        │
        │
 ATS JSON
        │
        ▼
  Source Adapters
        │
        ▼
 Candidate Matcher
        │
        ▼
 Candidate Merger
        │
        ▼
 Canonical Candidate
        │
        ▼
 Projection Engine
        │
        ▼
 JSON Output
```

---

# Requirements

- Python 3.11+
- Git

---

# Installation

Clone the repository.

```bash
git clone https://github.com/SLokesh1810/candidate-transformer-eightfold

cd candidate-transformer
```

Create a virtual environment.

### Windows

```bash
python -m venv .venv
```

Activate it.

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

### Configure GitHub API Token

To enable GitHub profile enrichment, create a `.env` file in the project root and add your GitHub Personal Access Token:

```env
GITHUB_TOKEN=your_github_personal_access_token
```

Generate a Personal Access Token from **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**.

---

# Input Files

The tool expects three input datasets.

## Candidate CSV

Contains candidate contact information.

Example:

| candidate_id | full_name | email |
|--------------|-----------|-------|

---

## GitHub CSV

Contains GitHub profile URLs.

Example:

| candidate_id | github_url |
|--------------|------------|

---

## ATS JSON

Contains professional information.

Example:

```json
[
    {
        "candidate_id": "C001",
        "candidateName": "Lokesh S",
        "technical_skills": [
            "Python",
            "Docker"
        ]
    }
]
```

---

# Projection Configuration

Projection is controlled using a JSON configuration.

Example:

```json
{
    "fields": [
        {
            "path": "candidate_id"
        },
        {
            "path": "name",
            "from": "full_name"
        },
        {
            "path": "email",
            "from": "emails[0]"
        },
        {
            "path": "github",
            "from": "links.github"
        },
        {
            "path": "skills",
            "from": "skills[].name"
        }
    ],
    "include_confidence": true,
    "on_missing": "null"
}
```

Supported features:

- Field renaming
- Nested fields
- Array indexing
- List projection
- Field normalization
- Missing field handling

---

# Running the Tool

Example:

```bash
python main.py ^
    --csv data\small_candidates.csv ^
    --github data\small_github_links.csv ^
    --ats data\small_sample_ats_with_ids.json ^
    --config projection.json ^
    --output data\output.json
```

Linux/macOS:

```bash
python main.py \
    --csv data/small_candidates.csv \
    --github data/small_github_links.csv \
    --ats data/small_sample_ats_with_ids.json \
    --config projection.json \
    --output data/output.json
```

---

# Output

Example:

```json
{
    "candidate_id": "C001",
    "name": "Lokesh S",
    "email": "slokesh1810@gmail.com",
    "github": "https://github.com/SLokesh1810",
    "skills": [
        "Docker",
        "Python",
        "SQL"
    ],
    "overall_confidence": 0.91
}
```

---

# Provenance

Every merged field stores its origin.

Example:

```json
{
    "field": "skills",
    "source": "github, ats",
    "method": "merged"
}
```

This makes every output field traceable back to its source.

---

# Confidence Score

The overall confidence represents the completeness of the merged profile.

Fields such as:

- Name
- Email
- Phone
- Skills
- Experience
- Education
- Links
- Location

contribute to the final confidence score.

---

# Error Handling

The application handles:

- Missing input files
- Empty datasets
- Invalid GitHub URLs
- Missing GitHub profiles
- Invalid JSON
- Missing projection fields

---

# Author

Lokesh S