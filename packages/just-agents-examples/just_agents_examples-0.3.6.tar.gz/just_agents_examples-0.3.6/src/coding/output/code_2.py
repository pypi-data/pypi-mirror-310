import GEOparse

gse = GEOparse.get_GEO(filepath='/input/GSE41781_family.soft.gz')

# Extract sample metadata
gsm_metadata = {}
for gsm_name, gsm in gse.gsms.items():
    gsm_metadata[gsm_name] = gsm.metadata

# Display metadata for inspection
for sample, metadata in gsm_metadata.items():
    print(f"Sample: {sample}")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    print("\n")