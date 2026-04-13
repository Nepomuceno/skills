# /// script
# requires-python = ">=3.10"
# ///
"""Remove a chroma key background from an image, replacing it with transparency.

Usage:
    uv run skills/image-generation/scripts/chroma-key.py \
        --input image.png --output image_transparent.png

How it works (progressive keying):
    1. Samples 100 pixels from four corner regions to detect the actual
       background color (FLUX models don't render exact hex values)
    2. Applies three progressive chroma key passes at increasing fuzz
       tolerance (4%, 8%, 12%) — each pass removes more of the gradient
       fringe between background and foreground
    3. Finishes with a 1px alpha erosion to clean the last sub-pixel edge

This is more robust than a single-pass key because FLUX backgrounds have
subtle color variation — a single high fuzz eats into icons, while a
single low fuzz leaves fringe. Progressive passes catch the gradient
naturally without over-removing.

Designed for FLUX-generated images where a magenta (#FF00FE) chroma key
background was requested but the model renders an approximate color.

Requires: magick (ImageMagick). Install with: brew install imagemagick
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter


# Progressive fuzz steps — each pass catches more of the gradient fringe
FUZZ_STEPS = [4, 8, 12]
# Final alpha erosion radius in pixels
ERODE_PX = 1


def detect_background_color(path: str) -> str:
    """Sample 100 corner pixels and return the most common hex color."""
    result = subprocess.run(
        ["magick", "identify", "-format", "%w %h", path],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Error reading image: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    w, h = (int(x) for x in result.stdout.strip().split())

    # 5x5 grid per corner = 25 samples x 4 corners = 100 samples
    offsets = [0, 2, 5, 8, 12]
    sample_points = []
    for ox in offsets:
        for oy in offsets:
            sample_points.append((ox, oy))                   # top-left
            sample_points.append((w - 1 - ox, oy))           # top-right
            sample_points.append((ox, h - 1 - oy))           # bottom-left
            sample_points.append((w - 1 - ox, h - 1 - oy))  # bottom-right

    fmt = "\\n".join(f"%[hex:u.p{{{x},{y}}}]" for x, y in sample_points)
    result = subprocess.run(
        ["magick", path, "-format", fmt, "info:"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Error sampling pixels: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    colors = [c.strip() for c in result.stdout.strip().split("\n") if c.strip()]
    if not colors:
        print("No colors sampled from corners.", file=sys.stderr)
        sys.exit(1)

    most_common = Counter(colors).most_common(1)[0][0]
    return f"#{most_common}"


def apply_progressive_key(input_path: str, output_path: str) -> None:
    """Remove background using progressive keying + alpha erosion."""
    bg_color = detect_background_color(input_path)
    print(f"  Detected background: {bg_color} (from 100 corner samples)")

    # Write to a temp file first to avoid corrupting input on in-place writes
    same_file = os.path.abspath(input_path) == os.path.abspath(output_path)
    if same_file:
        fd, tmp_path = tempfile.mkstemp(suffix=".png", dir=os.path.dirname(output_path))
        os.close(fd)
    else:
        tmp_path = output_path

    # Build magick command: progressive -transparent at increasing fuzz,
    # then erode alpha by ERODE_PX
    cmd = ["magick", input_path]
    for fuzz in FUZZ_STEPS:
        cmd += ["-fuzz", f"{fuzz}%", "-transparent", bg_color]
    cmd += ["-channel", "A", "-morphology", "Erode", f"Diamond:{ERODE_PX}", "+channel"]
    cmd += [tmp_path]

    steps_str = "→".join(f"{f}%" for f in FUZZ_STEPS)
    print(f"  Progressive key: {steps_str} + {ERODE_PX}px erode")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if same_file and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    if same_file:
        os.replace(tmp_path, output_path)

    size = os.path.getsize(output_path)
    print(f"  Saved: {output_path} ({size:,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove chroma key background from an image (progressive keying)"
    )
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output image path (with transparency)")
    args = parser.parse_args()

    if not shutil.which("magick"):
        print("Error: magick (ImageMagick) not found.", file=sys.stderr)
        print("Install with: brew install imagemagick", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found.", file=sys.stderr)
        sys.exit(1)

    print("Removing chroma key background...")
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    apply_progressive_key(args.input, args.output)


if __name__ == "__main__":
    main()
