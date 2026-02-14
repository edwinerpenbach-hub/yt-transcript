# YouTube Transcript Downloader

A desktop application that downloads transcripts from YouTube videos. Built with Python and Tkinter.

## Features

- **Paste any YouTube URL** and fetch its transcript instantly
- **Three output modes:**
  - **With Timestamps** — each line prefixed with `[MM:SS]` or `[HH:MM:SS]`
  - **No Timestamps** — plain text, one segment per line
  - **Sentences** — segments merged and split into natural sentences
- **Save to file** — export the transcript as a `.txt` file
- **Threaded fetching** — the UI stays responsive while downloading

## Screenshot

The app window has a URL input field, a mode dropdown, and Generate / Save buttons above a scrollable text area.

## Quick Start

### Run from source

```bash
pip install youtube-transcript-api
python ui.py
```

### Run the pre-built exe

[Download the latest release](https://github.com/edwinerpenbach-hub/yt-transcript/releases/latest) and double-click `YouTubeTranscriptDownloader.exe`. No Python installation required.

## CLI Usage

`transcript.py` also works as a standalone command-line tool:

```bash
python transcript.py <youtube_url> [--no-timestamps] [--sentences] [--output FILE]
```

## Project Structure

```
ui.py            — Tkinter GUI application
transcript.py    — Core logic: video ID extraction, transcript fetching, formatting
```

## Building the exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "YouTubeTranscriptDownloader" ui.py
```

The output will be in the `dist/` folder.

## Requirements

- Python 3.10+
- [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)
