# CloneArmy

CloneArmy is a modern Python package for analyzing haplotypes from Illumina paired-end amplicon sequencing data. It provides a streamlined workflow for processing FASTQ files, aligning reads, and identifying sequence variants.

## Features

- Fast paired-end read processing using BWA-MEM
- Quality-based filtering of bases and alignments
- Haplotype identification and frequency analysis
- Rich command-line interface with progress tracking
- Comprehensive output reports
- Multi-threading support

## Installation

```bash
pip install cloneArmy
```

### Requirements

- Python ≥ 3.8
- BWA (must be installed and available in PATH)
- Samtools (must be installed and available in PATH)

## Usage

### Command Line Interface

```bash
# Basic usage
cloneArmy /path/to/fastq/directory reference.fasta

# With all options
cloneArmy /path/to/fastq/directory reference.fasta \
    --threads 8 \
    --output results \
    --min-base-quality 20 \
    --min-mapping-quality 30
```

### Python API

```python
from pathlib import Path
from clone_army.processor import AmpliconProcessor

# Initialize processor
processor = AmpliconProcessor(
    reference_path="reference.fasta",
    min_base_quality=20,
    min_mapping_quality=30
)

# Process a single sample
results = processor.process_sample(
    fastq_r1="sample_R1.fastq.gz",
    fastq_r2="sample_R2.fastq.gz",
    output_dir="results",
    threads=4
)

# Results are returned as a pandas DataFrame
print(results)
```

## Output

For each sample, CloneArmy generates:
- A sorted BAM file with alignments
- A CSV file containing haplotype information:
  - Sequence
  - Read count
  - Frequency
  - Number of mutations
- Console output


