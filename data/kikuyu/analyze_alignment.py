import json

def analyze_alignment(file_path):
    # Initialize counters
    total_words = 0
    unaligned_words_count = 0
    unaligned_words_details = []

    # Open and read the alignment.json file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Parse the JSON data
    for word in data['words']:
        total_words += 1
        if word['case'] == 'not-found-in-audio':
            unaligned_words_count += 1
            unaligned_words_details.append(word['word'])

    # Print summary
    print(f"Total words: {total_words}")
    print(f"Unaligned words: {unaligned_words_count}")

    # Save the summary and unaligned words to a new file
    with open('alignment_summary.txt', 'w') as summary_file:
        summary_file.write(f"Total words: {total_words}\n")
        summary_file.write(f"Unaligned words: {unaligned_words_count}\n")
        summary_file.write("Unaligned words details:\n")
        for word in unaligned_words_details:
            summary_file.write(f"{word}\n")

    print("Analysis complete. Summary saved to alignment_summary.txt")

# Path to the alignment.json file
alignment_file_path = '/home/ubuntu/codekijiji.ai/data/kikuyu/alignment.json'

# Run the analysis
analyze_alignment(alignment_file_path)
