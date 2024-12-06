from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
from typing import List, Dict, Generator, Tuple
import logging
import shutil
from collections import Counter

import pysam
import pandas as pd
from Bio import SeqIO
from rich.progress import track

logger = logging.getLogger(__name__)

@dataclass
class AmpliconRead:
    """Represents a processed amplicon read pair."""
    sequence: str
    mutations: int
    quality: float

class AmpliconProcessor:
    """Main class for processing amplicon sequencing data."""
    
    def __init__(self, 
                 reference_path: Path,
                 min_base_quality: int = 20,
                 min_mapping_quality: int = 30,
                 max_file_size: int = 10_000_000_000):  # 10GB default
        """Initialize the processor with reference genome and quality parameters."""
        self.reference_path = Path(reference_path)
        self.min_base_quality = min_base_quality
        self.min_mapping_quality = min_mapping_quality
        self.max_file_size = max_file_size
        self.reference = self._load_reference()
        
        # Check for required executables
        self._check_dependencies()
        
    def _write_haplotypes_fasta(self, 
                               haplotypes: List[Dict],
                               output_path: Path):
        """Write haplotypes to a FASTA file.
        
        Args:
            haplotypes: List of dictionaries containing haplotype information
            output_path: Path to write the FASTA file
        """
        with open(output_path, 'w') as fasta_out:
            for entry in haplotypes:
                header = f"{entry['reference']}_{entry['count']}"
                sequence = entry['haplotype']
                fasta_out.write(f">{header}\n{sequence}\n")

    def _check_dependencies(self):
        """Check if required external programs are available."""
        for cmd in ['bwa', 'samtools']:
            if not shutil.which(cmd):
                raise RuntimeError(f"{cmd} not found in PATH. Please install {cmd}.")
    
    def _load_reference(self) -> Dict[str, str]:
        """Load reference sequences."""
        return {record.id: str(record.seq) 
                for record in SeqIO.parse(self.reference_path, "fasta")}

    def _align_reads(self, 
                     fastq_r1: Path,
                     fastq_r2: Path, 
                     temp_dir: Path,
                     output_dir: Path,
                     threads: int) -> Path:
        """Align reads using BWA-MEM and convert to sorted BAM."""
        sample_name = fastq_r1.stem.replace("_R1_001.fastq", "")
        temp_sam = temp_dir / f"{sample_name}.sam"
        temp_bam = temp_dir / f"{sample_name}.temp.bam"
        final_bam = output_dir / f"{sample_name}.bam"
        
        try:
            # Check input file sizes
            total_size = fastq_r1.stat().st_size + fastq_r2.stat().st_size
            if total_size > self.max_file_size:
                raise ValueError(f"Input files too large: {total_size} bytes")
            
            # Run BWA-MEM
            bwa_cmd = [
                'bwa', 'mem',
                '-t', str(threads),
                str(self.reference_path),
                str(fastq_r1),
                str(fastq_r2)
            ]
            
            with open(temp_sam, 'w') as sam_out:
                logger.debug(f"Running BWA: {' '.join(bwa_cmd)}")
                process = subprocess.run(
                    bwa_cmd,
                    stdout=sam_out,
                    stderr=subprocess.PIPE,
                    check=True
                )
            
            # Convert SAM to BAM
            logger.debug("Converting SAM to BAM")
            subprocess.run(
                ['samtools', 'view', '-b', '-@', str(threads), '-o', str(temp_bam), str(temp_sam)],
                check=True,
                stderr=subprocess.PIPE
            )
            
            # Sort BAM with explicit temp directory and memory limit
            logger.debug("Sorting BAM file")
            subprocess.run(
                [
                    'samtools', 'sort',
                    '-@', str(threads),
                    '-m', '1G',  # Memory per thread
                    '-T', str(temp_dir / f"{sample_name}.sort"),
                    '-o', str(final_bam),
                    str(temp_bam)
                ],
                check=True,
                stderr=subprocess.PIPE
            )
            
            # Index BAM
            logger.debug("Indexing BAM file")
            subprocess.run(
                ['samtools', 'index', str(final_bam)],
                check=True,
                stderr=subprocess.PIPE
            )
            
            return final_bam
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            raise RuntimeError(f"Alignment failed: {error_msg}")
        except Exception as e:
            raise RuntimeError(f"Alignment failed: {str(e)}")
        finally:
            # Cleanup temporary files
            for temp_file in [temp_sam, temp_bam]:
                try:
                    if temp_file.exists():
                        temp_file.unlink()
                except:
                    pass
    
    def _process_alignments(self, 
                          bam_path: Path,
                          ref_name: str) -> Generator[AmpliconRead, None, None]:
        """Process aligned reads for a reference sequence."""
        bam = None
        try:
            bam = pysam.AlignmentFile(bam_path, "rb")
            ref_seq = self.reference[ref_name]
            
            read_count = 0
            for read1, read2 in self._get_read_pairs(bam, ref_name):
                if not (read1 and read2):
                    continue
                    
                sequence = self._reconstruct_sequence(read1, read2, ref_seq)
                mutations = sum(1 for base in sequence if base.islower())
                quality = (read1.mapping_quality + read2.mapping_quality) / 2
                
                read_count += 1
                yield AmpliconRead(sequence, mutations, quality)
            
            if read_count == 0:
                logger.warning(f"No valid read pairs found for {ref_name}")
                
        except Exception as e:
            logger.error(f"Error processing alignments for {ref_name}: {str(e)}")
            raise
        finally:
            if bam:
                try:
                    bam.close()
                except:
                    pass

    def _get_read_pairs(self, 
                       bam: pysam.AlignmentFile,
                       ref_name: str) -> Generator[Tuple[pysam.AlignedSegment, pysam.AlignedSegment], None, None]:
        """Generate properly paired reads."""
        reads = {}
        for read in bam.fetch(ref_name):
            if (not read.is_proper_pair or 
                read.is_secondary or 
                read.is_supplementary or 
                read.mapping_quality < self.min_mapping_quality):
                continue
                
            qname = read.query_name
            if qname in reads:
                pair = reads.pop(qname)
                yield (read, pair) if read.is_read1 else (pair, read)
            else:
                reads[qname] = read
    
    def _reconstruct_sequence(self,
                            read1: pysam.AlignedSegment,
                            read2: pysam.AlignedSegment,
                            ref_seq: str) -> str:
        """Reconstruct the amplicon sequence from paired reads."""
        sequence = list(ref_seq.upper())  # Normalize reference sequence
        
        for read in (read1, read2):
            for qpos, rpos in read.get_aligned_pairs(matches_only=True):
                if (read.query_qualities[qpos] >= self.min_base_quality and
                    rpos < len(sequence)):
                    base = read.query_sequence[qpos].upper()  # Normalize query sequence
                    if base != ref_seq[rpos].upper():  # Compare normalized sequences
                        sequence[rpos] = base.lower()
                    else:
                        sequence[rpos] = base.upper()
        
        return ''.join(sequence)
    def _analyze_amplicons(self,
                          amplicon_reads: List[AmpliconRead],
                          ref_name: str) -> List[Dict]:
        """Analyze processed amplicon reads."""
        results = []
        
        if not amplicon_reads:
            logger.warning(f"No valid reads found for reference {ref_name}")
            return results
        
        # Count haplotypes
        haplotype_counts = Counter(read.sequence for read in amplicon_reads)
        total_reads = sum(haplotype_counts.values())
        
        # Count single mutations
        ref_seq = self.reference[ref_name].upper()
        single_mutation_count = 0
        possible_single_mutations = len(ref_seq) * 3  # each position can mutate to 3 other bases
        
        # Analyze each haplotype
        for haplotype, count in haplotype_counts.most_common():
            frequency = count / total_reads
            mutations = sum(1 for base in haplotype if base.islower())
            
            # Check if this is a single mutation haplotype
            if mutations == 1:
                single_mutation_count += 1
                
            results.append({
                'reference': ref_name,
                'haplotype': haplotype,
                'count': count,
                'frequency': frequency,
                'mutations': mutations
            })
        
        # Add summary statistics
        if results:  # Only add if we have results
            results[0].update({
                'single_mutations': single_mutation_count,
                'possible_single_mutations': possible_single_mutations,
                'single_mutation_coverage': single_mutation_count / possible_single_mutations
            })
        
        return results

    def _write_single_mutation_fasta(self,
                                   haplotypes: List[Dict],
                                   output_path: Path):
        """Write single-mutation haplotypes to a FASTA file."""
        with open(output_path, 'w') as fasta_out:
            for entry in haplotypes:
                if entry['mutations'] == 1:  # Only write sequences with exactly one mutation
                    header = f"{entry['reference']}_count{entry['count']}"
                    sequence = entry['haplotype']
                    fasta_out.write(f">{header}\n{sequence}\n")

    def process_sample(self, 
                      fastq_r1: Path,
                      fastq_r2: Path,
                      output_dir: Path,
                      threads: int = 4) -> pd.DataFrame:
        """Process a single sample's FASTQ files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)
            
            try:
                # Align reads
                bam_path = self._align_reads(fastq_r1, fastq_r2, temp_dir, output_dir, threads)
                
                # Process alignments
                results = []
                for ref_name in self.reference:
                    amplicon_reads = list(self._process_alignments(bam_path, ref_name))
                    if amplicon_reads:
                        results.extend(self._analyze_amplicons(amplicon_reads, ref_name))
                    else:
                        logger.warning(f"No valid reads found for reference {ref_name}")
                
                if not results:
                    return pd.DataFrame(columns=['reference', 'haplotype', 'count', 'frequency', 'mutations'])
                
                # Write haplotypes to FASTA files
                sample_name = fastq_r1.stem.replace("_R1_001.fastq", "")
                fasta_path = output_dir / f"{sample_name}_haplotypes.fasta"
                single_mut_fasta_path = output_dir / f"{sample_name}_single_mutations.fasta"
                
                self._write_haplotypes_fasta(results, fasta_path)
                self._write_single_mutation_fasta(results, single_mut_fasta_path)
                    
                return pd.DataFrame(results)
                
            except Exception as e:
                logger.error(f"Error processing sample: {str(e)}")
                return pd.DataFrame(columns=['reference', 'haplotype', 'count', 'frequency', 'mutations'])