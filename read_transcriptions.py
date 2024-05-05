import pandas as pd

# Define the path to the formatted transcriptions CSV file
transcriptions_csv_path = '/home/ubuntu/codekijiji.ai/data/kikuyu/formatted_transcriptions.csv'

# Read the first few lines of the formatted transcriptions CSV file
transcriptions_df = pd.read_csv(transcriptions_csv_path, nrows=5)

# Print the first few lines to understand the structure and naming convention
print(transcriptions_df.head())
