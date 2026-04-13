# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "python-dotenv"]
# ///
"""Synthesize speech using a built-in (non-cloned) Azure Neural TTS voice.

Usage:
  uv run skills/voice-clone/scripts/synthesize-generic.py \
    --text "Hello world" \
    --output output/generic-output.wav \
    --voice "en-US-GuyNeural"

  uv run skills/voice-clone/scripts/synthesize-generic.py --list-voices
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from _helpers import escape_xml, get_azure_config, get_token, human_size, load_env, resolve_path


def list_voices(config: dict[str, str], token: str) -> None:
    """List available English Neural voices."""
    print("Available English voices:")
    with httpx.Client(timeout=30) as client:
        resp = client.get(
            f"{config['base_url']}{config['voices_path']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        resp.raise_for_status()
        voices = resp.json()

    en_voices = [v for v in voices if v.get("Locale", "").startswith("en-")]
    for v in sorted(en_voices, key=lambda x: x["ShortName"]):
        name = v["ShortName"]
        gender = v.get("Gender", "")
        vtype = v.get("VoiceType", "")
        print(f"  {name:<40s} {gender:<8s} {vtype}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthesize speech with a built-in Azure Neural voice")
    parser.add_argument("--text", help="Text to speak")
    parser.add_argument("--output", help="Output WAV path")
    parser.add_argument("--voice", default="en-US-GuyNeural", help="Voice name (default: en-US-GuyNeural)")
    parser.add_argument("--list-voices", action="store_true", help="List available English voices")
    args = parser.parse_args()

    load_env()
    config = get_azure_config()
    token = get_token()

    if args.list_voices:
        list_voices(config, token)
        return

    if not args.text or not args.output:
        parser.error("--text and --output are required (unless using --list-voices)")

    output_file = resolve_path(args.output)

    print("Synthesizing with generic voice...")
    print(f"  Voice: {args.voice}")
    print(f"  Output: {output_file}")

    ssml = (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
        f"  <voice name='{escape_xml(args.voice)}'>"
        f"    {escape_xml(args.text)}"
        "  </voice>"
        "</speak>"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with httpx.Client(timeout=120) as client:
        resp = client.post(
            f"{config['base_url']}{config['tts_path']}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
                "User-Agent": "VoiceClone/1.0",
            },
            content=ssml.encode("utf-8"),
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
