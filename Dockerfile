ARG BASE=nvidia/cuda:11.8.0-base-ubuntu22.04
FROM ${BASE}

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed

# Install Dependencies:
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN pip3 install gunicorn
RUN pip3 install flask_cors  # Install flask_cors module
RUN rm -rf /root/.cache/pip

# Copy TTS repository contents:
WORKDIR /app
COPY . /app

# Copy the .models.json file to the root directory
COPY .models.json /.models.json

RUN make install

# Set the entry point to the Flask application using Gunicorn
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
