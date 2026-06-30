import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog="candidate-transformer",
        description="Merge candidate data from multiple sources into a canonical profile."
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to candidate CSV"
    )

    parser.add_argument(
        "--github",
        required=True,
        help="Path to GitHub CSV"
    )

    parser.add_argument(
        "--ats",
        required=True,
        help="Path to ATS JSON"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Projection configuration JSON"
    )

    parser.add_argument(
        "--output",
        required=False,
        default="output.json",
        help="Output JSON file"
    )

    return parser.parse_args()