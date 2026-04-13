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

Outputs files named tile_{row}_{col}.png in the output directory.

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
import struct
import subprocess
import sys
import zlib


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
    """Trim fully-transparent edges from a PNG using magick or sips+manual."""
    if shutil.which("magick"):
        # -trim removes borders that match the edge color.
        # For transparent PNGs, this removes transparent rows/cols from edges.
        # -fuzz 1% allows near-transparent pixels (alpha < 3) to be trimmed too.
        subprocess.run(
            ["magick", path, "-fuzz", "1%", "-trim", "+repage", path],
            check=True, capture_output=True
        )
        return

    # Fallback: sips doesn't support trim, but we can do a rough version
    # by reading the PNG pixel data and computing the content bounding box.
    bbox = _find_content_bbox(path)
    if bbox is None:
        return  # entirely transparent or couldn't read — leave as-is
    x, y, x2, y2 = bbox
    w = x2 - x
    h = y2 - y
    if w <= 0 or h <= 0:
        return
    # Re-crop to the content bounding box
    tmp = path + ".tmp.png"
    crop_image(path, tmp, x, y, w, h)
    os.replace(tmp, path)


def validate_tile(path: str, min_content_pct: float = 5.0) -> tuple[bool, float]:
    """Check that a tile has meaningful content.

    Returns (is_valid, content_percentage).
    A tile is valid if at least min_content_pct% of pixels are non-transparent.
    """
    stats = _get_alpha_stats(path)
    if stats is None:
        # Can't read alpha — assume valid (might be opaque image)
        return True, 100.0
    total, opaque_count = stats
    if total == 0:
        return False, 0.0
    pct = (opaque_count / total) * 100
    return pct >= min_content_pct, pct


def _get_alpha_stats(path: str) -> tuple[int, int] | None:
    """Get (total_pixels, non_transparent_pixels) using magick or raw PNG parsing.

    Returns None if alpha channel can't be read.
    """
    if shutil.which("magick"):
        # Use magick to get the percentage of opaque pixels
        # %[fx:mean] on the alpha channel gives avg alpha (0=transparent, 1=opaque)
        result = subprocess.run(
            ["magick", path, "-channel", "A", "-separate",
             "-format", "%[fx:mean] %[fx:w*h]", "info:"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split()
            if len(parts) >= 2:
                try:
                    mean_alpha = float(parts[0])
                    total = int(float(parts[1]))
                    opaque = int(total * mean_alpha)
                    return total, opaque
                except ValueError:
                    pass

    # Fallback: try raw PNG parsing (handles RGBA PNGs only)
    return _parse_png_alpha(path)


def _parse_png_alpha(path: str) -> tuple[int, int] | None:
    """Parse a PNG file and count non-transparent pixels.

    Only works with RGBA color type (6). Returns None for other types.
    """
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
            if sig != b"\x89PNG\r\n\x1a\n":
                return None

            width = height = 0
            bit_depth = 0
            color_type = 0
            idat_chunks = []

            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break
                length = struct.unpack(">I", chunk_header[:4])[0]
                chunk_type = chunk_header[4:8]

                data = f.read(length)
                f.read(4)  # CRC

                if chunk_type == b"IHDR":
                    width = struct.unpack(">I", data[0:4])[0]
                    height = struct.unpack(">I", data[4:8])[0]
                    bit_depth = data[8]
                    color_type = data[9]
                elif chunk_type == b"IDAT":
                    idat_chunks.append(data)
                elif chunk_type == b"IEND":
                    break

            if color_type != 6:  # Not RGBA
                return None
            if bit_depth != 8:
                return None

            # Decompress pixel data
            compressed = b"".join(idat_chunks)
            raw = zlib.decompress(compressed)

            # RGBA: 4 bytes per pixel, plus 1 filter byte per row
            stride = width * 4 + 1
            total = width * height
            opaque = 0

            for row_idx in range(height):
                row_start = row_idx * stride + 1  # skip filter byte
                for col in range(width):
                    px_start = row_start + col * 4
                    alpha = raw[px_start + 3]
                    if alpha > 0:
                        opaque += 1

            return total, opaque

    except Exception:
        return None


def _find_content_bbox(path: str) -> tuple[int, int, int, int] | None:
    """Find the bounding box of non-transparent content in a PNG.

    Returns (x, y, x2, y2) or None if image is fully transparent / can't read.
    """
    if shutil.which("magick"):
        # magick gives us the trim bounding box without actually trimming
        result = subprocess.run(
            ["magick", path, "-fuzz", "1%", "-format", "%@", "info:"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            # Format: WxH+X+Y
            info = result.stdout.strip()
            try:
                dims, offsets = info.split("+", 1)
                w, h = dims.split("x")
                x_off, y_off = offsets.split("+")
                x = int(x_off)
                y = int(y_off)
                return x, y, x + int(w), y + int(h)
            except (ValueError, IndexError):
                pass
    return None


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

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    width, height = get_image_size(args.input)
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
