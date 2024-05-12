import os
from TTS.config.shared_configs import BaseAudioConfig
from TTS.tts.configs.glow_tts_config import GlowTTSConfig
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.glow_tts import GlowTTS
from TTS.tts.utils.speakers import SpeakerManager
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor
from trainer import Trainer, TrainerArgs

# Define the path to the dataset and output
dataset_path = '/home/ubuntu/codekijiji.ai/data/kikuyu'
output_path = '/home/ubuntu/codekijiji.ai/models/kikuyu_glow_tts'

# Define dataset config
# Custom formatter function to handle the metadata file format
def custom_formatter(file_path, text, **kwargs):
    # Assuming the metadata file has the format: "filename.wav|transcript|"
    # and the audio files are located in the dataset_path directory.
    # The file_path and text are now directly provided as arguments to the function.
    if not file_path or not text:
        # Log an error if file_path or text is missing and return None
        error_message = f"Error in custom_formatter: file_path or text is missing for line: {file_path}|{text}"
        print(error_message)
        return None
    # Construct the full file path
    file_path = os.path.join(dataset_path, file_path.strip())
    # Construct the dictionary to be returned
    formatted_dict = {'audio_file': file_path, 'text': text.strip(), 'speaker_name': 'default'}
    # Debug: Log the constructed dictionary before returning
    print(f"Debug: Returning from custom_formatter: {formatted_dict}")
    return formatted_dict

# Load the metadata file and create the 'items' key in the dataset_config
metadata_file_path = os.path.join(dataset_path, "metadata.csv")
with open(metadata_file_path, 'r') as metadata_file:
    # Process each line in the metadata file with the custom_formatter to create a list of dictionaries
    items = [item for item in (custom_formatter(*line.strip().split('|')[:2]) for line in metadata_file) if item is not None]
    # Add a check to ensure each item is a dictionary
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {i} is not a dictionary. Item content: {item}")

# Debugging: Print the type and content of each item in the 'items' list
for i, item in enumerate(items):
    print(f"Item {i} type: {type(item)}, content: {item}")

# Debugging: Print the entire 'items' list before it is passed to the load_tts_samples function
print(f"Items list before load_tts_samples: {items}")

# Pass the custom formatter function directly to the BaseDatasetConfig
# The 'items' key is removed from here as it is not expected by BaseDatasetConfig
dataset_config = BaseDatasetConfig(formatter=custom_formatter, meta_file_train="metadata.csv", path=dataset_path)

# Define audio config
audio_config = BaseAudioConfig(sample_rate=16000)

# Define model config
config = GlowTTSConfig(
    # Add all necessary configurations specific to the Kikuyu dataset and training requirements
    batch_size=32,
    eval_batch_size=16,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=10,
    epochs=1000,
    text_cleaner='phoneme_cleaners',
    use_phonemes=True,
    phoneme_language='en-us',  # Placeholder for phonemizer support
    phoneme_cache_path=os.path.join(output_path, 'phoneme_cache'),
    num_speakers=1,  # Adjusted based on the documentation
)

# Initialize the audio processor
ap = AudioProcessor.init_from_config(audio_config)

# Ensure the custom formatter is callable before passing it to load_tts_samples
assert callable(custom_formatter), "The custom_formatter must be a callable function"
# Debug: Print the type and value of custom_formatter before passing to load_tts_samples
print(f"Debug: custom_formatter type: {type(custom_formatter)}, value: {custom_formatter}")

# Debugging: Print the type and content of each item in the 'items' list before passing to load_tts_samples
for i, item in enumerate(items):
    print(f"Debug before load_tts_samples - Item {i} type: {type(item)}, content: {item}")

# Debug: Print the dictionary being passed to load_tts_samples to confirm structure
print(f"Debug: Dictionary passed to load_tts_samples: {{'items': {items}, 'formatter': {custom_formatter}, 'dataset_name': 'kikuyu_dataset', 'path': {dataset_path}, 'meta_file_train': 'metadata.csv', 'meta_file_val': 'metadata.csv', 'ignored_speakers': [], 'language': 'kik'}}")

# Load data samples with the correct eval_split_size
train_samples, eval_samples = load_tts_samples({'items': items, 'formatter': custom_formatter, 'dataset_name': 'kikuyu_dataset', 'path': dataset_path, 'meta_file_train': 'metadata.csv', 'meta_file_val': 'metadata.csv', 'ignored_speakers': [], 'language': 'kik'}, eval_split=True, eval_split_size=0.2)

# Initialize the speaker manager for multi-speaker training
speaker_manager = SpeakerManager()
speaker_manager.set_ids_from_data(train_samples + eval_samples, parse_key="speaker_name")
config.num_speakers = speaker_manager.num_speakers

# Load the custom G2P mapping from the file and update the config object
g2p_mapping_path = '/home/ubuntu/codekijiji.ai/kikuyu_g2p_mapping.txt'
with open(g2p_mapping_path, 'r') as g2p_file:
    g2p_mapping = {line.split(' -> ')[0]: line.split(' -> ')[1].strip() for line in g2p_file.readlines()}
config.g2p_mapping = g2p_mapping  # Add the custom G2P mapping to the config object
tokenizer, config = TTSTokenizer.init_from_config(config)  # Initialize the tokenizer with the updated config

# Initialize the model
model = GlowTTS(config, ap, tokenizer, speaker_manager=speaker_manager)

# Initialize the trainer
trainer = Trainer(TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples)

# Start training
trainer.fit()
