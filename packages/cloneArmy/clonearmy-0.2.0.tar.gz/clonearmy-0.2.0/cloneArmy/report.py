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
    double_mutations = defaultdict(int)
    
    # Normalize reference sequence once
    reference_seq = reference_seq.upper()
    
    for df in results.values():
        if df.empty:
            continue
            
        for _, row in df.iterrows():
            haplotype = row['haplotype']
            count = row['count']
            
            # Track positions with mutations for linked analysis
            mutation_positions = []
            
            for i, (ref, var) in enumerate(zip(reference_seq, haplotype)):
                if var.islower():  # This identifies a mutation
                    # Create mutation string with both bases in uppercase
                    mutation = f"{ref}>{var.upper()}"
                    # Only count if they're actually different after normalization
                    if ref != var.upper():
                        mutation_types[mutation] += count
                        total_mutations += count
                        mutation_positions.append((i + 1, ref, var.upper()))
            
            # Process linked mutations
            for i in range(len(mutation_positions)):
                for j in range(i + 1, len(mutation_positions)):
                    pos1, ref1, mut1 = mutation_positions[i]
                    pos2, ref2, mut2 = mutation_positions[j]
                    double_key = f"({pos1}{ref1}>{mut1}, {pos2}{ref2}>{mut2})"
                    double_mutations[double_key] += count
    
    if not mutation_types:
        return ""
        
    # Create single mutation spectrum
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    types = sorted(mutation_types.keys())
    counts = [mutation_types[t] for t in types]
    percentages = [100 * c / total_mutations for c in counts]
    
    sns.barplot(x=types, y=percentages)
    plt.title('Single Mutation Spectrum')
    plt.xlabel('Mutation Type')
    plt.ylabel('Percentage of Total Mutations')
    plt.xticks(rotation=45)
    
    # Create linked mutation spectrum (top 10 most frequent)
    plt.subplot(1, 2, 2)
    if double_mutations:
        sorted_doubles = sorted(double_mutations.items(), key=lambda x: x[1], reverse=True)[:10]
        double_types, double_counts = zip(*sorted_doubles)
        double_percentages = [100 * c / total_mutations for c in double_counts]
        
        sns.barplot(x=list(range(len(double_types))), y=double_percentages)
        plt.title('Top 10 Linked Mutations')
        plt.xlabel('Mutation Pair')
        plt.ylabel('Percentage of Total Mutations')
        plt.xticks(range(len(double_types)), double_types, rotation=45, ha='right')
    
    plt.tight_layout()
    return fig_to_base64()

