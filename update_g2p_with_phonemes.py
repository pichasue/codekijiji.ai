import re

# Function to convert graphemes to phonemes based on G2P mappings
def grapheme_to_phoneme(grapheme, g2p_mappings):
    # TODO: Implement the conversion logic based on the g2p_mappings
    # This is a placeholder function and needs to be filled in with actual logic
    return grapheme  # Placeholder return

# Function to add OOV words to the G2P mapping
def add_oov_to_g2p(oov_file, g2p_file):
    # Read the existing G2P mappings
    with open(g2p_file, "r") as file:
        g2p_mappings = file.readlines()

    # Extract the last index used in the G2P mappings
    last_index = int(re.search(r"(\d+)", g2p_mappings[-1]).group(1))

    # Read the OOV words
    with open(oov_file, "r") as file:
        oov_words = file.read().split(", ")

    # Remove duplicates and sort
    oov_words = sorted(set(oov_words))

    # Open the G2P file for appending
    with open(g2p_file, "a") as file:
        for word in oov_words:
            # Increment the index for each new word
            last_index += 1
            # Convert the grapheme to its phoneme representation
            phoneme = grapheme_to_phoneme(word, g2p_mappings)
            file.write(f"{last_index} {word} -> {phoneme}\n")

# File paths
oov_file_path = "/home/ubuntu/Documents/MFA/kikuyu/utterance_oovs.txt"
g2p_file_path = "/home/ubuntu/codekijiji.ai/kikuyu_g2p_mapping.txt"

# Update the G2P mapping with OOV words
add_oov_to_g2p(oov_file_path, g2p_file_path)

