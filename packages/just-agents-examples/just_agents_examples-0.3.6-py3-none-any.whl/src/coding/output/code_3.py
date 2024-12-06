from Bio import ExPASy, SeqIO
from Bio import SwissProt
import random

# Search for FGF2_HUMAN in UniProt
search_term = 'FGF2_HUMAN'

# Fetch the UniProt entry
handle = ExPASy.get_sprot_raw(search_term)
record = SwissProt.read(handle)

# Extract the sequence
sequence = record.sequence

# Save the sequence in FASTA format
with open('/output/FGF2.fasta', 'w') as fasta_file:
    fasta_file.write(f'> {record.accession[0]}\n{sequence}')