def format_summary_table(results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Format complete summary table with all mutation statistics."""
    summary_data = []
    
    for sample, df in results.items():
        if df.empty:
            continue
            
        # Basic stats
        total_reads = df['count'].sum()
        unique_haplotypes = len(df)
        max_freq = (df['count'].max() / total_reads * 100) if total_reads > 0 else 0.0
        avg_mutations = (df['mutations'] * df['count']).sum() / total_reads if total_reads > 0 else 0.0
        
        # Full length statistics
        full_length_reads = df[df['is_full_length']]['count'].sum()
        full_length_percent = (full_length_reads / total_reads * 100) if total_reads > 0 else 0.0
        
        # Single mutation statistics
        single_mut_reads = df[df['mutations'] == 1]['count'].sum()
        single_mut_percent = (single_mut_reads / total_reads * 100) if total_reads > 0 else 0.0
        
        # Full length single mutations
        full_length_single = df[(df['mutations'] == 1) & (df['is_full_length'])]['count'].sum()
        full_length_single_percent = (full_length_single / total_reads * 100) if total_reads > 0 else 0.0
        
        summary_data.append({
            'sample': sample,
            'total_reads': total_reads,
            'unique_haplotypes': unique_haplotypes,
            'max_frequency': max_freq,
            'avg_mutations': avg_mutations,
            'full_length_reads': full_length_reads,
            'full_length_percent': full_length_percent,
            'single_mutations': single_mut_reads,
            'single_mutation_percent': single_mut_percent,
            'full_length_single_mutations': full_length_single,
            'full_length_single_percent': full_length_single_percent
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Format for display
    if not summary_df.empty:
        # Round percentages to 2 decimal places
        percentage_cols = ['max_frequency', 'full_length_percent', 
                         'single_mutation_percent', 'full_length_single_percent']
        summary_df[percentage_cols] = summary_df[percentage_cols].round(2)
        
        # Round avg_mutations to 2 decimal places
        summary_df['avg_mutations'] = summary_df['avg_mutations'].round(2)
    
    return summary_df

def generate_report(results: Dict[str, pd.DataFrame], 
                   summary: pd.DataFrame, 
                   output_path: Path,
                   reference_seq: str):
    """Generate HTML report with summary table and mutation spectrum plot."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Format full summary table
        summary = format_summary_table(results)
        
        # Generate mutation spectrum plot
        mutation_spectrum = create_mutation_spectrum(results, reference_seq)
        
        # Calculate additional statistics
        stats_data = {}
        for sample, df in results.items():
            if df.empty:
                continue
                
            # Get mutation rates for different read lengths
            mutation_rates = df.groupby('mutations')['count'].sum() / df['count'].sum() * 100
            stats_data[sample] = {
                'mutation_rates': mutation_rates.to_dict(),
                'total_reads': df['count'].sum(),
                'unique_haplotypes': len(df),
                'full_length_percent': (df[df['is_full_length']]['count'].sum() / df['count'].sum() * 100)
            }
        
        # Generate HTML
        template = Template(HTML_TEMPLATE)
        report_html = template.render(
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=summary.to_html(
                classes=['table', 'table-striped', 'table-bordered', 'table-hover'],
                index=False,
                float_format=lambda x: '{:,.2f}'.format(x) if isinstance(x, float) else '{:,}'.format(x) if isinstance(x, int) else x
            ),
            mutation_spectrum=mutation_spectrum,
            stats=stats_data,
            has_data=bool(results and any(not df.empty for df in results.values()))
        )
        
        # Write report
        with output_path.open('w') as f:
            f.write(report_html)
            
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CloneArmy Analysis Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap5.min.js"></script>
    <style>
        body { padding: 20px; }
        .plot-container { margin: 20px 0; }
        .table {
            font-size: 0.9rem;
            width: 100% !important;
        }
        .plot-description {
            font-size: 0.9rem;
            color: #666;
            margin-top: 10px;
        }
        .dataTables_wrapper {
            padding: 10px 0;
        }
        .card-body {
            overflow-x: auto;
        }
        th, td {
            white-space: nowrap;
        }
        .text-end {
            text-align: right;
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
                <p class="plot-description">
                    Overview of sequencing results and mutation statistics for each sample.
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
                    Left: Distribution of single mutation types (e.g., A>T, G>C). Shows the percentage 
                    of each mutation type among all observed mutations.<br>
                    Right: Top 10 most frequent linked mutations showing co-occurring mutation pairs.
                </p>
            </div>
        </div>
        {% endif %}

        <!-- Per-Sample Statistics -->
        {% for sample, stats in stats.items() %}
        <div class="card mb-4">
            <div class="card-header">
                <h2 class="h4 mb-0">{{ sample }} Details</h2>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h3 class="h5">Basic Statistics</h3>
                        <ul>
                            <li>Total Reads: {{ "{:,}".format(stats.total_reads) }}</li>
                            <li>Unique Haplotypes: {{ "{:,}".format(stats.unique_haplotypes) }}</li>
                            <li>Full Length Sequences: {{ "%.2f"|format(stats.full_length_percent) }}%</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h3 class="h5">Mutation Rates</h3>
                        <ul>
                            {% for mutations, rate in stats.mutation_rates.items() %}
                            <li>{{ mutations }} mutation(s): {{ "%.2f"|format(rate) }}%</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}

        <footer class="mt-5 pt-3 border-top text-muted">
            <small>Generated by CloneArmy | Data processed: {{ date }}</small>
        </footer>
    </div>

    <script>
        $(document).ready(function() {
            $('.table').DataTable({
                pageLength: 25,
                order: [[1, 'desc']],
                dom: 'Bfrtip',
                buttons: ['copy', 'csv', 'excel']
            });
        });
    </script>
</body>
</html>
"""