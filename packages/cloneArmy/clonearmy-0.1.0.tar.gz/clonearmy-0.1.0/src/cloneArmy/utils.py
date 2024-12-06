from pathlib import Path
from typing import Union, Dict, List
import logging
import pandas as pd

from .processor import AmpliconProcessor

logger = logging.getLogger(__name__)

def process_samples(
    fastq_dir: Union[str, Path],
    reference: Union[str, Path],
    output_dir: Union[str, Path, None] = None,
    threads: int = 4,
    min_base_quality: int = 20,
    min_mapping_quality: int = 30
) -> Dict[str, pd.DataFrame]:
    """
    Process all samples in a directory.

    Args:
        fastq_dir: Directory containing FASTQ files
        reference: Path to reference FASTA file
        output_dir: Directory for output files (default: fastq_dir/results)
        threads: Number of threads to use
        min_base_quality: Minimum base quality score
        min_mapping_quality: Minimum mapping quality score

    Returns:
        Dictionary mapping sample names to their results DataFrames
    """
    fastq_dir = Path(fastq_dir)
    reference = Path(reference)
    output_dir = Path(output_dir) if output_dir else fastq_dir / 'results'

    # Initialize processor
    processor = AmpliconProcessor(
        reference_path=reference,
        min_base_quality=min_base_quality,
        min_mapping_quality=min_mapping_quality
    )

    # Process each sample
    results = {}
    for r1_file in fastq_dir.glob('*R1_001.fastq.gz'):
        r2_file = r1_file.parent / r1_file.name.replace('R1', 'R2')
        if not r2_file.exists():
            logger.warning(f"No R2 file found for {r1_file.name}")
            continue

        sample_name = r1_file.stem.replace('_R1_001.fastq.gz', '')
        logger.info(f"Processing sample: {sample_name}")

        try:
            results[sample_name] = processor.process_sample(
                fastq_r1=r1_file,
                fastq_r2=r2_file,
                output_dir=output_dir,
                threads=threads
            )
        except Exception as e:
            logger.error(f"Error processing sample {sample_name}: {str(e)}")
            continue

    return results

def summarize_results(results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create a summary of results across all samples."""
    if not results:
        return pd.DataFrame()
        
    summaries = []
    for sample, df in results.items():
        try:
            summary = {
                'sample': sample,
                'total_reads': int(df['count'].sum()),  # whole number
                'unique_haplotypes': int(len(df)),  # whole number
                'max_frequency': round(df['frequency'].max() * 100),  # percentage, no decimals
                'avg_mutations': round((df['mutations'] * df['frequency']).sum(), 2),  # keep 2 decimals if needed
                'single_mutations': int(df.iloc[0].get('single_mutations', 0)),  # whole number
                'possible_single_mutations': int(df.iloc[0].get('possible_single_mutations', 0)),  # whole number
                'single_mutation_coverage': round(df.iloc[0].get('single_mutation_coverage', 0) * 100)  # percentage, no decimals
            }
            summaries.append(summary)
        except Exception as e:
            logger.error(f"Error summarizing results for {sample}: {str(e)}")
            continue
    
    return pd.DataFrame(summaries)

def validate_input(
    fastq_dir: Union[str, Path],
    reference: Union[str, Path]
) -> List[str]:
    """
    Validate input files and return any warnings.

    Args:
        fastq_dir: Directory containing FASTQ files
        reference: Path to reference FASTA file

    Returns:
        List of warning messages, empty if all valid
    """
    warnings = []
    
    # Check reference file
    ref_path = Path(reference)
    if not ref_path.exists():
        warnings.append(f"Reference file not found: {ref_path}")
    elif ref_path.stat().st_size == 0:
        warnings.append(f"Reference file is empty: {ref_path}")

    # Check BWA index files
    for ext in ['.amb', '.ann', '.bwt', '.pac', '.sa']:
        if not (ref_path.parent / (ref_path.name + ext)).exists():
            warnings.append(f"BWA index file missing: {ref_path}{ext}")

    # Check FASTQ directory
    fastq_dir = Path(fastq_dir)
    if not fastq_dir.is_dir():
        warnings.append(f"FASTQ directory not found: {fastq_dir}")
    else:
        r1_files = list(fastq_dir.glob('*R1_001.fastq.gz'))
        if not r1_files:
            warnings.append(f"No R1 FASTQ files found in: {fastq_dir}")
        
        # Check for matching R2 files
        for r1 in r1_files:
            r2 = r1.parent / r1.name.replace('R1', 'R2')
            if not r2.exists():
                warnings.append(f"No matching R2 file for: {r1.name}")

    return warnings

def load_results(results_dir: Union[str, Path]) -> Dict[str, pd.DataFrame]:
    """Load previously generated results from CSV files."""
    results_dir = Path(results_dir)
    results = {}
    
    for csv_file in results_dir.glob('*_haplotypes.csv'):
        sample_name = csv_file.stem.replace('_haplotypes', '')
        try:
            results[sample_name] = pd.read_csv(csv_file)
        except Exception as e:
            logger.error(f"Error loading results for {sample_name}: {str(e)}")
            continue
            
    return results