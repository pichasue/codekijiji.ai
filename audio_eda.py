import os
import wave
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# Directory containing the audio files
audio_dir = '/home/ubuntu/codekijiji.ai/data/kikuyu'

# Lists to store audio properties and filenames
durations = []
frame_rates = []
n_channels_list = []
filenames = []

# Iterate over all .wav files in the audio directory
for filename in os.listdir(audio_dir):
    if filename.endswith('.wav'):
        # Append the filename to the filenames list
        filenames.append(filename)

        # Open the .wav file
        with wave.open(os.path.join(audio_dir, filename), 'rb') as wave_file:
            # Get audio parameters
            n_channels = wave_file.getnchannels()
            sample_width = wave_file.getsampwidth()
            frame_rate = wave_file.getframerate()
            n_frames = wave_file.getnframes()
            duration = n_frames / float(frame_rate)

            # Append properties to lists
            durations.append(duration)
            frame_rates.append(frame_rate)
            n_channels_list.append(n_channels)

            # Print audio file properties
            print(f"File: {filename}")
            print(f"Number of Channels: {n_channels}")
            print(f"Sample Width: {sample_width}")
            print(f"Frame Rate (Sample Rate): {frame_rate}")
            print(f"Number of Frames: {n_frames}")
            print(f"Duration (seconds): {duration:.2f}")
            print("-" * 40)

# Create a DataFrame from the audio properties
audio_df = pd.DataFrame({
    'Filename': filenames,
    'Duration': durations,
    'Frame Rate': frame_rates,
    'Channels': n_channels_list
})

# Calculate summary statistics for audio durations
duration_stats = audio_df['Duration'].describe()

# Print summary statistics
print("Summary Statistics for Audio Durations:")
print(duration_stats)

# Plot the distribution of audio durations using Plotly
fig_duration = px.histogram(audio_df, x='Duration', title='Distribution of Audio Durations')
fig_duration.write_html('/home/ubuntu/codekijiji.ai/data/kikuyu/audio_durations_histogram_interactive.html')

# Plot the distribution of frame rates using Plotly
fig_frame_rate = px.histogram(audio_df, x='Frame Rate', title='Distribution of Frame Rates')
fig_frame_rate.write_html('/home/ubuntu/codekijiji.ai/data/kikuyu/frame_rates_histogram_interactive.html')

# Plot the distribution of channels using Plotly
fig_channels = px.histogram(audio_df, x='Channels', title='Distribution of Channels')
fig_channels.write_html('/home/ubuntu/codekijiji.ai/data/kikuyu/channels_histogram_interactive.html')
