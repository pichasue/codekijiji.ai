#!/bin/bash

# Iterate over all .webm files in the current directory
for file in *.webm; do
  # Extract the filename without the extension
  filename=$(basename "$file" .webm)
  # Convert the .webm file to .wav using ffmpeg
  ffmpeg -i "$file" -acodec pcm_s16le -ar 16000 "${filename}.wav"
done
