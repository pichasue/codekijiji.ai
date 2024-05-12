import requests

# Define the search query
search_query = 'Kikuyu language dataset for TTS'

# Google Search URL
google_search_url = 'https://www.google.com/search?q=' + search_query

# Perform the search
response = requests.get(google_search_url)

# Check if the request was successful
if response.status_code == 200:
    print('Search successful. Here are the results:')
    print(response.text)
else:
    print('Search failed with status code:', response.status_code)
