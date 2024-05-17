#!flask/bin/python
import io
import json
import os
from pathlib import Path
from threading import Lock
from typing import Union
from urllib.parse import parse_qs

from functools import lru_cache
import cProfile  # Import cProfile for performance profiling
from flask import Flask, render_template, render_template_string, request, send_file
from flask_cors import CORS

from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import logging
import traceback
import time

# Removed CLI argument parsing to resolve conflict with Gunicorn
# Necessary configurations will be set within the file or through environment variables

# Placeholder values for configurations previously set by CLI arguments
model_name = "tts_models/en/ljspeech/tacotron2-DDC"
vocoder_name = None
config_path = None
model_path = None
vocoder_path = None
vocoder_config_path = None
speakers_file_path = None
port = 5000
use_cuda = False
debug = False
show_details = False

path = Path(__file__).parent / ".models.json"
manager = ModelManager(path)

# update in-use models to the specified released models.

# CASE2: load pre-trained model paths
if model_name is not None and not model_path:
    model_path, config_path, model_item = manager.download_model(model_name)
    vocoder_name = model_item["default_vocoder"] if vocoder_name is None else vocoder_name

if vocoder_name is not None and not vocoder_path:
    vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

# CASE3: set custom model paths
if model_path is not None:
    model_path = model_path
    config_path = config_path
    speakers_file_path = speakers_file_path

if vocoder_path is not None:
    vocoder_path = vocoder_path
    vocoder_config_path = vocoder_config_path

# load models
synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    tts_speakers_file=speakers_file_path,
    tts_languages_file=None,
    vocoder_checkpoint=vocoder_path,
    vocoder_config=vocoder_config_path,
    encoder_checkpoint="",
    encoder_config="",
    use_cuda=use_cuda,
)

use_multi_speaker = hasattr(synthesizer.tts_model, "num_speakers") and (
    synthesizer.tts_model.num_speakers > 1 or synthesizer.tts_speakers_file is not None
)
speaker_manager = getattr(synthesizer.tts_model, "speaker_manager", None)

use_multi_language = hasattr(synthesizer.tts_model, "num_languages") and (
    synthesizer.tts_model.num_languages > 1 or synthesizer.tts_languages_file is not None
)
language_manager = getattr(synthesizer.tts_model, "language_manager", None)

# TODO: set this from SpeakerManager
use_gst = synthesizer.tts_config.get("use_gst", False)
app = Flask(__name__)
CORS(app, origins=["https://clever-youtiao-1fec37.netlify.app"])

# Set up logging configuration to file and console
log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
log_file_handler = logging.FileHandler('/var/log/tts/tts_service.log')
log_file_handler.setFormatter(log_formatter)
log_console_handler = logging.StreamHandler()
log_console_handler.setFormatter(log_formatter)
logging.basicConfig(handlers=[log_file_handler, log_console_handler], level=logging.WARNING)
logging.warning('Logging system initialized at WARNING level.')

def style_wav_uri_to_dict(style_wav: str) -> Union[str, dict]:
    """Transform an uri style_wav, in either a string (path to wav file to be use for style transfer)
    or a dict (gst tokens/values to be use for styling)

    Args:
        style_wav (str): uri

    Returns:
        Union[str, dict]: path to file (str) or gst style (dict)
    """
    if style_wav:
        if os.path.isfile(style_wav) and style_wav.endswith(".wav"):
            return style_wav  # style_wav is a .wav file located on the server

        style_wav = json.loads(style_wav)
        return style_wav  # style_wav is a gst dictionary with {token1_id : token1_weigth, ...}
    return None

@app.route("/")
def index():
    return "TTS Service is running", 200

@app.route("/details")
def details():
    if config_path is not None and os.path.isfile(config_path):
        model_config = load_config(config_path)
    else:
        if model_name is not None:
            model_config = load_config(config_path)

    if vocoder_config_path is not None and os.path.isfile(vocoder_config_path):
        vocoder_config = load_config(vocoder_config_path)
    else:
        if vocoder_name is not None:
            vocoder_config = load_config(vocoder_config_path)
        else:
            vocoder_config = None

    return render_template(
        "details.html",
        show_details=show_details,
        model_config=model_config,
        vocoder_config=vocoder_config,
        args={"model_name": model_name, "vocoder_name": vocoder_name, "port": port, "use_cuda": use_cuda, "debug": debug, "show_details": show_details},
    )


lock = Lock()


@app.route("/api/tts", methods=["GET", "POST", "HEAD"])
def tts():
    start_time = time.time()  # Start timing the request processing
    logging.info('Entered the tts() function.')
    response = process_tts_request()
    end_time = time.time()  # End timing the request processing
    logging.info(f"Processed tts request in {end_time - start_time:.2f} seconds.")  # Log the processing time
    return response

