import requests
import numpy as np
import pandas as pd
import time

from Bio import Entrez, SeqIO
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from matplotlib import colormaps, figure
from matplotlib.figure import Figure
from os import getenv
from typing import Any, Dict, List, Optional, Tuple

cmap = colormaps["viridis"]

# Load .env
load_dotenv()

# Environment variables
SEQUENCE_ID: str = getenv("SEQUENCE_ID")

# Kyte-Doolittle hydrophobicity scale
HYDROPHOBICITY_SCALE = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}


def calculate_hydrophobicity(sequence: str, window_size: int = 19) -> np.ndarray:
    """
    Calculate hydrophobicity using Kyte-Doolittle scale with sliding window.

    Args:
        sequence (str): Protein sequence
        window_size (int): Size of sliding window (default 19 for transmembrane prediction)

    Returns:
        np.ndarray: Hydrophobicity scores
    """
    # Convert sequence to hydrophobicity values
    hydro_values = np.array([HYDROPHOBICITY_SCALE.get(aa, 0) for aa in sequence])

    # Pad the array for the sliding window
    pad_width = window_size // 2
    padded_values = np.pad(hydro_values, pad_width, mode='edge')

    # Calculate moving average
    window = np.ones(window_size) / window_size
    hydro_scores = np.convolve(padded_values, window, mode='valid')

    return hydro_scores


