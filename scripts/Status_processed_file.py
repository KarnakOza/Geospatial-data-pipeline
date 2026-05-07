import os

# folders
input_folder = r"H:\GEOSPATIAL_PIPELINE\raw_sar"
output_folder = r"G:\Project\output"

# input SAR files
input_files = [
    os.path.splitext(f)[0]
    for f in os.listdir(input_folder)
    if f.endswith(".zip")
]

output_files = [
    os.path.splitext(f)[0].replace("_processed", "")
    for f in os.listdir(output_folder)
    if f.endswith(".tif")
]

# comparison
processed = set(input_files) & set(output_files)
not_processed = set(input_files) - set(output_files)

print("\nProcessed Files:")
for f in sorted(processed):
    print("✓", f)

print("\nNot Processed Files:")
for f in sorted(not_processed):
    print("✗", f)
