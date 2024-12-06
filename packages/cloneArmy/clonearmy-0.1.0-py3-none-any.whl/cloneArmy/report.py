from typing import Dict, List, Set, Tuple
import json
from pathlib import Path
import base64
from io import BytesIO, StringIO
import datetime
import logging
from collections import defaultdict
import shutil

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template

logger = logging.getLogger(__name__)

def fig_to_base64() -> str:
    """Convert matplotlib figure to base64 string."""
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    buf.seek(0)
    plt.close()
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

def create_mutation_spectrum(results: Dict[str, pd.DataFrame], reference_seq: str) -> str:
    """Create mutation spectrum analysis."""
    mutation_types = defaultdict(int)
    total_mutations = 0
    
    # Normalize reference sequence once
    reference_seq = reference_seq.upper()
    
    for df in results.values():
        if df.empty:
            continue
            
        for _, row in df.iterrows():
            haplotype = row['haplotype']
            count = row['count']
            
            for i, (ref, var) in enumerate(zip(reference_seq, haplotype)):
                if var.islower():  # This identifies a mutation
                    # Create mutation string with both bases in uppercase
                    mutation = f"{ref}>{var.upper()}"
                    # Only count if they're actually different after normalization
                    if ref != var.upper():
                        mutation_types[mutation] += count
                        total_mutations += count
    
    if not mutation_types:
        return ""
        
    plt.figure(figsize=(10, 6))
    types = sorted(mutation_types.keys())
    counts = [mutation_types[t] for t in types]
    
    # Convert to percentages
    percentages = [100 * c / total_mutations for c in counts]
    
    sns.barplot(x=types, y=percentages)
    plt.title('Mutation Spectrum')
    plt.xlabel('Mutation Type')
    plt.ylabel('Percentage of Total Mutations')
    plt.xticks(rotation=45)
    
    return fig_to_base64()

def generate_report(results: Dict[str, pd.DataFrame], 
                   summary: pd.DataFrame, 
                   output_path: Path,
                   reference_seq: str):
    """Generate HTML report with summary table and mutation spectrum plot."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate mutation spectrum plot
        mutation_spectrum = create_mutation_spectrum(results, reference_seq)
        
        # Generate HTML
        template = Template(HTML_TEMPLATE)
        report_html = template.render(
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=summary.to_html(classes=['table', 'table-striped'], index=False),
            mutation_spectrum=mutation_spectrum,
            has_data=bool(results and any(not df.empty for df in results.values()))
        )
        
        # Write report
        with output_path.open('w') as f:
            f.write(report_html)
            
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        # Create minimal error report
        with output_path.open('w') as f:
            f.write(f"""
            <html>
                <head><title>CloneArmy Analysis Report - Error</title></head>
                <body>
                    <h1>Error Generating Report</h1>
                    <p>Error: {str(e)}</p>
                    <h2>Raw Summary</h2>
                    <pre>{summary.to_string()}</pre>
                </body>
            </html>
            """)


def calculate_single_mutation_stats(results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calculate statistics for sequences with single mutations."""
    stats_list = []
    
    for sample, df in results.items():
        if df.empty:
            continue
            
        # Filter for sequences with exactly one mutation
        single_mut_df = df[df['mutations'] == 1]
        if not single_mut_df.empty:
            stats = {
                'sample': sample,
                'median_reads': int(single_mut_df['count'].median()),  # whole number
                'mean_reads': round(single_mut_df['count'].mean(), 2),  # 2 decimals if needed
                'std_reads': round(single_mut_df['count'].std(), 2),  # 2 decimals if needed
                'min_reads': int(single_mut_df['count'].min()),  # whole number
                'max_reads': int(single_mut_df['count'].max()),  # whole number
                'q25_reads': int(single_mut_df['count'].quantile(0.25)),  # whole number
                'q75_reads': int(single_mut_df['count'].quantile(0.75)),  # whole number
                'iqr_reads': int(single_mut_df['count'].quantile(0.75) - single_mut_df['count'].quantile(0.25))  # whole number
            }
            stats_list.append(stats)
    
    return pd.DataFrame(stats_list)


def generate_report(results: Dict[str, pd.DataFrame], 
                   summary: pd.DataFrame, 
                   output_path: Path,
                   reference_seq: str):
    """Generate HTML report with summary table and mutation spectrum plot."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate mutation spectrum plot
        mutation_spectrum = create_mutation_spectrum(results, reference_seq)
        
        # Calculate single mutation statistics
        single_mut_stats = calculate_single_mutation_stats(results)
        
        # Format the numbers in the single mutation stats table
        formatted_stats = single_mut_stats.copy()
        numeric_columns = formatted_stats.columns.difference(['sample'])
        formatted_stats[numeric_columns] = formatted_stats[numeric_columns].round(2)
        
        # Generate HTML
        template = Template(HTML_TEMPLATE)
        report_html = template.render(
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=summary.to_html(classes=['table', 'table-striped'], index=False),
            single_mutation_stats=single_mut_stats.to_html(classes=['table', 'table-striped'], index=False),
            mutation_spectrum=mutation_spectrum,
            has_data=bool(results and any(not df.empty for df in results.values()))
        )
        
        # Write report
        with output_path.open('w') as f:
            f.write(report_html)
            
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        # Create minimal error report
        with output_path.open('w') as f:
            f.write(f"""
            <html>
                <head><title>CloneArmy Analysis Report - Error</title></head>
                <body>
                    <h1>Error Generating Report</h1>
                    <p>Error: {str(e)}</p>
                    <h2>Raw Summary</h2>
                    <pre>{summary.to_string()}</pre>
                </body>
            </html>
            """)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CloneArmy Analysis Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; }
        .plot-container { margin: 20px 0; }
        .table {
            font-size: 0.9rem;
        }
        .plot-description {
            font-size: 0.9rem;
            color: #666;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">CloneArmy Analysis Report</h1>
        <p class="text-muted">Generated on: {{ date }}</p>

        <!-- Sample Summary -->
        <div class="card mb-4">
            <div class="card-header">
                <h2 class="h4 mb-0">Sample Summary</h2>
            </div>
            <div class="card-body">
                {{ summary }}
            </div>
        </div>

        <!-- Single Mutation Statistics -->
        <div class="card mb-4">
            <div class="card-header">
                <h2 class="h4 mb-0">Single Mutation Statistics</h2>
            </div>
            <div class="card-body">
                {{ single_mutation_stats }}
                <p class="plot-description">
                    Statistical summary of read counts for sequences containing exactly one mutation.
                    IQR = Interquartile Range (Q75 - Q25).
                </p>
            </div>
        </div>

        <!-- Mutation Spectrum -->
        {% if mutation_spectrum %}
        <div class="card mb-4">
            <div class="card-header">
                <h2 class="h4 mb-0">Mutation Spectrum</h2>
            </div>
            <div class="card-body">
                <img src="{{ mutation_spectrum }}" class="img-fluid" alt="Mutation Spectrum">
                <p class="plot-description">
                    Distribution of mutation types (e.g., A>T, G>C). Shows the percentage 
                    of each mutation type among all observed mutations.
                </p>
            </div>
        </div>
        {% endif %}

        <footer class="mt-5 pt-3 border-top text-muted">
            <small>Generated by CloneArmy | Data processed: {{ date }}</small>
        </footer>
    </div>
</body>
</html>
"""