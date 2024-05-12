from phonemizer import phonemize
from phonemizer.separator import Separator

# Sample Kikuyu text to be phonemized
sample_text = "Mũndũ wĩ mũtheri"

# Phonemize the sample text using the custom G2P mapping
# The custom G2P mapping should be provided as a file path directly in the command line
phonemized_text = phonemize(
    sample_text,
    language='en-us',  # Assuming 'en-us' as a placeholder
    backend='espeak',  # Using espeak backend
    separator=Separator(word='|', phone=' ', syllable='-')
)

print(f"Original text: {sample_text}")
print(f"Phonemized text: {phonemized_text}")
