import pandas as pd
import json
import os
import sys
from pathlib import Path
from pprint import pprint

from csv_adapter.table_extractor import transform_candidate
from github_adapter.web_extractor import git_extractor
from ats_adapter.extractor import ats_extractor
from cli import parse_args
from utils.config_loader import load_config
from projector.projector import Projector

from matcher.matcher import CandidateMatcher
from merger.merger import CandidateMerger


def main():
    args = parse_args()

    
    config_path = Path(args.config)

    projection_config = load_config(args.config)
    projector = Projector(projection_config)

    csv_path = Path(args.csv)
    github_path = Path(args.github)
    ats_path = Path(args.ats)

    for path in [csv_path, github_path, ats_path, config_path]:
        if not path.exists():
            print(f"Error: File not found: {path}")
            return
    

    csv_df = pd.read_csv(csv_path)
    csv_candidates = []
    for _, row in csv_df.iterrows():
        csv_candidates.append(
            transform_candidate(row)["candidate"]
        )

    github_df = pd.read_csv(github_path)
    github_candidates = []
    for _, row in github_df.iterrows():
        github_candidates.append(
            git_extractor(
                row["github_url"],
                row["candidate_id"]
            )
        )

    ats_candidates = ats_extractor(ats_path)
    matcher = CandidateMatcher()
    matched_candidates = matcher.match(
        csv_candidates,
        github_candidates,
        ats_candidates
    )

    merger = CandidateMerger()
    results = []
    for sources in matched_candidates.values():
        candidate = merger.merge(sources)
        candidate_dict = candidate.model_dump()

        projected = projector.project(candidate_dict)

        results.append(projected)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Generated {len(results)} candidates.")
    print(f"Saved to {args.output}")


if __name__ == "__main__":
    main()