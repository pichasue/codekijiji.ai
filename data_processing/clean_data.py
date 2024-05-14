import librosa
import pydub
import numpy as np
import soundfile as sf

def clean_data(data):
    """
    Cleans the input data by removing unwanted noise and non-speech elements.

    Parameters:
    data (list of dict): The input data to clean, each entry is a dictionary representing a single audio file and its metadata.

    Returns:
    list of dict: The cleaned data.
    """
    cleaned_data = []

    for entry in data:
        # Load the audio file
        audio_path = entry['audio']
        y, sr = librosa.load(audio_path, sr=None)

        # Remove silence
        non_silent_intervals = librosa.effects.split(y, top_db=30)
        non_silent_audio = np.concatenate([y[start:end] for start, end in non_silent_intervals])

        # Save the cleaned audio to a temporary file
        temp_audio_path = audio_path.replace('.wav', '_cleaned.wav')
        sf.write(temp_audio_path, non_silent_audio, sr)

        # Update the entry with the path to the cleaned audio
        entry['audio'] = temp_audio_path
        cleaned_data.append(entry)

    return cleaned_data

# Placeholder for testing the clean_data function
if __name__ == "__main__":
    # Example data format
    example_data = [
        {'audio': '/home/ubuntu/codekijiji.ai/data/kikuyu/recording-1715062066291.wav', 'metadata': {'text': 'example text 1'}},
        {'audio': '/home/ubuntu/codekijiji.ai/data/kikuyu/recording-1715191505661.wav', 'metadata': {'text': 'example text 2'}}
    ]

    # Call the clean_data function with example data
    cleaned_example_data = clean_data(example_data)
    print("Cleaned Data:", cleaned_example_data)
