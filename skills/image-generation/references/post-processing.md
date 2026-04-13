# Post-Processing CLI Reference

Prefer command-line tools over Python image libraries. They are fast, scriptable,
and available without pip installs.

## sips (macOS built-in)

Zero install. Always available on macOS.

```bash
# Resize to exact dimensions
sips -z 800 1200 input.png --out resized.png

# Resize preserving aspect ratio (fit within width)
sips --resampleWidth 800 input.png --out resized.png

# Convert format
sips -s format jpeg input.png --out output.jpg
sips -s format png input.jpg --out output.png

# Crop (height x width from center)
sips -c 600 800 input.png --out cropped.png

# Pad to exact dimensions (adds letterboxing)
sips -p 1080 1920 input.png --out padded.png

# Get image dimensions
sips -g pixelWidth -g pixelHeight input.png

# Rotate
sips -r 90 input.png --out rotated.png
```

## ImageMagick (`magick`)

Install: `brew install imagemagick`

More powerful than sips — precise cropping, trimming, compositing, montage.

```bash
# Resize
magick input.png -resize 800x600 output.png

# Crop specific region (WxH+X+Y from top-left)
magick input.png -crop 512x512+100+50 +repage output.png

# Trim transparent/white borders automatically
magick input.png -trim +repage trimmed.png

# Composite (overlay one image on another)
magick background.png overlay.png -gravity center -composite result.png

# Add border/padding
magick input.png -bordercolor transparent -border 20x20 output.png

# Batch convert all PNGs to JPG
for f in *.png; do magick "$f" "${f%.png}.jpg"; done

# Create a montage (combine multiple images into grid)
magick montage img1.png img2.png img3.png img4.png -geometry 512x512+5+5 grid.png

# Strip metadata and optimize
magick input.png -strip -quality 95 optimized.png
```

## pngquant (lossy PNG compression)

Install: `brew install pngquant`

Best for web assets. 60-80% file size reduction with minimal visual loss.

```bash
pngquant --quality=65-80 --output optimized.png input.png
```

## optipng (lossless PNG optimization)

Install: `brew install optipng`

Reduces file size without any quality loss. Slower than pngquant.

```bash
optipng -o7 input.png
```

## split-grid.py (included)

Splits a generated grid image into individual tiles.

```bash
uv run skills/image-generation/scripts/split-grid.py \
  --input grid.png --rows 2 --cols 2 --output-dir tiles/
```

Outputs: `tiles/tile_0_0.png`, `tiles/tile_0_1.png`, etc.

## Tool selection guide

| Task | Tool | Why |
|------|------|-----|
| Quick resize/convert on macOS | `sips` | Zero install, fast |
| Crop specific pixel region | `magick -crop` | Precise offsets |
| Trim whitespace/transparency | `magick -trim` | Automatic edge detection |
| Overlay/composite images | `magick -composite` | Layer control, gravity |
| Compress PNGs for web | `pngquant` | Best size reduction |
| Lossless optimization | `optipng` | No quality loss |
| Split grids into tiles | `split-grid.py` | Purpose-built |

## Common pipelines

**Generate + optimize for web:**
```bash
uv run skills/image-generation/scripts/generate-image.py ... --output raw.png
pngquant --quality=80-95 --output optimized.png raw.png
```

**Generate transparent + trim + resize:**
```bash
uv run skills/image-generation/scripts/generate-image.py ... --background transparent --output raw.png
magick raw.png -trim +repage trimmed.png
sips --resampleWidth 256 trimmed.png --out icon_256.png
```

**Generate grid + split + optimize:**
```bash
uv run skills/image-generation/scripts/generate-image.py ... --output grid.png
uv run skills/image-generation/scripts/split-grid.py --input grid.png --rows 2 --cols 2 --output-dir tiles/
for f in tiles/*.png; do pngquant --quality=80-95 --output "${f%.png}_opt.png" "$f"; done
```
