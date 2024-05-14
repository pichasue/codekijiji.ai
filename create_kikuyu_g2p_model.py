import pynini
from pynini.lib import pynutil
from pynini.examples import g2p

def create_g2p_model(mapping_file):
    with open(mapping_file, 'r') as file:
        mappings = file.readlines()

    # Create a FST that maps graphemes to phonemes
    g2p_fst = pynini.Fst()
    for mapping in mappings:
        grapheme, phoneme = mapping.strip().split(' -> ')
        g2p_fst |= pynini.cross(grapheme, phoneme)

    # Compile the FST into a G2P model
    g2p_model = g2p_fst.optimize()

    # Save the model
    g2p_model.write('kikuyu_g2p.fst')

    print("G2P model created and saved as 'kikuyu_g2p.fst'")

# Path to the grapheme-to-phoneme mapping file
mapping_file_path = 'kikuyu_g2p_mapping.txt'

# Create the G2P model
create_g2p_model(mapping_file_path)
