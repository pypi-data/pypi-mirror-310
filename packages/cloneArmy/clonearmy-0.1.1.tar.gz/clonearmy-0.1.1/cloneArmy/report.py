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

def get_full_length_single_mutations_stats(df: pd.DataFrame) -> Tuple[int, float]:
    """Calculate full length single mutations count and percentage."""
    if df.empty:
        return 0, 0.0
    
    # Filter for full-length sequences with exactly one mutation
    full_length_single = df[(df['mutations'] == 1) & (df['is_full_length'] == True)]
    count = len(full_length_single)
    
    # Calculate percentage of all sequences
    total_sequences = len(df)
    percentage = (count / total_sequences * 100) if total_sequences > 0 else 0.0
    
    return count, round(percentage, 2)

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

def calculate_full_length_mutation_stats(results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Calculate statistics for full-length sequences with single mutations."""
    stats_list = []
    
    for sample, df in results.items():
        if df.empty:
            continue
            
        # Filter for full-length sequences with exactly one mutation
        full_length_single_mut_df = df[(df['mutations'] == 1) & (df['is_full_length'] == True)]
        if not full_length_single_mut_df.empty:
            stats = {
                'sample': sample,
                'median_reads': int(full_length_single_mut_df['count'].median()),
                'mean_reads': round(full_length_single_mut_df['count'].mean(), 2),
                'std_reads': round(full_length_single_mut_df['count'].std(), 2),
                'min_reads': int(full_length_single_mut_df['count'].min()),
                'max_reads': int(full_length_single_mut_df['count'].max()),
                'q25_reads': int(full_length_single_mut_df['count'].quantile(0.25)),
                'q75_reads': int(full_length_single_mut_df['count'].quantile(0.75)),
                'iqr_reads': int(full_length_single_mut_df['count'].quantile(0.75) - 
                               full_length_single_mut_df['count'].quantile(0.25))
            }
            stats_list.append(stats)
    
    return pd.DataFrame(stats_list)

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
        
        # Get mutation statistics from the first row (where they're stored by processor)
        first_row = df.iloc[0] if not df.empty else {}
        
        summary_data.append({
            'sample': sample,
            'total_reads': total_reads,
            'unique_haplotypes': unique_haplotypes,
            'max_frequency': max_freq,
            'avg_mutations': avg_mutations,
            'possible_single_mutations': first_row.get('possible_single_mutations', 0),
            'single_mutations': first_row.get('single_mutations', 0),
            'single_mutation_coverage': first_row.get('single_mutation_coverage', 0),
            'single_mutations_full_length': first_row.get('full_length_single_mutations', 0),
            'single_mutation_coverage_full_length': first_row.get('full_length_single_mutation_coverage', 0)
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Format for display
    if not summary_df.empty:
        # Round percentages to 2 decimal places
        percentage_cols = ['max_frequency', 'single_mutation_coverage', 'single_mutation_coverage_full_length']
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
        
        # Calculate other statistics
        single_mut_stats = calculate_single_mutation_stats(results)
        full_length_mut_stats = calculate_full_length_mutation_stats(results)
        
        # Pre-format statistics DataFrames
        for stats_df in [single_mut_stats, full_length_mut_stats]:
            if not stats_df.empty:
                numeric_columns = stats_df.columns.difference(['sample'])
                for col in numeric_columns:
                    stats_df[col] = stats_df[col].apply(lambda x: f"{x:.2f}")
        
        # Format summary DataFrame for display
        display_columns = {
            'sample': 'Sample',
            'total_reads': 'Total Reads',
            'unique_haplotypes': 'Unique Haplotypes',
            'max_frequency': 'Max Frequency (%)',
            'avg_mutations': 'Avg Mutations',
            'possible_single_mutations': 'Possible Single Mutations',
            'single_mutations': 'Single Mutations',
            'single_mutation_coverage': 'Single Mutation Coverage (%)',
            'single_mutations_full_length': 'Full Length Single Mutations',
            'single_mutation_coverage_full_length': 'Full Length Single Mutation Coverage (%)'
        }
        
        summary = summary.rename(columns=display_columns)
        
        # Generate HTML
        template = Template(HTML_TEMPLATE)
        report_html = template.render(
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary=summary.to_html(
                classes=['table', 'table-striped', 'table-bordered', 'table-hover'],
                index=False,
                float_format=lambda x: '{:,.2f}'.format(x) if isinstance(x, float) else '{:,}'.format(x) if isinstance(x, int) else x
            ),
            single_mutation_stats=single_mut_stats.to_html(
                classes=['table', 'table-striped', 'table-bordered', 'table-hover'],
                index=False
            ),
            full_length_mutation_stats=full_length_mut_stats.to_html(
                classes=['table', 'table-striped', 'table-bordered', 'table-hover'],
                index=False
            ),
            mutation_spectrum=mutation_spectrum,
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

        <!-- Single Mutation Statistics -->
        <div class="card mb-4">
            <div class="card-header">
                <h2 class="h4 mb-0">Single Mutation Statistics</h2>
            </div>
            <div class="card-body">
                <table id="singleMutationTable" class="table table-striped table-bordered">
                    {{ single_mutation_stats }}
                </table>
                <p class="plot-description">
                    Statistical summary of read counts for sequences containing exactly one mutation.
                    IQR = Interquartile Range (Q75 - Q25).
                </p>
            </div>
        </div>

        <!-- Full Length Single Mutation Statistics -->
        <div class="card mb-4">
            <div class="card-header">
                <h2 class="h4 mb-0">Full Length Single Mutation Statistics</h2>
            </div>
            <div class="card-body">
                <table id="fullLengthTable" class="table table-striped table-bordered">
                    {{ full_length_mutation_stats }}
                </table>
                <p class="plot-description">
                    Statistical summary of read counts for sequences that cover the entire reference sequence
                    and contain exactly one mutation. IQR = Interquartile Range (Q75 - Q25).
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

    <script>
        $(document).ready(function() {
            // Initialize DataTables
            $('#summaryTable').DataTable({
                pageLength: 25,
                order: [[1, 'desc']],
                dom: 'Bfrtip',
                buttons: ['copy', 'csv', 'excel']
            });
            
            $('#singleMutationTable').DataTable({
                pageLength: 25,
                order: [[1, 'desc']],
                scrollX: true
            });
            
            $('#fullLengthTable').DataTable({
                pageLength: 25,
                order: [[1, 'desc']],
                scrollX: true
            });
        });
    </script>
</body>
</html>
"""