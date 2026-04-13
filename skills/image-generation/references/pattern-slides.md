# Pattern: Slide / Presentation Backgrounds

## When to use

Generating background images for presentation slides, pitch decks, or any
content where the image sits behind text.

## Recommended parameters

- **Size:** `1536x1024` (landscape, closest to 16:10 slide ratio)
- **Quality:** `high`
- **Background:** `opaque`

## Prompt guidance

- Describe the exact color palette: specific hex codes or named colors
- Specify the visual style: "soft gradient", "geometric low-poly", "bokeh particles"
- State composition: "radial gradient from center", "diagonal sweep left to right"
- Include "no text, no words, no letters, no watermark" to prevent text artifacts
- Mention "presentation slide background" to bias toward clean, professional results
- Describe negative space: "leave the center clean for text overlay"
- For thematic slides, describe mood in detail: "futuristic", "corporate", "organic", "warm and inviting"

## Examples

Simple gradient:
```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint https://ACCOUNT.cognitiveservices.azure.com/ \
  --deployment gpt-image-1.5 \
  --prompt "Abstract presentation slide background. Smooth radial gradient flowing from deep navy blue (#1a1a4e) at the edges to a rich purple (#6a0dad) in the center. Subtle translucent geometric shapes — hexagons and triangles — scattered across the image at low opacity (10-15%), creating depth without distraction. Soft bokeh light particles in pale lavender floating near the top right corner. The overall mood is futuristic and professional. The center area should remain clean and uncluttered to allow text overlay. No text, no words, no letters, no logos, no watermarks anywhere in the image." \
  --size 1536x1024 --quality high \
  --output slide_bg.png
```

Thematic (nature):
```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint https://ACCOUNT.cognitiveservices.azure.com/ \
  --deployment gpt-image-1.5 \
  --prompt "Soft, dreamlike presentation slide background inspired by nature. A blurred forest canopy photographed from below looking up at the sky through leaves. Dominant color palette: deep emerald green (#2d6a4f) with lighter sage green (#95d5b2) highlights and warm golden sunlight filtering through gaps in the foliage. Heavy gaussian blur applied to all details so nothing is sharp — this is purely a texture/atmosphere background. Gentle lens flare from sunlight in the upper right area. Warm, inviting, organic mood suitable for a sustainability or environmental presentation. No sharp details, no identifiable leaves or branches, no text, no words, no watermarks." \
  --size 1536x1024 --quality high \
  --output nature_bg.png
```

## Post-processing

Slides are often compressed. Optimize after generation:
```bash
pngquant --quality=80-95 --output bg_opt.png slide_bg.png
```

If the slide system needs a specific resolution (e.g., 1920x1080):
```bash
sips -z 1080 1920 slide_bg.png --out slide_1080p.png
```
