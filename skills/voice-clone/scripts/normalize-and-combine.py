# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Normalize audio loudness and optionally combine multiple audio files.

Uses ffmpeg's loudnorm filter (EBU R128) with a two-pass approach for
precise normalization. Optionally concatenates multiple files.

Usage:
  # Normalize a single file
  uv run skills/voice-clone/scripts/normalize-and-combine.py \
    --input audio.wav --output normalized.wav

  # Normalize and concatenate multiple files
  uv run skills/voice-clone/scripts/normalize-and-combine.py \
    --input file1.wav --input file2.wav --input file3.wav \
    --output combined.wav

  # With options
  uv run skills/voice-clone/scripts/normalize-and-combine.py \
    --input audio.wav --output normalized.wav \
    --target-lufs -16 --reverb
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_ffmpeg() -> None:
    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg is not installed.", file=sys.stderr)
        print("  macOS:   brew install ffmpeg", file=sys.stderr)
        print("  Ubuntu:  sudo apt install ffmpeg", file=sys.stderr)
        print("  Windows: winget install ffmpeg  (or https://ffmpeg.org/download.html)", file=sys.stderr)
        sys.exit(1)


def measure_loudness(input_path: Path, target_lufs: float) -> dict[str, str]:
    """Pass 1: Measure loudness stats using ffmpeg loudnorm."""
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(input_path),
            "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=7:print_format=json",
            "-f", "null", "-",
        ],
        capture_output=True,
        text=True,
    )
    # loudnorm JSON is in stderr
    output = result.stderr

    # Find the JSON block in the output
    json_match = re.search(r'\{[^{}]*"input_i"[^{}]*\}', output, re.DOTALL)
    if not json_match:
        print(f"ERROR: Could not parse loudnorm stats from ffmpeg output", file=sys.stderr)
        sys.exit(1)

    stats = json.loads(json_match.group())
    return stats


def normalize_file(
    input_path: Path,
    output_path: Path,
    target_lufs: float,
    reverb: bool,
) -> None:
    """Two-pass normalization of a single file."""
    stats = measure_loudness(input_path, target_lufs)
    print(f"  Measured: I={stats['input_i']} dB  TP={stats['input_tp']} dB  LRA={stats['input_lra']} dB")

    # Build filter chain
    af = (
        f"loudnorm=I={target_lufs}:TP=-1.5:LRA=7"
        f":measured_I={stats['input_i']}"
        f":measured_TP={stats['input_tp']}"
        f":measured_LRA={stats['input_lra']}"
        f":measured_thresh={stats['input_thresh']}"
        f":linear=true"
    )
    if reverb:
        af += ",aecho=0.8:0.88:60:0.1"

    result = subprocess.run(
        [
            "ffmpeg", "-i", str(input_path),
            "-af", af,
            "-ar", "24000", "-acodec", "pcm_s16le",
            str(output_path), "-y",
        ],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        print(f"ERROR: ffmpeg normalization failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def concatenate_files(file_paths: list[Path], output_path: Path, tmpdir: Path) -> None:
    """Concatenate multiple WAV files using ffmpeg."""
    concat_list = tmpdir / "concat.txt"
    with open(concat_list, "w") as f:
        for p in file_paths:
            # Use forward slashes for ffmpeg compatibility on all platforms
            f.write(f"file '{p.as_posix()}'\n")

    result = subprocess.run(
        [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-acodec", "pcm_s16le",
            str(output_path), "-y",
        ],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        print(f"ERROR: ffmpeg concatenation failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def get_duration(path: Path) -> str:
    """Get audio duration using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or "unknown"


def human_size(path: Path) -> str:
    size = path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize audio loudness and optionally combine files")
    parser.add_argument("--input", action="append", required=True, dest="inputs",
                        help="Input WAV file (can be specified multiple times)")
    parser.add_argument("--output", required=True, help="Output WAV path")
    parser.add_argument("--target-lufs", type=float, default=-16,
                        help="Target loudness in LUFS (default: -16)")
    parser.add_argument("--reverb", action="store_true",
                        help="Apply subtle room reverb for keynote warmth")
    args = parser.parse_args()

    check_ffmpeg()

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path.cwd() / output_path

    input_paths = []
    for inp in args.inputs:
        p = Path(inp)
        if not p.is_absolute():
            p = Path.cwd() / p
        if not p.exists():
            print(f"ERROR: Input file not found: {p}", file=sys.stderr)
            sys.exit(1)
        input_paths.append(p)

    print("=== Audio Normalization ===")
    print(f"  Target: {args.target_lufs} LUFS")
    print()

    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        normalized_files: list[Path] = []

        for i, input_path in enumerate(input_paths):
            print(f"Normalizing: {input_path.name}")
            normalized = tmpdir / f"normalized_{i}.wav"
            normalize_file(input_path, normalized, args.target_lufs, args.reverb)
            normalized_files.append(normalized)
            print("  Done.")
            print()

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if len(normalized_files) == 1:
            # Single file: just copy
            shutil.copy2(normalized_files[0], output_path)
        else:
            # Multiple files: concatenate
            print(f"Concatenating {len(normalized_files)} files...")
            concatenate_files(normalized_files, output_path, tmpdir)

    duration = get_duration(output_path)
    print()
    print("=== DONE ===")
    print(f"  Output: {output_path}")
    print(f"  Duration: {duration}s")
    print(f"  Size: {human_size(output_path)}")


if __name__ == "__main__":
    main()
