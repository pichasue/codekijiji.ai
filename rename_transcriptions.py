import pandas as pd
import re

# Define the paths to the CSV files
metadata_csv_path = '/home/ubuntu/codekijiji.ai/kikuyu_bible_audio/metadata.csv'
transcriptions_csv_path = '/home/ubuntu/codekijiji.ai/data/kikuyu/formatted_transcriptions.csv'

# Read the CSV files
metadata_df = pd.read_csv(metadata_csv_path)
transcriptions_df = pd.read_csv(transcriptions_csv_path)

# Create a mapping of the filenames from formatted_transcriptions.csv to the expected filenames in metadata.csv
# The mapping will be a dictionary where the key is the current filename and the value is the new filename
filename_mapping = {}

# Regex pattern to extract the book name and chapter number from the formatted_transcriptions.csv filenames
# Updated pattern to match filenames like 'ISA_026'
pattern = re.compile(r'(\w{3})_(\d{3})')

# Additional patterns for filenames that do not match the expected pattern
# These patterns are based on the observed discrepancies
additional_patterns = {
    re.compile(r'recording-\d+(_cleaned)?\.wav'): 'GEN_001',  # Assuming 'GEN_001' as a placeholder for these recordings
    # Removed the previous additional pattern as it is now covered by the updated main pattern
}

# Iterate over the rows in the transcriptions DataFrame
for index, row in transcriptions_df.iterrows():
    # Ensure the audio_filename is a string before processing
    current_filename = str(row['audio_filename'])
    # Skip rows with NaN values or non-matching patterns
    if current_filename.lower() == 'nan':
        print(f"Skipping NaN value at index {index}")
        continue
    # Use regex to extract the book name and chapter number
    match = pattern.match(current_filename)
    if match:
        # Construct the new filename using the extracted book name and chapter number
        new_filename = f"{match.group(1).upper()}_{int(match.group(2)):03d}"
        # Add the mapping to the filename_mapping dictionary
        filename_mapping[current_filename] = new_filename
    else:
        # Check additional patterns
        for additional_pattern, replacement in additional_patterns.items():
            additional_match = additional_pattern.match(current_filename)
            if additional_match:
                if callable(replacement):
                    new_filename = replacement(additional_match)
                else:
                    new_filename = replacement
                filename_mapping[current_filename] = new_filename
                break
        else:
            print(f"Filename does not match expected pattern: {current_filename}")

# Use the mapping to rename the filenames in the transcriptions DataFrame
transcriptions_df['audio_filename'] = transcriptions_df['audio_filename'].map(filename_mapping)

# Save the updated formatted_transcriptions.csv
transcriptions_df.to_csv(transcriptions_csv_path, index=False)

print("Filenames in formatted_transcriptions.csv have been updated.")