def analyze_domains(
    sequence_id: str,
    email: str,
    db: str = "cdd",
    threshold: float = 0.01,
    debug: bool = True,  # Always debug for now
    timeout_minutes: float = 5,
    use_precomputed: bool = True
) -> tuple:
    """
    Analyze protein sequence for conserved domains using NCBI's CD-Search.
    """
    print("\n=== Starting Analysis ===")
    print(f"Sequence ID: {sequence_id}")

    # Set email for NCBI queries
    Entrez.email = email

    # Fetch sequence
    try:
        handle = Entrez.efetch(db="protein", id=sequence_id, rettype="fasta")
        sequence_record = SeqIO.read(handle, "fasta")
        handle.close()
        print(f"Retrieved sequence length: {len(sequence_record.seq)}")
    except Exception as e:
        raise Exception(f"Failed to fetch sequence {sequence_id}: {str(e)}")

    base_url = "https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi"

    # Try precomputed results first if requested
    if use_precomputed:
        print("\n=== Checking Pre-computed Results ===")
        precomputed_params = {
            'db': db,
            'queries': sequence_id,
            'tdata': 'hits',
            'dmode': 'full',
            'tmode': 'rep',
            'smode': 'prec',
            'useid1': 'true',
            'maxhit': '500',
            'filter': 'true',
            'evalue': str(threshold),
            'compbasedadj': 'true',
            'CMD': 'Put'
        }

        print("Request Parameters:")
        print(precomputed_params)

        response = requests.get(base_url, params=precomputed_params)

        print("\nInitial Response:")
        print("Status Code:", response.status_code)
        print("Response Text:")
        print(response.text)

        if "No hits" not in response.text and "Error" not in response.text:
            print("\nFound pre-computed results!")
            use_response = response
        else:
            print("\nNo pre-computed results, running new search...")
            submit_params = {
                'db': db,
                'queries': str(sequence_record.seq),
                'CMD': 'Put',
                'smode': 'auto',
                'tdata': 'hits',
                'dmode': 'full',
                'tmode': 'rep'
            }

            print("\nSubmit Parameters:")
            print(submit_params)

            response = requests.get(base_url, params=submit_params)
            use_response = response

            print("\nSubmit Response:")
            print("Status Code:", response.status_code)
            print("Response Text:")
            print(response.text)

    # Parse the response to get Request ID
    print("\n=== Parsing Initial Response ===")
    cdsid = None

    for line in use_response.text.split('\n'):
        print(f"Processing line: '{line}'")
        if line.startswith('#cdsid'):
            cdsid = line.split('\t')[1].strip()
            print(f"Found cdsid: {cdsid}")

    if not cdsid:
        raise Exception("Failed to get CD-Search ID")

    print(f"\n=== Starting Result Polling with cdsid: {cdsid} ===")

    # Poll for results
    max_tries = int(timeout_minutes * 60 / 10)
    wait_time = 10  # seconds
    start_time = time.time()

    for try_num in range(max_tries):
        elapsed_time = time.time() - start_time
        elapsed_minutes = elapsed_time / 60

        print(f"\nPoll attempt {try_num + 1}/{max_tries}")
        print(f"Time elapsed: {elapsed_minutes:.1f} minutes")

        time.sleep(wait_time)

        poll_params = {
            'CMD': 'Get',
            'cdsid': cdsid
        }

        print("\nPoll Parameters:")
        print(poll_params)

        poll_response = requests.get(base_url, params=poll_params)

        print("\nPoll Response:")
        print("Status Code:", poll_response.status_code)
        print("Response Text:")
        print(poll_response.text)

        # Parse status from response
        for line in poll_response.text.split('\n'):
            if line.startswith('#status'):
                parts = line.split('\t')
                if len(parts) >= 2:
                    status = parts[1].strip()
                    message = parts[2].strip() if len(parts) > 2 else "No message"
                    print(f"\nFound status: {status}")
                    print(f"Message: {message}")

                    if status == '0':  # Success
                        print("\n=== Processing Results ===")
                        header = None
                        domain_data = []

                        for line in poll_response.text.split('\n'):
                            if line.startswith('Q#1'):  # Only process lines for our query
                                try:
                                    # Split the line and remove any empty strings
                                    fields = [f for f in line.split('\t') if f]

                                    if len(fields) >= 9:  # Make sure we have enough fields
                                        domain_data.append({
                                            'query': fields[0],
                                            'hit_type': fields[1],
                                            'pssm_id': fields[2],
                                            'from': int(fields[3]),
                                            'to': int(fields[4]),
                                            'e_value': float(fields[5]),
                                            'bit_score': float(fields[6]),
                                            'accession': fields[7],
                                            'short_name': fields[8],
                                            'incomplete': fields[9] if len(fields) > 9 else '',
                                            'superfamily': fields[10] if len(fields) > 10 else ''
                                        })
                                except (IndexError, ValueError) as e:
                                    if debug:
                                        print(f"Warning: Could not parse line: {line}")
                                        print(f"Error: {str(e)}")
                                    continue

                        df = pd.DataFrame(domain_data)

                        if df.empty:
                            print("No domains found")
                            return df, None

                        # Sort by e-value and domain size
                        df = df.assign(domain_size=df['to'] - df['from'])
                        df = df.sort_values(['e_value', 'domain_size'], ascending=[True, False])

                        # Create visualization with improved layout
                        fig = visualize_domains(df, str(sequence_record.seq))

                        # Print a summary of the most significant hits
                        print("\nTop 5 most significant domain hits:")
                        summary_df = df[['short_name', 'hit_type', 'from', 'to', 'e_value', 'bit_score']].head()
                        print(summary_df.to_string(index=False))

                        return df, fig

                    elif status in ['1', '2', '3']:  # Running states
                        break
                    else:
                        raise Exception(f"Search failed: {message}")
                break
        else:
            print("\nNo status line found in response!")
            print("Full response text:")
            print(poll_response.text)
            raise Exception("Failed to get status from poll response")

    raise Exception(f"Analysis timed out after {timeout_minutes} minutes")


