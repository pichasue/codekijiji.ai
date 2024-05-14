import csv
import os

# Define the directory where the files are located
data_dir = '/home/ubuntu/codekijiji.ai/data/kikuyu'

# Define the path to the metadata.csv file
metadata_csv_path = os.path.join(data_dir, 'metadata.csv')

# Function to check if a file exists and is not empty
def check_file_exists_and_not_empty(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

# Read the metadata.csv file and perform checks
with open(metadata_csv_path, mode='r', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter='|')
    for row in csv_reader:
        audio_file = row['filename']
        transcript_file = row['transcript']

        # Check if the audio file exists and is a WAV file
        audio_file_path = os.path.join(data_dir, audio_file)
        if not check_file_exists_and_not_empty(audio_file_path) or not audio_file.endswith('.wav'):
            print(f"Audio file issue: {audio_file_path}")

        # Check if the transcript file exists and is not empty
        transcript_file_path = os.path.join(data_dir, transcript_file)
        if not check_file_exists_and_not_empty(transcript_file_path):
            print(f"Transcript file issue: {transcript_file_path}")

print("Dataset verification complete.")
