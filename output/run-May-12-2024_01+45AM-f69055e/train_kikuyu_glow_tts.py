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
def custom_formatter(file_path, text, *args, **kwargs):
    # Assuming the metadata file has the format: "filename.wav|transcript|"
    # and the audio files are located in the dataset_path directory.
    # Remove the '.wav' extension from file_path if it exists to prevent duplication
    if file_path.endswith('.wav'):
        file_path = file_path[:-4]
    file_path = os.path.join(dataset_path, file_path + '.wav')
    text = text.strip('|')
    # Return a dictionary as expected by the add_extra_keys function
    return {'audio_file': file_path, 'text': text, 'speaker_name': 'default'}

# Pass the custom formatter function directly to the BaseDatasetConfig
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

# Load data samples with the correct eval_split_size
# Ensure that the formatter is not retrieved by name by not passing a 'formatter' key in the dataset dictionary
# Explicitly pass the custom formatter to the load_tts_samples function
# Load the metadata file and create the 'items' key in the dataset_config
metadata_file_path = os.path.join(dataset_path, dataset_config.meta_file_train)
with open(metadata_file_path, 'r') as metadata_file:
    # Process each line in the metadata file with the custom_formatter to create a list of dictionaries
    items = [custom_formatter(*line.strip().split('|')) for line in metadata_file]
    # Add a check to ensure each item is a dictionary
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {i} is not a dictionary. Item content: {item}")

# Debugging: Print the type and content of each item in the 'items' list
for i, item in enumerate(items):
    print(f"Item {i} type: {type(item)}, content: {item}")

# Debugging: Print the entire 'items' list before it is passed to the load_tts_samples function
print(f"Items list before load_tts_samples: {items}")
dataset_config.items = items  # Add the 'items' key with the loaded metadata to the dataset_config

# Ensure the custom formatter is callable before passing it to load_tts_samples
assert callable(custom_formatter), "The custom_formatter must be a callable function"

# Pass the custom formatter directly to the load_tts_samples function
train_samples, eval_samples = load_tts_samples(dataset_config, eval_split=True, eval_split_size=0.16666666666666666, formatter=custom_formatter)

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
