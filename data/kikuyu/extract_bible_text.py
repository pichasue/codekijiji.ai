import csv
from bs4 import BeautifulSoup
import requests

# Define the URL for Genesis 1 in the Kikuyu language on the STEP Bible website
url = 'https://www.stepbible.org/?q=version=KikGKY|reference=Gen.1'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the verse elements
    verses = soup.find_all('span', {'class': 'verse'})
    
    # Open a CSV file to write the verses
    with open('genesis_chapter_1.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Verse', 'Text'])
        
        # Write each verse number and text to the CSV file
        for verse in verses:
            verse_number = verse.find('span', {'class': 'verseNumber'}).get_text(strip=True)
            verse_text = verse.get_text(strip=True).replace(verse_number, '')
            writer.writerow([verse_number, verse_text])
else:
    print('Failed to retrieve the webpage content.')
