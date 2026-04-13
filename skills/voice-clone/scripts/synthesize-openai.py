# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "python-dotenv"]
# ///
"""Synthesize speech using Azure OpenAI gpt-4o-mini-tts with instructions/vibe.

Usage:
  uv run skills/voice-clone/scripts/synthesize-openai.py \
    --text "Hello world" \
    --output output/test.wav \
    --voice "ash" \
    --instructions "Speak in a calm, warm tone."

Available voices: alloy, ash, ballad, coral, echo, fable, nova, onyx,
                  sage, shimmer, verse
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from _helpers import get_token, human_size, load_env, resolve_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthesize speech with Azure OpenAI gpt-4o-mini-tts")
    parser.add_argument("--text", required=True, help="Text to speak")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--voice", default="ash",
                        help="Voice name (default: ash). Options: alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer, verse")
    parser.add_argument("--instructions", default="", help="Vibe/instructions for how to speak")
    parser.add_argument("--format", default="wav", dest="audio_format",
                        help="Output format: wav, mp3, opus, aac, flac, pcm (default: wav)")
    parser.add_argument("--deployment", default=None,
                        help="Azure OpenAI deployment name (default: from DEPLOYMENT_NAME env or gpt-4o-mini-tts)")
    args = parser.parse_args()

    load_env()

    subdomain = os.environ.get("AZURE_CUSTOM_SUBDOMAIN", "")
    if not subdomain:
        print("ERROR: AZURE_CUSTOM_SUBDOMAIN must be set in .env for OpenAI TTS.", file=sys.stderr)
        sys.exit(1)

    api_version = os.environ.get("OPENAI_API_VERSION", "2025-03-01-preview")
    deployment = args.deployment or os.environ.get("DEPLOYMENT_NAME", "gpt-4o-mini-tts")

    output_file = resolve_path(args.output)

    print(f"Synthesizing with {deployment} (Azure OpenAI)...")
    print(f"  Voice: {args.voice}")
    print(f"  Format: {args.audio_format}")
    if args.instructions:
        print(f"  Instructions: {args.instructions}")
    print(f"  Output: {output_file}")

    token = get_token()

    payload: dict = {
        "model": deployment,
        "voice": args.voice,
        "input": args.text,
        "response_format": args.audio_format,
    }
    if args.instructions.strip():
        payload["instructions"] = args.instructions.strip()

    output_file.parent.mkdir(parents=True, exist_ok=True)

    url = (
        f"https://{subdomain}.openai.azure.com/openai/deployments/"
        f"{deployment}/audio/speech?api-version={api_version}"
    )

    with httpx.Client(timeout=120) as client:
        resp = client.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            content=json.dumps(payload).encode("utf-8"),
        )

    if resp.status_code == 200:
        output_file.write_bytes(resp.content)
        print(f"SUCCESS! Audio saved to: {output_file} ({human_size(output_file)})")
    else:
        output_file.write_bytes(resp.content)
        print(f"FAILED with HTTP {resp.status_code}", file=sys.stderr)
        try:
            print(f"  {resp.text}", file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
