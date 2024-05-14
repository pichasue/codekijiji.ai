from montreal_forced_aligner.alignment.pretrained import PretrainedAligner

# Define the paths to the necessary files and directories
corpus_directory = '/home/ubuntu/codekijiji.ai/data/kikuyu'  # Directory containing the audio files and their transcriptions
dictionary_path = '/home/ubuntu/codekijiji.ai/kikuyu_g2p_mapping.txt'  # Path to the pronunciation dictionary
acoustic_model_path = '/home/ubuntu/codekijiji.ai/swahili_mfa'  # Path to the pre-trained acoustic model directory
output_directory = '/home/ubuntu/codekijiji.ai/data/kikuyu/aligned_output'  # Directory where the aligned output will be saved

# Perform forced alignment using the PretrainedAligner class
aligner = PretrainedAligner(
    corpus_directory=corpus_directory,
    dictionary_path=dictionary_path,
    acoustic_model_path=acoustic_model_path,
    output_directory=output_directory,
    clean=True,
    verbose=True
)
aligner.align()
