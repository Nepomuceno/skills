# /// script
# requires-python = ">=3.10"
# ///
"""Split a grid image into individual tiles, with optional trim and validation.

Usage:
    uv run skills/image-generation/scripts/split-grid.py \
        --input grid.png --rows 2 --cols 2 --output-dir tiles/

    # With auto-trim and content validation (recommended for transparent grids):
    uv run skills/image-generation/scripts/split-grid.py \
        --input grid.png --rows 2 --cols 2 --output-dir tiles/ --trim --validate

Outputs files named tile_{row}_{col}.{ext} in the output directory (extension
matches the input file).

--trim:     Crops each tile to its actual content bounding box by removing
            fully-transparent rows/columns from the edges. Requires the grid
            to have been generated with --background transparent.

--validate: Checks each tile has meaningful content (non-transparent pixels).
            Warns if a quadrant appears empty or has very little content,
            indicating the model didn't place an item there.

Uses only Python stdlib (no PIL/Pillow). Image operations use sips (macOS)
or magick (ImageMagick) as available.
"""

import argparse
import os
import shutil
import subprocess
import sys


def get_image_size(path: str) -> tuple[int, int]:
    """Get image dimensions using sips or magick."""
    if shutil.which("sips"):
        result = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            width = height = 0
            for line in lines:
                if "pixelWidth" in line:
                    width = int(line.split(":")[-1].strip())
                elif "pixelHeight" in line:
                    height = int(line.split(":")[-1].strip())
            return width, height

    if shutil.which("magick"):
        result = subprocess.run(
            ["magick", "identify", "-format", "%w %h", path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            w, h = result.stdout.strip().split()
            return int(w), int(h)

    print("Error: neither sips nor magick (ImageMagick) found.", file=sys.stderr)
    print("Install ImageMagick: brew install imagemagick", file=sys.stderr)
    sys.exit(1)


def crop_image(src: str, dst: str, x: int, y: int, w: int, h: int) -> None:
    """Crop a region from src and save to dst."""
    if shutil.which("magick"):
        subprocess.run(
            ["magick", src, "-crop", f"{w}x{h}+{x}+{y}", "+repage", dst],
            check=True, capture_output=True
        )
        return

    if shutil.which("sips"):
        # sips crop is awkward — it crops from edges, not offset.
        # Copy first, then use --cropOffset
        shutil.copy2(src, dst)
        subprocess.run(
            ["sips", "--cropOffset", str(y), str(x), "-c", str(h), str(w), dst],
            check=True, capture_output=True
        )
        return

    print("Error: no image tool available for cropping.", file=sys.stderr)
    sys.exit(1)


def trim_transparent(path: str) -> None:
    """Trim fully-transparent edges from a PNG using ImageMagick."""
    subprocess.run(
        ["magick", path, "-fuzz", "1%", "-trim", "+repage", path],
        check=True, capture_output=True
    )


def validate_tile(path: str, min_content_pct: float = 1.0) -> tuple[bool, float]:
    """Check that a tile has meaningful content.

    Returns (is_valid, content_percentage).
    A tile is valid if at least min_content_pct% of pixels are non-transparent.
    """
    total, opaque_count = _get_alpha_stats(path)
    if total == 0:
        return False, 0.0
    pct = (opaque_count / total) * 100
    return pct >= min_content_pct, pct


def _get_alpha_stats(path: str) -> tuple[int, int]:
    """Get (total_pixels, non_transparent_pixels) using ImageMagick."""
    result = subprocess.run(
        ["magick", path, "-channel", "A", "-separate",
         "-format", "%[fx:mean] %[fx:w*h]", "info:"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: ImageMagick failed to analyze alpha for {path}", file=sys.stderr)
        if result.stderr.strip():
            print(result.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    parts = result.stdout.strip().split()
    if len(parts) < 2:
        print(f"Error: unexpected alpha stats output for {path}: {result.stdout!r}", file=sys.stderr)
        sys.exit(1)

    try:
        mean_alpha = float(parts[0])
        total = int(float(parts[1]))
    except ValueError:
        print(f"Error: could not parse alpha stats for {path}: {result.stdout!r}", file=sys.stderr)
        sys.exit(1)

    opaque = int(total * mean_alpha)
    return total, opaque


def main() -> None:
    parser = argparse.ArgumentParser(description="Split a grid image into tiles")
    parser.add_argument("--input", required=True, help="Input grid image")
    parser.add_argument("--rows", type=int, required=True, help="Number of rows")
    parser.add_argument("--cols", type=int, required=True, help="Number of columns")
    parser.add_argument("--output-dir", required=True, help="Output directory for tiles")
    parser.add_argument("--trim", action="store_true",
                        help="Trim transparent edges from each tile (requires transparent grid)")
    parser.add_argument("--validate", action="store_true",
                        help="Validate each tile has meaningful content (non-transparent pixels)")
    parser.add_argument("--min-content-pct", type=float, default=1.0,
                        help="Minimum %% of non-transparent pixels for a tile to pass validation (default: 1)")
    args = parser.parse_args()

    if args.trim and not shutil.which("magick"):
        print("Error: --trim requires magick (ImageMagick). Install with: brew install imagemagick",
              file=sys.stderr)
        sys.exit(1)

    if args.validate and not shutil.which("magick"):
        print("Error: --validate requires magick (ImageMagick) for reliable alpha analysis.",
              file=sys.stderr)
        print("Install with: brew install imagemagick", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    width, height = get_image_size(args.input)

    if width % args.cols != 0 or height % args.rows != 0:
        print(f"Error: image {width}x{height} is not evenly divisible by "
              f"{args.rows} rows x {args.cols} cols.", file=sys.stderr)
        sys.exit(1)

    tile_w = width // args.cols
    tile_h = height // args.rows

    print(f"Image: {width}x{height}")
    print(f"Grid:  {args.rows} rows x {args.cols} cols")
    print(f"Tile:  {tile_w}x{tile_h}")

    os.makedirs(args.output_dir, exist_ok=True)

    ext = os.path.splitext(args.input)[1] or ".png"
    all_valid = True
    tiles = []

    for row in range(args.rows):
        for col in range(args.cols):
            x = col * tile_w
            y = row * tile_h
            out_path = os.path.join(args.output_dir, f"tile_{row}_{col}{ext}")
            crop_image(args.input, out_path, x, y, tile_w, tile_h)

            status_parts = [f"  tile_{row}_{col}{ext}"]

            if args.trim:
                trim_transparent(out_path)
                new_w, new_h = get_image_size(out_path)
                status_parts.append(f"trimmed to {new_w}x{new_h}")

            if args.validate:
                valid, pct = validate_tile(out_path, args.min_content_pct)
                status_parts.append(f"content: {pct:.1f}%")
                if not valid:
                    status_parts.append("WARNING: low content — quadrant may be empty")
                    all_valid = False

            print(" | ".join(status_parts))
            tiles.append(out_path)

    print(f"\nDone. {args.rows * args.cols} tiles saved to {args.output_dir}/")

    if args.validate:
        if all_valid:
            print("Validation: PASSED — all tiles have sufficient content")
        else:
            print("Validation: WARNING — some tiles have low content")
            print("The model may not have placed items in all quadrants.")
            print("Consider re-generating with a clearer prompt or using individual generation.")
            sys.exit(2)


if __name__ == "__main__":
    main()
