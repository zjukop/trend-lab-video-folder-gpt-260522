# Video Folder GPT

Chat with a local folder of videos and get timestamped citations.

This is a minimal starter implementation: it indexes video filenames into a tiny SQLite database and exposes a simple search CLI. It is intentionally small so you can replace the stub indexer with transcript/OCR/frame sampling later.

## Requirements

- Python 3.11+

## Install

```bash
pip install -e .
```

## Usage

Index a folder:

```bash
video-folder-gpt index ./videos
```

Ask a question:

```bash
video-folder-gpt ask "zoom demo"
```

Run tests:

```bash
pytest
```