def visualize_domains(df: pd.DataFrame, sequence: str) -> plt.Figure:
    """
    Create a visualization of domain architecture with hydrophobicity plot.
    """
    # Calculate hydrophobicity
    hydro_scores = calculate_hydrophobicity(sequence)

    # Create figure with three subplots and increased spacing
    fig = plt.figure(figsize=(15, 12))

    # Create gridspec for custom subplot layout
    gs = fig.add_gridspec(3, 1, height_ratios=[3, 2, 2], hspace=0.4)

    # Create subplots with gridspec
    ax1 = fig.add_subplot(gs[0])  # Domain architecture
    ax2 = fig.add_subplot(gs[1])  # Domain overlap
    ax3 = fig.add_subplot(gs[2])  # Hydrophobicity

    # Filter to show only specific hits and superfamilies
    plot_df = df[df['hit_type'].isin(['specific', 'superfamily'])].copy()
    n_domains = len(plot_df)
    y_positions = np.linspace(0, n_domains * 1.2, n_domains)
    colors = cmap(np.linspace(0, 1, n_domains))

    # Plot domains as blocks
    for idx, (_, row) in enumerate(plot_df.iterrows()):
        y_pos = y_positions[idx]
        width = row['to'] - row['from']
        left = row['from']

        # Plot domain block
        ax1.barh(y_pos, width, left=left, height=0.3,
                 color=colors[idx], alpha=0.7)

        # Add label
        label = f"{row['short_name']} (e={row['e_value']:.1e})"
        label_x = left + width / 2
        label_y = y_pos + 0.1

        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9)
        ax1.text(label_x, label_y, label,
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 fontsize=10,
                 bbox=bbox_props)

    # Set axis properties for domain plot
    ax1.set_yticks([])
    ax1.set_xlabel('Amino Acid Position')
    ax1.set_title('Domain Architecture', pad=20)

    # Add sequence length markers
    seq_len = len(sequence)
    ax1.set_xlim(-10, seq_len + 10)
    tick_positions = np.arange(0, seq_len + 100, 100)
    ax1.set_xticks(tick_positions)

    # Add domain overlap plot
    coverage = np.zeros(len(sequence))
    for _, row in df.iterrows():
        coverage[int(row['from']):int(row['to'])] += 1

    ax2.plot(range(len(sequence)), coverage, color='navy')
    ax2.fill_between(range(len(sequence)), coverage, alpha=0.3, color='navy')

    # Set explicit y-axis for domain overlap with less frequent ticks
    max_overlap = int(np.max(coverage))
    ax2.set_ylim(0, max_overlap + 0.5)  # Keep the padding
    y_ticks = np.arange(0, max_overlap + 1, 5)  # Ticks at intervals of 5
    ax2.set_yticks(y_ticks)
    ax2.set_yticklabels([str(int(i)) for i in y_ticks])

    ax2.set_xlabel('Amino Acid Position')
    ax2.set_ylabel('Number of\nOverlapping\nDomains')
    ax2.set_xlim(-10, seq_len + 10)
    ax2.set_xticks(tick_positions)

    # Add hydrophobicity plot
    ax3.plot(range(len(hydro_scores)), hydro_scores, color='red')
    ax3.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax3.fill_between(range(len(hydro_scores)), hydro_scores,
                     where=(hydro_scores > 0),
                     color='red', alpha=0.3)
    ax3.fill_between(range(len(hydro_scores)), hydro_scores,
                     where=(hydro_scores < 0),
                     color='blue', alpha=0.3)
    ax3.set_xlabel('Amino Acid Position')
    ax3.set_ylabel('Hydrophobicity\nScore')
    ax3.set_xlim(-10, seq_len + 10)
    ax3.set_xticks(tick_positions)

    # Add threshold line for potential transmembrane regions
    ax3.axhline(y=1.6, color='green', linestyle='--', alpha=0.5,
                label='Transmembrane threshold')
    ax3.legend()

    # Add gridlines
    ax1.grid(True, axis='x', linestyle='--', alpha=0.3)
    ax2.grid(True, axis='x', linestyle='--', alpha=0.3)
    ax3.grid(True, axis='x', linestyle='--', alpha=0.3)

    # Adjust layout for better spacing
    plt.gcf().set_layout_engine("constrained")

    return fig


def main(sequence_id: Optional[str] = None) -> None:
    if not sequence_id and SEQUENCE_ID:
        sequence_id = SEQUENCE_ID
    domains_df, fig = analyze_domains(
        sequence_id=sequence_id,
        email="rice97@live.missouristate.edu"
    )

    if not domains_df.empty:
        print("\nFound Domains:")
        print(domains_df[['short_name', 'from', 'to', 'e_value']])
        plt.show()


# Example usage:
if __name__ == "__main__":
    main()