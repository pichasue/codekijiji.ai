import os

# Directory containing the audio and text files
directory = '/home/ubuntu/codekijiji.ai/data/kikuyu/'

# Output metadata file
metadata_file = directory + 'metadata.csv'

# Clear the metadata file content
open(metadata_file, 'w').close()

# Iterate over all .txt files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        # Construct the full path to the text file
        text_file_path = os.path.join(directory, filename)
        # Read the transcript from the text file
        with open(text_file_path, 'r') as text_file:
            transcript = text_file.read().strip()
        # Construct the corresponding .wav filename
        wav_filename = filename.replace('.txt', '.wav')
        # Write the metadata entry
        with open(metadata_file, 'a') as meta_file:
            meta_file.write(f'{wav_filename}|{transcript}\n')
