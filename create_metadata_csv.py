import xml.etree.ElementTree as ET
import csv

# Define the path to the metadata.xml file
metadata_xml_path = '/home/ubuntu/codekijiji.ai/kikuyu_bible_audio/metadata.xml'
# Define the path for the new metadata.csv file
metadata_csv_path = '/home/ubuntu/codekijiji.ai/kikuyu_bible_audio/metadata.csv'

# Parse the XML file
tree = ET.parse(metadata_xml_path)
root = tree.getroot()

# Open the CSV file for writing
with open(metadata_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
    # Define the CSV writer
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Write the header row
    csv_writer.writerow(['filename', 'transcript', 'speaker_id', 'audio_length'])

    # Iterate over each resource in the XML file
    for resource in root.findall('.//resource'):
        # Extract the uri attribute which contains the filename
        uri = resource.get('uri')
        # Extract the filename from the uri
        filename = uri.split('/')[-1]
        # Placeholder values for transcript and speaker_id
        transcript = 'Unknown'  # This should be updated with actual transcript data if available
        speaker_id = 'default'  # This should be updated if speaker information is available
        # Placeholder for audio_length
        audio_length = 'Unknown'  # This should be calculated from the audio file if necessary

        # Write the row to the CSV file
        csv_writer.writerow([filename, transcript, speaker_id, audio_length])

print(f"Metadata CSV file created at {metadata_csv_path}")
