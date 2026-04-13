# Pattern: Transparent Inserts

## When to use

Generating assets that will be overlaid on other content: icons, mascots,
logos, diagrams, product shots, stickers, UI elements.

## Recommended parameters

- **Size:** `1024x1024` (square — trim/resize after)
- **Quality:** `high`
- **Background:** `transparent`

## Prompt guidance

- Explicitly state "on transparent background" or "isolated on blank background"
- OpenAI models (gpt-image-1.5) handle transparency natively — no post-processing needed
- FLUX models don't support native transparency — use `generate-image.py --background transparent` (adds chroma key) then run `chroma-key.py` to strip the background
- Describe the subject in full detail: shape, color (use hex codes), proportions
- Specify the art style precisely: "flat vector", "3D isometric render", "hand-drawn sketch"
- Mention size relative to canvas: "centered, filling about 70% of the canvas"
- Include negative constraints: "no shadow, no text, no glow, no outline"
- For icons, specify edge treatment: "clean sharp edges", "1px dark outline", "soft rounded corners"

## Examples

Icon:
```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint https://ACCOUNT.cognitiveservices.azure.com/ \
  --deployment gpt-image-1.5 \
  --prompt "A lightning bolt icon on transparent background. Flat vector design with zero gradients. The bolt is a vibrant golden yellow (#FFD700) with a thin 1px dark amber (#B8860B) outline for definition. The bolt has sharp angular edges, 5 segments in a classic zigzag shape, pointing downward at a slight 10-degree angle to the right. Centered on the canvas, filling approximately 70% of the total area with generous transparent padding on all sides. No shadow, no glow, no text, no additional elements, no background color or shape behind the bolt." \
  --size 1024x1024 --quality high --background transparent \
  --output lightning_icon.png
```

Mascot:
```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint https://ACCOUNT.cognitiveservices.azure.com/ \
  --deployment gpt-image-1.5 \
  --prompt "A friendly robot mascot character on transparent background. Cartoon illustration style with soft cel-shading and clean outlines. The robot has a rounded rectangular body in light blue (#87CEEB) with a darker blue (#4682B4) chest panel. Large expressive oval eyes with white sclera and black pupils showing a happy expression. Small antenna on top with a glowing yellow (#FFD700) ball. Short stubby arms — the right arm is raised in a cheerful waving gesture. The robot is shown in a 3/4 view facing slightly left. Centered on the canvas with the full body visible from head to feet. No shadow on the ground, no text, no speech bubble, no additional objects or scenery." \
  --size 1024x1024 --quality high --background transparent \
  --output mascot.png
```

## Post-processing

Trim excess transparent space and resize to target:
```bash
magick mascot.png -trim +repage trimmed.png
sips --resampleWidth 256 trimmed.png --out mascot_256.png
```

For web usage, compress:
```bash
pngquant --quality=80-95 --output mascot_web.png mascot_256.png
```
