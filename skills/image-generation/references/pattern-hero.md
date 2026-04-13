# Pattern: Hero Images / Banners

## When to use

Website hero sections, marketing banners, social media headers, blog post
covers — any wide-format image that may have text overlaid on it.

## Recommended parameters

- **Size:** `1536x1024` (landscape)
- **Quality:** `high`
- **Background:** `opaque`

## Prompt guidance

- Describe composition in detail: where the subject is, where empty space is
- Specify the exact color palette with named colors or hex codes
- Include lighting direction and quality: "warm golden hour light from the left", "cool diffused overcast"
- Mention depth of field: "shallow depth of field with blurred background", "everything in sharp focus"
- State where text will go: "leave the left 40% of the image clean and uncluttered for text overlay"
- Include atmosphere: "hazy", "crisp", "moody", "vibrant"
- Negative constraints: "no text, no words, no logos, no watermarks"

## Examples

Tech hero:
```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint https://ACCOUNT.cognitiveservices.azure.com/ \
  --deployment gpt-image-1.5 \
  --prompt "Wide cinematic landscape shot of a futuristic city skyline at dusk. The skyline fills the right two-thirds of the image with tall sleek skyscrapers featuring glowing neon blue (#00BFFF) and electric purple (#8A2BE2) accent lighting along their edges. The left third of the image is a clean dark sky area suitable for text overlay — keep this area free of buildings or bright elements. The sky transitions from deep navy (#0a0a2e) at the top to a warm amber (#FF8C00) horizon glow at the bottom where the sun has just set. Faint stars visible in the upper portion. A thin layer of fog or low clouds wraps around the base of the buildings, creating depth. Shot at golden hour with a wide-angle lens perspective. Cinematic color grading, high contrast. No text, no words, no logos, no watermarks, no UI elements." \
  --size 1536x1024 --quality high \
  --output hero.png
```

Blog cover:
```bash
uv run skills/image-generation/scripts/generate-image.py \
  --endpoint https://ACCOUNT.cognitiveservices.azure.com/ \
  --deployment gpt-image-1.5 \
  --prompt "Minimalist flat vector illustration of a developer workspace, viewed from a top-down isometric angle. A laptop computer sits slightly right of center with a code editor on screen showing colorful syntax-highlighted lines (no readable text). To the left of the laptop: a white ceramic coffee mug with steam wisps rising. To the right: a small potted succulent plant in a terracotta pot. The desk surface is a clean warm beige (#F5E6D3). All objects use a limited palette: warm coral (#FF6B6B), soft teal (#4ECDC4), creamy white (#FFF8E7), and charcoal (#2C3E50) for outlines. Flat design with no gradients, subtle drop shadows only (2px offset, 10% opacity). The top 30% of the image is open negative space in the beige desk color for a blog title. No text, no words, no watermarks." \
  --size 1536x1024 --quality high \
  --output blog_cover.png
```

## Post-processing

Resize to exact banner dimensions:
```bash
sips -z 600 1200 hero.png --out hero_1200x600.png
```

Optimize for web:
```bash
pngquant --quality=80-95 --output hero_web.png hero_1200x600.png
```
