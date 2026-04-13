# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "python-dotenv"]
# ///
"""Synthesize speech using an existing cloned voice speaker profile.

Usage:
  uv run skills/voice-clone/scripts/synthesize.py \
    --profile-file output/profiles/jane-doe-speaker-profile-id.txt \
    --text "Hello world" \
    --output output/audio/jane-doe/hello.wav

  Or pass the UUID directly:
  uv run skills/voice-clone/scripts/synthesize.py \
    --speaker-profile-id "UUID-HERE" \
    --text "Hello world" \
    --output output/test.wav
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from _helpers import get_azure_config, get_token, human_size, load_env, resolve_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthesize speech with a cloned voice profile")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--speaker-profile-id", help="Speaker profile UUID directly")
    group.add_argument("--profile-file", help="Path to text file containing the speaker profile UUID")
    parser.add_argument("--text", required=True, help="Text to speak")
    parser.add_argument("--output", required=True, help="Output WAV path")
    parser.add_argument("--voice-model", default="DragonLatestNeural", help="TTS model (default: DragonLatestNeural)")
    args = parser.parse_args()

    load_env()
    config = get_azure_config()

    # Resolve speaker profile ID
    if args.profile_file:
        profile_path = resolve_path(args.profile_file)
        speaker_profile_id = profile_path.read_text().strip()
    else:
        speaker_profile_id = args.speaker_profile_id

    output_file = resolve_path(args.output)

    print("Synthesizing with personal voice...")
    print(f"  Speaker Profile: {speaker_profile_id}")
    print(f"  Voice Model: {args.voice_model}")
    print(f"  Output: {output_file}")

    token = get_token()

    ssml = (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
        "xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>"
        f"  <voice name='{args.voice_model}'>"
        f"    <mstts:ttsembedding speakerProfileId='{speaker_profile_id}'>"
        f"      {args.text}"
        "    </mstts:ttsembedding>"
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
