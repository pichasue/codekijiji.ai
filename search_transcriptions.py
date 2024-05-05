import pandas as pd

# Define the path to the formatted transcriptions CSV file
transcriptions_csv_path = '/home/ubuntu/codekijiji.ai/data/kikuyu/formatted_transcriptions.csv'

# Define the filename to search for
filename_to_search = "1CH_001"

print(f"Searching for filename: {filename_to_search}")

# Read the CSV file in chunks
chunk_size = 5000
chunk_number = 0
found = False  # Flag to indicate if the filename has been found
for chunk in pd.read_csv(transcriptions_csv_path, chunksize=chunk_size):
    chunk_number += 1
    print(f"Processing chunk {chunk_number}, size: {len(chunk)} rows")
    # Ensure the 'audio_filename' column is treated as a string
    chunk['audio_filename'] = chunk['audio_filename'].astype(str)
    # Search for the filename in the 'audio_filename' column
    matching_rows = chunk[chunk['audio_filename'].str.contains(filename_to_search, na=False)]
    if not matching_rows.empty:
        print(f"Found matching rows in chunk {chunk_number}:")
        print(matching_rows)
        found = True
        break  # Stop searching after finding the filename
    else:
        print(f"No matching rows found in chunk {chunk_number}.")

if not found:
    print(f"The filename {filename_to_search} was not found in any chunk.")
