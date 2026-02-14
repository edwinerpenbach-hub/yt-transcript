import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def combine_into_sentences(transcript):
    """Combine transcript segments into full sentences."""
    raw_text = " ".join(entry.text for entry in transcript)
    # Remove tags like [music], [applause], etc. and >> markers
    raw_text = re.sub(r'\[.*?\]', '', raw_text)
    raw_text = re.sub(r'>>', '', raw_text)
    # Normalize whitespace
    raw_text = re.sub(r'\s+', ' ', raw_text).strip()
    # Split on sentence-ending punctuation, keeping the punctuation attached
    sentences = re.split(r'(?<=[.!?])\s+', raw_text)
    return "\n".join(s.strip() for s in sentences if s.strip())


def download_transcript(url, include_timestamps=True, sentences=False):
    """Download and return the transcript for a YouTube video."""
    video_id = extract_video_id(url)
    if not video_id:
        print(f"Error: Could not extract video ID from '{url}'")
        sys.exit(1)

    print(f"Fetching transcript for video: {video_id}")

    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)

    if sentences:
        return combine_into_sentences(transcript)

    lines = []
    for entry in transcript:
        text = re.sub(r'\[.*?\]', '', entry.text)
        text = re.sub(r'>>', '', text).strip()
        if not text:
            continue
        if include_timestamps:
            timestamp = format_timestamp(entry.start)
            lines.append(f"[{timestamp}] {text}")
        else:
            lines.append(text)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python transcript.py <youtube_url> [--no-timestamps] [--sentences] [--output FILE]")
        sys.exit(1)

    url = sys.argv[1]
    include_timestamps = "--no-timestamps" not in sys.argv

    output_file = None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    sentences = "--sentences" in sys.argv

    text = download_transcript(url, include_timestamps, sentences)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Transcript saved to {output_file}")
    else:
        print("\n" + text)


if __name__ == "__main__":
    main()
