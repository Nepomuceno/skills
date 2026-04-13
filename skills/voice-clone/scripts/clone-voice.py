# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "python-dotenv"]
# ///
"""Voice Clone - Azure Personal Voice Pipeline.

Automates the full personal voice cloning workflow:
  1. Create a project
  2. Upload consent audio
  3. Create personal voice (get speaker profile ID)
  4. Synthesize speech with the cloned voice

Usage:
  uv run skills/voice-clone/scripts/clone-voice.py \
    --name "Jane Doe" \
    --company "Contoso" \
    --consent-audio recordings/jane-doe-consent.wav \
    --voice-audio recordings/jane-doe-voice-sample.wav \
    --text "Hello, this is a test." \
    --output output/audio/jane-doe/test.wav

Prerequisites:
  - az CLI authenticated (az login)
  - .env file at current working directory with Azure configuration
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import httpx

# Allow importing the helpers module from the same directory
sys.path.insert(0, str(Path(__file__).parent))
from _helpers import get_azure_config, get_token, human_size, load_env, log_step, resolve_path, safe_name


def check_operation(client: httpx.Client, operation_url: str, token: str, max_attempts: int = 60) -> dict | None:
    """Poll an async operation until it succeeds, fails, or times out."""
    for attempt in range(1, max_attempts + 1):
        time.sleep(5)
        resp = client.get(operation_url, headers={"Authorization": f"Bearer {token}"})

        if resp.status_code != 200:
            print(f"  Waiting... (attempt {attempt}/{max_attempts}, HTTP {resp.status_code})")
            continue

        data = resp.json()
        status = data.get("status", "")
        print(f"  Status: {status} (attempt {attempt}/{max_attempts})")

        if status == "Succeeded":
            return data
        if status == "Failed":
            print(f"  FAILED: {data}", file=sys.stderr)
            return None

    print("  TIMEOUT: Operation did not complete in time", file=sys.stderr)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Clone a voice using Azure Personal Voice")
    parser.add_argument("--name", required=True, help="Voice talent full name")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--consent-audio", required=True, help="Path to consent audio WAV")
    parser.add_argument("--voice-audio", help="Path to voice sample WAV (defaults to consent audio)")
    parser.add_argument("--text", required=True, help="Text to synthesize as test")
    parser.add_argument("--output", required=True, help="Output audio file path")
    parser.add_argument("--project-id", help="Custom project ID (auto-generated if omitted)")
    parser.add_argument("--locale", default="en-US", help="Locale (default: en-US)")
    args = parser.parse_args()

    load_env()
    config = get_azure_config()

    consent_audio = resolve_path(args.consent_audio)
    voice_audio = resolve_path(args.voice_audio) if args.voice_audio else consent_audio
    output_file = resolve_path(args.output)

    slug = safe_name(args.name)
    project_id = args.project_id or f"pv-project-{slug}"
    consent_id = f"consent-{slug}"
    personal_voice_id = f"voice-{slug}"

    # ── Step 1: Authenticate ──────────────────────────────────────────
    log_step("Step 1: Authenticating with Azure AD")
    token = get_token()
    print("  Token obtained successfully.")

    with httpx.Client(timeout=120) as client:
        headers = {"Authorization": f"Bearer {token}"}

        # ── Step 2: Create Project ────────────────────────────────────
        log_step(f"Step 2: Creating Personal Voice Project ({project_id})")
        url = f"{config['base_url']}/customvoice/projects/{project_id}?api-version={config['api_version']}"
        resp = client.put(
            url,
            headers={**headers, "Content-Type": "application/json"},
            json={"description": f"Personal voice for {args.name}", "kind": "PersonalVoice"},
        )
        if resp.status_code in (200, 201):
            print(f"  Project created/exists: {project_id}")
        elif resp.status_code == 409:
            print(f"  Project already exists: {project_id}")
        else:
            print(f"  HTTP {resp.status_code}: {resp.text}")
            print("  WARNING: Unexpected response, continuing anyway...")

        # ── Step 3: Upload Consent ────────────────────────────────────
        log_step(f"Step 3: Uploading Consent Audio ({consent_id})")
        print(f"  Audio file: {consent_audio}")

        url = f"{config['base_url']}/customvoice/consents/{consent_id}?api-version={config['api_version']}"
        with open(consent_audio, "rb") as f:
            resp = client.post(
                url,
                headers=headers,
                data={
                    "description": f"Consent for {args.name}",
                    "projectId": project_id,
                    "voiceTalentName": args.name,
                    "companyName": args.company,
                    "locale": args.locale,
                },
                files={"audiodata": (consent_audio.name, f, "audio/wav")},
            )
        print(f"  HTTP {resp.status_code}")

        operation_url = resp.headers.get("Operation-Location", "")
        if operation_url:
            print("  Waiting for consent processing...")
            check_operation(client, operation_url, token)

        # ── Step 4: Create Personal Voice ─────────────────────────────
        log_step(f"Step 4: Creating Personal Voice ({personal_voice_id})")
        print(f"  Voice audio: {voice_audio}")

        # Refresh token in case it expired
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}

        url = f"{config['base_url']}/customvoice/personalvoices/{personal_voice_id}?api-version={config['api_version']}"
        with open(voice_audio, "rb") as f:
            resp = client.post(
                url,
                headers=headers,
                data={"projectId": project_id, "consentId": consent_id},
                files={"audiodata": (voice_audio.name, f, "audio/wav")},
            )
        print(f"  HTTP {resp.status_code}")

        speaker_profile_id = ""
        try:
            speaker_profile_id = resp.json().get("speakerProfileId", "")
        except Exception:
            pass

        operation_url = resp.headers.get("Operation-Location", "")
        if operation_url and not speaker_profile_id:
            print("  Waiting for personal voice processing...")
            check_operation(client, operation_url, token)

        # If we still don't have it, fetch from the API
        if not speaker_profile_id:
            time.sleep(5)
            token = get_token()
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{config['base_url']}/customvoice/personalvoices/{personal_voice_id}?api-version={config['api_version']}"
            resp = client.get(url, headers=headers)
            try:
                speaker_profile_id = resp.json().get("speakerProfileId", "")
            except Exception:
                pass
            print(f"  Full voice details: {resp.text}")

        if not speaker_profile_id:
            print("ERROR: Could not obtain speaker profile ID", file=sys.stderr)
            sys.exit(1)

        print()
        print(f"  *** Speaker Profile ID: {speaker_profile_id} ***")
        print()

        # Save the profile ID
        profiles_dir = Path.cwd() / "output" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)
        profile_path = profiles_dir / f"{slug}-speaker-profile-id.txt"
        profile_path.write_text(speaker_profile_id)
        print(f"  Saved to: {profile_path}")

        # ── Step 5: Synthesize Speech ─────────────────────────────────
        log_step("Step 5: Synthesizing Speech with Personal Voice")
        token = get_token()

        ssml = (
            "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' "
            "xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>"
            "  <voice name='DragonLatestNeural'>"
            f"    <mstts:ttsembedding speakerProfileId='{speaker_profile_id}'>"
            f"      {args.text}"
            "    </mstts:ttsembedding>"
            "  </voice>"
            "</speak>"
        )

        print(f"  Generating audio...")
        print(f"  Output: {output_file}")
        output_file.parent.mkdir(parents=True, exist_ok=True)

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
            print(f"  SUCCESS! Audio saved to: {output_file}")
            print(f"  File size: {human_size(output_file)}")
        else:
            output_file.write_bytes(resp.content)
            print(f"  HTTP {resp.status_code} - Synthesis may have failed")
            try:
                print(f"  Error: {resp.text}")
            except Exception:
                pass

    log_step("Done!")
    print(f"  Speaker Profile ID: {speaker_profile_id}")
    print(f"  Output file: {output_file}")


if __name__ == "__main__":
    main()
