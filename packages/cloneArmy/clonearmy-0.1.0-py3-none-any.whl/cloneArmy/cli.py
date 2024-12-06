import sys
from pathlib import Path
from typing import Optional
import time
import logging

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import print as rprint
from Bio import SeqIO

from . import process_samples, summarize_results, validate_input, __version__
from .report import generate_report  # Import the new report generator

console = Console()

def load_reference_sequence(reference_path: Path) -> str:
    """Load the reference sequence from a FASTA file."""
    try:
        with open(reference_path) as handle:
            record = next(SeqIO.parse(handle, "fasta"))
            return str(record.seq)
    except Exception as e:
        console.print(f"[bold red]Error loading reference sequence:[/] {str(e)}")
        sys.exit(1)

def print_version(ctx, param, value):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return
    console.print(f"CloneArmy version [bold cyan]{__version__}[/]")
    ctx.exit()

@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="Show version and exit.")
@click.option('--debug/--no-debug', default=False, help="Enable debug logging.")

def cli(debug: bool):
    """
    CloneArmy: Analyze haplotypes from Illumina paired-end amplicon sequencing.
    
    This tool processes FASTQ files to identify and quantify sequence variants
    and haplotypes in amplicon sequencing data.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

@cli.command()
@click.argument('fastq_dir', type=click.Path(exists=True))
@click.argument('reference', type=click.Path(exists=True))
@click.option('--threads', '-t', default=8, help='Number of threads to use')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--min-base-quality', '-q', default=20, 
              help='Minimum base quality score')
@click.option('--min-mapping-quality', '-Q', default=30,
              help='Minimum mapping quality score')
@click.option('--report/--no-report', default=True,
              help='Generate HTML report')

def run(fastq_dir: str, reference: str, threads: int, output: Optional[str],
        min_base_quality: int, min_mapping_quality: int, report: bool):
    """Process amplicon sequencing data."""
    
    # Show welcome message
    console.print(Panel.fit(
        "[bold blue]CloneArmy[/] - Amplicon Analysis Tool",
        subtitle=f"Version {__version__}"
    ))

    # Load reference sequence
    reference_path = Path(reference)
    ref_seq = load_reference_sequence(reference_path)

    # Validate input
    with console.status("[bold yellow]Validating input..."):
        warnings = validate_input(fastq_dir, reference)
        if warnings:
            console.print("\n[bold red]Validation Warnings:[/]")
            for warning in warnings:
                console.print(f"⚠️  {warning}")
            if not click.confirm("Continue anyway?"):
                sys.exit(1)

    # Process samples
    start_time = time.time()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Processing samples...", total=None)
        
        try:
            results = process_samples(
                fastq_dir=fastq_dir,
                reference=reference,
                output_dir=output,
                threads=threads,
                min_base_quality=min_base_quality,
                min_mapping_quality=min_mapping_quality
            )
            progress.update(task, completed=True)
        except Exception as e:
            console.print(f"\n[bold red]Error:[/] {str(e)}")
            sys.exit(1)

    # Generate summary
    summary = summarize_results(results)
    
    # Display results
    console.print("\n[bold green]Analysis Complete![/]")
    
    table = Table(title="Sample Summary")
    table.add_column("Sample", style="cyan")
    table.add_column("Total Reads", justify="right", style="green")
    table.add_column("Unique Haplotypes", justify="right", style="blue")
    table.add_column("Max Frequency", justify="right", style="magenta")
    table.add_column("Avg Mutations", justify="right", style="red")
    
    for _, row in summary.iterrows():
        table.add_row(
            row['sample'],
            f"{row['total_reads']:,}",
            str(row['unique_haplotypes']),
            f"{row['max_frequency']:.1%}",
            f"{row['avg_mutations']:.2f}"
        )
    
    console.print(table)
    
    # Generate report if requested
    if report:
        output_dir = Path(output) if output else Path(fastq_dir) / 'results'
        report_path = output_dir / 'report.html'
        
        with console.status("[bold yellow]Generating report..."):
            generate_report(
                results=results,
                summary=summary,
                output_path=report_path,
                reference_seq=ref_seq
            )
        
        console.print(f"\nReport generated: [blue]{report_path}[/]")
    
    # Show completion message
    elapsed = time.time() - start_time
    console.print(f"\nTotal processing time: [bold]{elapsed:.1f}[/] seconds")

@cli.command()
@click.argument('results_dir', type=click.Path(exists=True))
@click.option('--reference', '-r', type=click.Path(exists=True), required=True,
              help='Reference FASTA file')
@click.option('--output', '-o', type=click.Path(), help='Output report path')

def report(results_dir: str, reference: str, output: Optional[str]):
    """Generate a report from existing results."""
    try:
        # Load reference sequence
        ref_seq = load_reference_sequence(Path(reference))
        
        # Load results
        results = load_results(results_dir)
        summary = summarize_results(results)
        
        output_path = Path(output) if output else Path(results_dir) / 'report.html'
        generate_report(
            results=results,
            summary=summary,
            output_path=output_path,
            reference_seq=ref_seq
        )
        
        console.print(f"\nReport generated: [blue]{output_path}[/]")
    except Exception as e:
        console.print(f"[bold red]Error generating report:[/] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    cli()