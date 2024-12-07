# datasnatch/BLAST.py
# Import statements
import os

import numpy as np
import pandas as pd
import re
import requests
import seaborn as sns

from Bio import Align, Blast, SeqIO, SearchIO
from Bio.Blast import NCBIXML
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from matplotlib.figure import Figure

# Load .env
load_dotenv()

# Get environment variables
BLAST_EMAIL_ADDRESS = os.getenv("BLAST_EMAIL_ADDRESS")
BLAST_QUERY_FILE_PATH = os.getenv("BLAST_QUERY_FILE_PATH")
BLAST_XML_PATH = os.getenv("BLAST_XML_FILE") or Path(
    "~/.datasnatch/BLAST_results.xml"
).expanduser() # Get file path for `BLAST_results.xml`

if not BLAST_XML_PATH.parent.exists():
    BLAST_XML_PATH.parent.mkdir(parents=True, exist_ok=True)

def extract_species_name(title: str) -> str:
    """
    Extract species name from BLAST hit title.

    Args:
        title (str): The BLAST hit title.

    Returns:
        str: Extracted species name.
    """

    # Regex
    patterns = [
        r"\[(.*?)\]", # Matches anything in square brackets
        r"(?<=\s)([A-Z][a-z]+\s+[a-z]+)(?=\s|$)", # Matches *Genus species* format
    ]

    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1).strip()
        return ""


class Blaster:
    def __init__(
            self,
            query: Optional[Union[str, List[str]]] = None,
            email: Optional[str] = None
    ) -> None:
        self.alignment = None
        self.file_path = BLAST_QUERY_FILE_PATH
        self.query = open(self.file_path, "r").read()
        self.email = email or BLAST_EMAIL_ADDRESS

        self.get_alignment()

    def get_alignment(self):
        self.alignment = Align.read(self.file_path, "fasta")


def analyze_blast_xml(
    blast_xml_file: Path | str,
    exclude: Optional[str | List[str]] = None,
) -> tuple[None, pd.DataFrame] | tuple[Figure, pd.DataFrame]:
    """
    Analyze BLAST results and generate insights.

    Args:
        blast_xml_file (Path, str): Path to BLAST XML file.
        exclude (str, list, optional): Species to exclude from analysis. Defaults to None.

    Returns:
        tuple[Figure, DataFrame] | tuple[None, DataFrame]: A tuple containing the analysis results. First item defaults to None if DataFrame is empty after BLAST results are filtered by provided exclude list.
    """

    # Convert single species to list for consistent handling
    if exclude is not None:
        if isinstance(exclude, str):
            exclude = [exclude]
        # Convert to lowercase for case-insensitive comparison
        exclude = [species.lower() for species in exclude]

    # Parse BLAST results from XML
    blast_results = NCBIXML.parse(open(blast_xml_file))

    # Initialization
    e_values = []
    bit_scores = []
    alignments_data = []

    # Extract data from BLAST results
    for result in blast_results:
        for alignment in result.alignments:
            species = extract_species_name(alignment.title)

            if exclude and species.lower() in exclude: continue

            for hsp in alignment.hsps:
                e_values.append(hsp.expect)
                bit_scores.append(hsp.bits)
                alignments_data.append({
                    "accession": alignment.accession,
                    "length": alignment.length,
                    "e_value": hsp.expect,
                    "bit_score": hsp.bits,
                    "identity": hsp.identities / float(hsp.align_length),
                    "gaps": hsp.gaps,
                    "align_length": hsp.align_length
                })

    # Convert to `DataFrame`
    df = pd.DataFrame(alignments_data)

    # Skip visualization if no data exists in the data frame after filtering
    if df.empty:
        print("No data remaining after species exclusion")
        return None, df

    # Visualize
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    # E-value distribution
    sns.histplot(data=df, x="e_value", ax=ax1, log_scale=True)
    ax1.set_title("E-value Distribution")
    ax1.set_xlabel("E-value (Logarithmic Scale)")

    # Bit Score vs. Identity
    sns.scatterplot(data=df, x="bit_score", y="identity", ax=ax2)
    ax2.set_title("Bit-score vs. Sequence Identity")
    ax2.set_xlabel("Bit Score")
    ax2.set_ylabel("Identity")

    # Alignment length distribution
    sns.histplot(data=df, x="align_length", ax=ax3)
    ax3.set_title("Alignment Length Distribution")
    ax3.set_xlabel("Alignment Length")

    # Top Hits by Bit Score
    top_hits = df.nlargest(10, "bit_score")
    sns.barplot(data=top_hits, x="bit_score", y="accession", ax=ax4)
    ax4.set_title("Top 10 Hits by Bit Score")
    ax4.set_xlabel("Bit Score")
    ax4.set_ylabel("Accession")

    plt.tight_layout()
    return fig, df


def generate_alignment_summary(
        df: pd.DataFrame
) -> Dict[str, str | int | Dict[str, int]]:
    """
    Generate a summary of the BLAST alignments.

    Args:
        df (pandas.DataFrame): A DataFrame containing the BLAST alignment results.

    Returns:
        Dict[str, str | int | Dict[str, int]]: A dictionary containing the summary of the alignments.
    """
    if df.empty:
        return {
            "total_hits": 0,
            "species_count": 0,
            "error": "No data remaining after filtering."
        }

    summary = {
        "total_hits": len(df),
        "avg_identity": df["identity"].mean() * 100,
        "median_e_value": df["e_value"].median(),
        "avg_alignment_length": df["align_length"].mean(),
        "high_confidence_hits": len(df[df["e_value"] < 1e-50]),
    }
    return summary


def main() -> None:
    fig, df = analyze_blast_xml(
        BLAST_XML_PATH,
        exclude=["M. abscessus", "Mycobacteroides abscessus"]
    )

    # Get summary
    summary = generate_alignment_summary(df)
    print("\nAlignment Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()