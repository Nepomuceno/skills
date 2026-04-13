---
name: voice-clone
description: >
  Clone real voices and generate speech using Azure Cognitive Services Personal
  Voice and Azure OpenAI TTS. Use this skill whenever the user mentions voice
  cloning, custom voice, personal voice, speech synthesis, text-to-speech, TTS,
  generate audio narration, clone a voice, speaker profile, voice sample,
  consent recording, Azure Speech, DragonLatestNeural, gpt-4o-mini-tts, SSML,
  multi-speaker narration, audio normalization, voice talent, voice generation,
  narration pipeline, or wants to turn text into spoken audio with a cloned or
  built-in voice. Also trigger when the user asks about creating a speaker
  profile, synthesizing speech from text, building a voice pipeline, combining
  audio clips, normalizing loudness, or generating presentation narration.
---

# Voice Clone

Clone real voices and synthesize speech via Azure Cognitive Services Personal
Voice. Also supports built-in Azure Neural voices and Azure OpenAI
gpt-4o-mini-tts with vibe/instructions. The scripts handle the full pipeline:
record, convert, clone, synthesize, normalize, and combine.

All scripts are Python and run cross-platform (macOS, Linux, Windows) via
`uv run` with inline dependency metadata.

## Prerequisites

- `az` CLI authenticated (`az login`) to a subscription with a Speech resource
- `uv` ([astral.sh/uv](https://docs.astral.sh/uv/)) -- runs scripts with inline dependency metadata
- `ffmpeg` installed -- used for audio conversion and normalization
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`
  - Windows: `winget install ffmpeg`
- A `.env` file at the project root (loaded automatically by all scripts):

```
AZURE_REGION=eastus2
AZURE_CUSTOM_SUBDOMAIN=<your-subdomain>
AZURE_RESOURCE_NAME=<your-resource-name>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
API_VERSION=2024-02-01-preview
```

Before running any voice commands, point `az` at the correct subscription --
the default session may be on a different tenant, causing 400 errors:

```bash
az account set --subscription "<your-subscription-id>"
```

## Pipeline Overview

```
1. Record consent + voice sample (~30s each, reading the Microsoft consent statement)
2. Convert recordings to 24kHz 16-bit mono WAV (convert-audio.py)
3. Run clone-voice.py to create a speaker profile (one-time per voice)
4. Use synthesize.py to generate speech from any text
5. Optionally normalize and combine multi-speaker clips (normalize-and-combine.py)
```

## Creating a New Voice Clone

### 1. Record consent and voice sample

The speaker records two audio clips:

- **Consent statement**: reads the [Microsoft consent statement](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-create-voice) aloud (legally required).
- **Voice sample**: reads any text for ~30 seconds. Can be the same recording as consent.

Save to the project's recordings directory. Naming convention:
`<first-last>-consent-statement-<date>.m4a` and `<first-last>-voice-sample-<date>.m4a`.

### 2. Convert recordings to WAV

Azure requires 24kHz 16-bit mono PCM WAV:

```bash
uv run skills/voice-clone/scripts/convert-audio.py input.m4a output.wav
```

### 3. Run the clone pipeline

```bash
uv run skills/voice-clone/scripts/clone-voice.py \
  --name "Jane Doe" \
  --company "Contoso" \
  --consent-audio recordings/jane-doe-consent.wav \
  --voice-audio recordings/jane-doe-voice-sample.wav \
  --text "Hello, this is a test of my cloned voice." \
  --output output/audio/jane-doe/test.wav
```

This performs five steps:
1. Authenticates with Azure AD (`az account get-access-token`)
2. Creates a Personal Voice project (`PUT /customvoice/projects/<id>`)
3. Uploads consent audio (`POST /customvoice/consents/<id>`)
4. Creates personal voice and extracts the **speaker profile ID** (`POST /customvoice/personalvoices/<id>`)
5. Synthesizes a test utterance

The speaker profile ID is saved to `output/profiles/<name>-speaker-profile-id.txt`.

**Options:**

| Flag | Description | Required |
|------|-------------|----------|
| `--name` | Voice talent full name | Yes |
| `--company` | Company name | Yes |
| `--consent-audio` | Path to consent WAV | Yes |
| `--voice-audio` | Path to voice sample WAV (defaults to consent) | No |
| `--text` | Text to synthesize as test | Yes |
| `--output` | Output WAV path | Yes |
| `--project-id` | Custom project ID (auto-generated from name) | No |
| `--locale` | Locale, default `en-US` | No |

## Synthesizing Speech

Once a speaker profile exists, use the synthesis scripts directly -- no need to
re-run the clone pipeline.

### Cloned voice

```bash
uv run skills/voice-clone/scripts/synthesize.py \
  --profile-file output/profiles/jane-doe-speaker-profile-id.txt \
  --text "Hello, this is Jane speaking." \
  --output output/audio/jane-doe/hello.wav
```

Or pass the UUID directly with `--speaker-profile-id`.

| Flag | Description |
|------|-------------|
| `--profile-file` | Path to text file containing the speaker profile UUID |
| `--speaker-profile-id` | The UUID directly |
| `--text` | Text to speak |
| `--output` | Output WAV path |
| `--voice-model` | TTS model (default: `DragonLatestNeural`) |

### Built-in Azure Neural voice (no profile needed)

```bash
uv run skills/voice-clone/scripts/synthesize-generic.py \
  --text "Hello world" \
  --output output/generic-test.wav \
  --voice "en-US-GuyNeural"
```

List all available English voices:

```bash
uv run skills/voice-clone/scripts/synthesize-generic.py --list-voices
```

### Azure OpenAI gpt-4o-mini-tts

For the OpenAI TTS model with vibe/instructions support:

```bash
uv run skills/voice-clone/scripts/synthesize-openai.py \
  --text "Hello world" \
  --output output/openai-test.wav \
  --voice "ash" \
  --instructions "Speak in a calm, warm, authoritative tone. Slow pacing."
```

Available voices: `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `nova`,
`onyx`, `sage`, `shimmer`, `verse`.

## Audio Conversion

Convert any audio format to Azure-compatible WAV:

```bash
uv run skills/voice-clone/scripts/convert-audio.py input.m4a output.wav
```

Produces 24kHz 16-bit mono PCM WAV.

## Audio Normalization

Different speakers produce audio at different volumes (up to ~8 dB gaps).
Use the normalization script to equalize:

```bash
uv run skills/voice-clone/scripts/normalize-and-combine.py \
  --input main-audio.wav \
  --output normalized.wav \
  --target-lufs -16 --reverb
```

Uses ffmpeg's `loudnorm` filter (EBU R128) with a two-pass approach for
precision. Default target is -16 LUFS for presentations. Use -23 LUFS for
quieter narration.

For manual normalization, see `references/troubleshooting.md`.

## References

Read these on demand -- not needed for basic usage.

| Path | When to read |
|------|-------------|
| `references/ssml-reference.md` | SSML syntax, supported tags, multi-language workaround for DragonLatestNeural |
| `references/multi-speaker.md` | Multi-speaker narration patterns (dual, quad voice rotation, silence gaps) |
| `references/troubleshooting.md` | Common errors (400, 500, token expiry, volume issues) and manual ffmpeg normalization |

## Scripts

All scripts use `uv run` with inline dependency metadata. No manual
`pip install` needed.

| Script | Purpose |
|--------|---------|
| `scripts/clone-voice.py` | Full cloning pipeline: project, consent, voice profile, test synthesis |
| `scripts/synthesize.py` | Synthesize text with a cloned voice profile |
| `scripts/synthesize-generic.py` | Synthesize with a built-in Azure Neural voice |
| `scripts/synthesize-openai.py` | Synthesize with Azure OpenAI gpt-4o-mini-tts |
| `scripts/convert-audio.py` | Convert any audio to 24kHz 16-bit mono WAV |
| `scripts/normalize-and-combine.py` | Two-pass loudnorm normalization + optional concatenation |
| `scripts/_helpers.py` | Shared utilities (Azure auth, .env loading, path resolution) |
