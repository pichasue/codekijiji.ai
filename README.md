# Kikuyu TTS Interface

This project is focused on developing a Text-to-Speech (TTS) system for the Kikuyu language. It includes tools for aligning speech with text and generating synthetic speech from Kikuyu text.

## Getting Started with Gentle

Gentle is a robust yet lenient forced-aligner built on Kaldi, used as a tool for aligning speech with text.

### Installation

There are three ways to install Gentle:

1. Download the [pre-built Mac application](https://github.com/lowerquality/gentle/releases/latest). This package includes a GUI that will start the server and a browser. It only works on Mac OS.
2. Use the [Docker](https://www.docker.com/) image. Just run `docker run -P lowerquality/gentle`. This works on all platforms supported by Docker.
3. Download the source code and run `./install.sh`. Then run `python3 serve.py` to start the server. This works on Mac and Linux.

### Usage

By default, the aligner listens at http://localhost:8765. That page has a graphical interface for transcribing audio, viewing results, and downloading data.

There is also a REST API so you can use Gentle in your programs. Here's an example of how to use the API with CURL:

```bash
curl -F "audio=@audio.mp3" -F "transcript=@words.txt" "http://localhost:8765/transcriptions?async=false"
```

If you've downloaded the source code you can also run the aligner as a command line program:

```bash
git clone https://github.com/lowerquality/gentle.git
cd gentle
./install.sh
python3 align.py audio.mp3 words.txt
```

The default behaviour outputs the JSON to stdout. See `python3 align.py --help` for options.

## BibleTTS Project

The BibleTTS project aims to create TTS systems for various languages using the Bible as a dataset.

- [BibleTTS project website](https://masakhane-io.github.io/bibleTTS/)
- [Paper](https://arxiv.org/pdf/2207.03546.pdf)

### Links to code

#### Alignment methodology

1. [Segmentation using existing verse timestamps](https://github.com/coqui-ai/open-bible-scripts) (Sec 4.1.1)
2. [Forced alignment using pre-trained acoustic models](https://github.com/alpoktem/bible2speechDB) (Sec 4.1.2)
3. [Forced alignment from scratch](https://github.com/coqui-ai/open-bible-scripts) (Sec 4.1.3)

#### Outlier detection

- [Data-checker](https://github.com/coqui-ai/data-checker) code for outlier detection (Sec 4.2)

#### TTS model training

- VITS TTS models were trained with [coqui-ai](https://github.com/coqui-ai/TTS) (Sec 5)

## Project Update

As of the latest project developments, we have encountered significant challenges with the alignment of Kikuyu language audio files using Gentle. The alignment process resulted in a high number of unaligned words, which suggests that the tool may not be fully compatible with the phonetic characteristics of the Kikuyu language.

### Next Steps

- **Data Review**: We will conduct a thorough review of the audio files and the corresponding text data to ensure clarity and accuracy.
- **Tool Configuration**: We will explore the settings and configurations of the Gentle tool to determine if adjustments can improve alignment accuracy.
- **Expert Consultation**: We will seek advice from linguists or language model experts with experience in the Kikuyu language to gain insights into improving the alignment process.
- **Alternative Tools**: If necessary, we will explore alternative alignment tools or methods that may be better suited for the Kikuyu language.

The project's progress and any changes to the approach will be documented in subsequent updates to this README.