# Removed redundant lru_cache decorators
@app.route("/api/tts", methods=["GET", "POST", "HEAD"])
def tts():
    start_time = time.time()  # Start timing the request processing
    logging.info('Entered the tts() function.')
    response = process_tts_request()
    end_time = time.time()  # End timing the request processing
    logging.info(f"Processed tts request in {end_time - start_time:.2f} seconds.")  # Log the processing time
    return response

def process_tts_request():
    profiler = cProfile.Profile()
    try:
        # HEAD requests do not have a body, skip processing
        if request.method == "HEAD":
            response = make_response('', 200)
        else:
            # Only process 'text' parameter for POST requests
            if request.method == "POST":
                data = request.get_json(silent=True)
                logging.info(f"Received data: {data}")
                if not data:
                    error_message = "No data provided in the request."
                    logging.error(error_message)
                    response = make_response({"error": error_message}, 400)
                elif 'text' not in data:
                    error_message = "The 'text' parameter is missing from the request."
                    logging.error(error_message)
                    response = make_response({"error": error_message}, 400)
                elif not data['text']:
                    error_message = "The 'text' parameter is empty."
                    logging.error(error_message)
                    response = make_response({"error": error_message}, 400)
                else:
                    text = data['text']
                    speaker_idx = request.headers.get("speaker-id") or request.values.get("speaker_id", "")
                    language_idx = request.headers.get("language-id") or request.values.get("language_id", "")
                    logging.info(f" > Model input: {text}")
                    logging.info(f" > Speaker Idx: {speaker_idx}")
                    logging.info(f" > Language Idx: {language_idx}")
                    style_wav = request.headers.get("style-wav") or request.values.get("style_wav", "")
                    style_wav = style_wav_uri_to_dict(style_wav)
                    logging.info(f" > Style Wav: {style_wav}")

                    # Profile the synthesizer.tts function call
                    profiler.enable()
                    wavs = synthesizer.tts(text, speaker_idx, language_idx, style_wav)
                    profiler.disable()
                    out = io.BytesIO()
                    synthesizer.save_wav(wavs, out)
                    profiler.dump_stats('/home/ubuntu/TTS/tts_profile.prof')  # Save profiling data to file
                    logging.info("Synthesis process completed successfully.")
                    response = make_response(send_file(out, mimetype="audio/wav"))
        # Removed manual CORS headers as they are now set in the after_request function
        return response
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(traceback.format_exc())
        response = make_response({"error": str(e)}, 500)
        # Removed manual CORS headers as they are now set in the after_request function
        return response


# Basic MaryTTS compatibility layer


@app.route("/locales", methods=["GET"])
def mary_tts_api_locales():
    """MaryTTS-compatible /locales endpoint"""
    # NOTE: We currently assume there is only one model active at the same time
    if model_name is not None:
        model_details = model_name.split("/")
    else:
        model_details = ["", "en", "", "default"]
    return render_template_string("{{ locale }}\n", locale=model_details[1])


@app.route("/voices", methods=["GET"])
def mary_tts_api_voices():
    """MaryTTS-compatible /voices endpoint"""
    # NOTE: We currently assume there is only one model active at the same time
    if model_name is not None:
        model_details = model_name.split("/")
    else:
        model_details = ["", "en", "", "default"]
    return render_template_string(
        "{{ name }} {{ locale }} {{ gender }}\n", name=model_details[3], locale=model_details[1], gender="u"
    )


@app.route("/process", methods=["GET", "POST"])
def mary_tts_api_process():
    """MaryTTS-compatible /process endpoint"""
    with lock:
        if request.method == "POST":
            data = parse_qs(request.get_data(as_text=True))
            # NOTE: we ignore param. LOCALE and VOICE for now since we have only one active model
            text = data.get("INPUT_TEXT", [""])[0]
        else:
            text = request.args.get("INPUT_TEXT", "")
        logging.info(f" > Model input: {text}")
        wavs = synthesizer.tts(text)
        out = io.BytesIO()
        synthesizer.save_wav(wavs, out)
        return send_file(out, mimetype="audio/wav")


@app.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint for ELB."""
    return "pong", 200

@app.after_request
def after_request(response):
    """Post-processing of the response to include CORS headers."""
    response.headers.add('Access-Control-Allow-Origin', 'https://clever-youtiao-1fec37.netlify.app')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    # Log the CORS headers for debugging purposes
    logging.info(f"CORS headers set: {response.headers}")
    return response

if __name__ == "__main__":
    app.run(debug=debug, host="0.0.0.0", port=port)
