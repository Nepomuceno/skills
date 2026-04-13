# Multi-Speaker Narration

Patterns for generating narration with multiple cloned voices, combining them
into a single audio file.

## Approach

Each speaker's paragraphs are synthesized separately (one API call per
paragraph), then the clips are concatenated with silence gaps between them.
This approach:

- Lets each speaker use their own profile ID
- Allows varying silence gaps for pacing
- Avoids token expiration issues (refresh between calls)

## Dual Voice (2 Speakers)

Alternate paragraphs between two speakers. Speaker A reads odd paragraphs,
Speaker B reads even paragraphs.

```python
import subprocess

speakers = {
    "A": "output/profiles/speaker-a-profile-id.txt",
    "B": "output/profiles/speaker-b-profile-id.txt",
}
paragraphs = ["First paragraph...", "Second paragraph...", ...]

for i, text in enumerate(paragraphs):
    profile = speakers["A"] if i % 2 == 0 else speakers["B"]
    subprocess.run([
        "uv", "run", "skills/voice-clone/scripts/synthesize.py",
        "--profile-file", profile,
        "--text", text,
        "--output", f"output/clips/paragraph-{i+1}.wav",
    ], check=True)
```

Then combine the clips:

```bash
uv run skills/voice-clone/scripts/normalize-and-combine.py \
    --input output/clips/paragraph-1.wav \
    --input output/clips/paragraph-2.wav \
    --input output/clips/paragraph-3.wav \
    --output output/combined.wav
```

## Quad Voice (4 Speakers)

Round-robin rotation across four speakers:

```
Speaker A: paragraphs 1, 5, 9
Speaker B: paragraphs 2, 6, 10
Speaker C: paragraphs 3, 7
Speaker D: paragraphs 4, 8
```

The rotation uses modular arithmetic: `speaker = (paragraph - 1) % 4`.

## Varied Silence Gaps

For natural pacing, vary the silence between paragraphs based on narrative
relationship:

| Gap type | Duration | When to use |
|----------|----------|-------------|
| Tight | 0.6s | Tightly related paragraphs (continuation of same idea) |
| Normal | 0.9s | Standard transitions between ideas |
| Wide | 1.2s | Major topic shifts or dramatic pauses |

To insert silence between clips, generate a silence WAV with ffmpeg:

```bash
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 0.8 -acodec pcm_s16le silence.wav -y
```

Then include the silence file between clips when combining.

## Token Refresh

Azure AD tokens expire after ~60 minutes. The Python scripts call
`az account get-access-token` for each invocation, so tokens are always fresh
when running scripts individually. For custom Python code that makes multiple
API calls in a single process, refresh the token between paragraphs.

## Combining Without Extra Pauses

TTS clips already contain natural trailing silence. When combining dialog-style
clips where speakers are responding to each other, do NOT add extra silence --
use `normalize-and-combine.py` directly, which concatenates without gaps.

## Volume Equalization

Different speaker profiles produce audio at different volume levels (up to ~8 dB
gaps). Always normalize after combining multi-speaker audio:

```bash
uv run skills/voice-clone/scripts/normalize-and-combine.py \
    --input combined.wav \
    --output combined-normalized.wav \
    --target-lufs -16
```

Or normalize each clip individually before combining if you need per-speaker
control.
