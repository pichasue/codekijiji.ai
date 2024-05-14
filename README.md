# Gentle
**Robust yet lenient forced-aligner built on Kaldi. A tool for aligning speech with text.**

## Getting Started

There are three ways to install Gentle.

1. Download the [pre-built Mac application](https://github.com/lowerquality/gentle/releases/latest). This package includes a GUI that will start the server and a browser. It only works on Mac OS.

2. Use the [Docker](https://www.docker.com/) image. Just run ```docker run -P lowerquality/gentle```. This works on all platforms supported by Docker.

3. Download the source code and run ```./install.sh```. Then run ```python3 serve.py``` to start the server. This works on Mac and Linux.

## Using Gentle

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

The default behaviour outputs the JSON to stdout.  See `python3 align.py --help` for options.

## Project Update

As of the latest project developments, we have encountered significant challenges with the alignment of Kikuyu language audio files using Gentle. The alignment process resulted in a high number of unaligned words, which suggests that the tool may not be fully compatible with the phonetic characteristics of the Kikuyu language.

### Next Steps

- **Data Review**: We will conduct a thorough review of the audio files and the corresponding text data to ensure clarity and accuracy.
- **Tool Configuration**: We will explore the settings and configurations of the Gentle tool to determine if adjustments can improve alignment accuracy.
- **Expert Consultation**: We will seek advice from linguists or language model experts with experience in the Kikuyu language to gain insights into improving the alignment process.
- **Alternative Tools**: If necessary, we will explore alternative alignment tools or methods that may be better suited for the Kikuyu language.

The project's progress and any changes to the approach will be documented in subsequent updates to this README.
