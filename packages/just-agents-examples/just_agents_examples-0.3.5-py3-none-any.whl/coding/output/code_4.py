import requests
from pathlib import Path

# Define the UniProt URL for FGF2_HUMAN
uniprot_url = 'https://www.uniprot.org/uniprot/P08100.txt'

# Fetch the data
response = requests.get(uniprot_url)

# Check if the request was successful
if response.status_code == 200:
    # Save the content to a file
    with open('/output/FGF2.fasta', 'w') as fasta_file:
        fasta_file.write(response.text)
else:
    print('Failed to retrieve data from UniProt')