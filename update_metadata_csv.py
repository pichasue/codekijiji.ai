import pandas as pd
import os
from pydub import AudioSegment

# Define the path to the formatted transcriptions CSV file
transcriptions_csv_path = '/home/ubuntu/codekijiji.ai/data/kikuyu/formatted_transcriptions.csv'
# Define the path to the metadata CSV file
metadata_csv_path = '/home/ubuntu/codekijiji.ai/kikuyu_bible_audio/metadata.csv'
# Define the path to the audio files
audio_files_path = '/home/ubuntu/codekijiji.ai/kikuyu_bible_audio/'

# Read the formatted transcriptions CSV file
transcriptions_df = pd.read_csv(transcriptions_csv_path)

# Ensure all values in the 'audio_filename' column are strings
transcriptions_df['audio_filename'] = transcriptions_df['audio_filename'].astype(str)

# Read the metadata CSV file
metadata_df = pd.read_csv(metadata_csv_path)

# Function to calculate audio length
def get_audio_length(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000  # length in seconds

# Update the metadata with the actual transcript data
for index, row in metadata_df.iterrows():
    # Extract the base filename without the extension
    base_filename = os.path.splitext(row['filename'])[0]
    # Find the transcript for the current filename
    transcript_row = transcriptions_df[transcriptions_df['audio_filename'] == base_filename]
    if not transcript_row.empty:
        # Update the transcript in the metadata
        metadata_df.at[index, 'transcript'] = transcript_row['transcription'].values[0]
        # Calculate and update the audio length
        audio_file_path = os.path.join(audio_files_path, row['filename'])
        if os.path.exists(audio_file_path):
            metadata_df.at[index, 'audio_length'] = get_audio_length(audio_file_path)
        else:
            print(f"Audio file not found: {audio_file_path}")
    else:
        print(f"Transcript not found for: {base_filename}")

# Save the updated metadata CSV file
metadata_df.to_csv(metadata_csv_path, index=False)

print(f"Metadata CSV file updated at {metadata_csv_path}")
