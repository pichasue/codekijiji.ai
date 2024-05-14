import pandas as pd

# Define the path to the CSV file
csv_file_path = 'data/kikuyu/formatted_transcriptions.csv'

# Read the CSV file in chunks
chunk = pd.read_csv(csv_file_path, chunksize=5)

# Print the first chunk to inspect the headers and a few rows of data
print(next(chunk))
