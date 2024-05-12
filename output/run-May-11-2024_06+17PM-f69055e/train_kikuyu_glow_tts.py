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
dataset_config = BaseDatasetConfig(formatter="ljspeech", meta_file_train="metadata.csv", path=dataset_path)

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
    phoneme_language='en-us',  # This should be changed to 'kikuyu' if a Kikuyu phoneme dictionary is available
    phoneme_cache_path=os.path.join(output_path, 'phoneme_cache'),
    num_speakers=1,  # Adjusted based on the documentation
    # Removed the gst_use_speaker_embedding parameter as it is not recognized
)

# Initialize the audio processor
ap = AudioProcessor.init_from_config(audio_config)

# Initialize the tokenizer
tokenizer, config = TTSTokenizer.init_from_config(config)

# Load data samples with the correct eval_split_size
train_samples, eval_samples = load_tts_samples(dataset_config, eval_split=True, eval_split_size=0.16666666666666666)

# Initialize the speaker manager for multi-speaker training
speaker_manager = SpeakerManager()
speaker_manager.set_ids_from_data(train_samples + eval_samples, parse_key="speaker_name")
config.num_speakers = speaker_manager.num_speakers

# Initialize the model
model = GlowTTS(config, ap, tokenizer, speaker_manager=speaker_manager)

# Initialize the trainer
trainer = Trainer(TrainerArgs(), config, output_path, model=model, train_samples=train_samples, eval_samples=eval_samples)

# Start training
trainer.fit()
