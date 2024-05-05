import pandas as pd

# Define the paths to the CSV files
metadata_csv_path = '/home/ubuntu/codekijiji.ai/kikuyu_bible_audio/metadata.csv'
transcriptions_csv_path = '/home/ubuntu/codekijiji.ai/data/kikuyu/formatted_transcriptions.csv'

# Read the CSV files
metadata_df = pd.read_csv(metadata_csv_path)
transcriptions_df = pd.read_csv(transcriptions_csv_path)

# Get the list of filenames from both CSV files
metadata_filenames = metadata_df['filename'].apply(lambda x: x.split('.')[0]).tolist()
transcriptions_filenames = transcriptions_df['audio_filename'].apply(lambda x: x.split('.')[0]).tolist()

# Find filenames in metadata that are not in transcriptions
missing_in_transcriptions = set(metadata_filenames) - set(transcriptions_filenames)

# Find filenames in transcriptions that are not in metadata
missing_in_metadata = set(transcriptions_filenames) - set(metadata_filenames)

# Print the results
print(f"Filenames in metadata.csv not found in formatted_transcriptions.csv: {missing_in_transcriptions}")
print(f"Filenames in formatted_transcriptions.csv not found in metadata.csv: {missing_in_metadata}")
