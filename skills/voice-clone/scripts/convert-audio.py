# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Convert audio files to WAV format suitable for Azure Speech API.

Produces 24kHz 16-bit mono PCM WAV (required by Azure Speech API).

Usage:
  uv run skills/voice-clone/scripts/convert-audio.py INPUT OUTPUT
  uv run skills/voice-clone/scripts/convert-audio.py input.m4a output.wav
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert audio to 24kHz 16-bit mono WAV for Azure Speech API"
    )
    parser.add_argument("input", help="Input audio file (any format ffmpeg supports)")
    parser.add_argument("output", help="Output WAV file path")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg is not installed.", file=sys.stderr)
        print("  macOS:   brew install ffmpeg", file=sys.stderr)
        print("  Ubuntu:  sudo apt install ffmpeg", file=sys.stderr)
        print("  Windows: winget install ffmpeg  (or https://ffmpeg.org/download.html)", file=sys.stderr)
        sys.exit(1)

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Converting: {input_path} -> {output_path}")
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(input_path),
            "-acodec", "pcm_s16le",
            "-ar", "24000",
            "-ac", "1",
            str(output_path),
            "-y",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"ERROR: ffmpeg failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    size = output_path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            print(f"Done! Output: {output_path} ({size:.1f} {unit})")
            break
        size /= 1024


if __name__ == "__main__":
    main()
