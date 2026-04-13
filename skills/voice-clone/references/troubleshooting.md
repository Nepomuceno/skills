# Troubleshooting

Common issues and fixes for the voice clone pipeline.

## 400 Bad Request

The Azure CLI is likely on the wrong subscription/tenant. Fix with:

```bash
az account set --subscription "<your-subscription-id>"
```

Verify with `az account show` that the correct subscription is active.

## 500 Internal Server Error with Non-English `xml:lang`

The `DragonLatestNeural` model does not support changing the top-level
`xml:lang` to a non-English locale. Use the `<lang>` tag inside the SSML body
instead. See `references/ssml-reference.md` for the multi-language workaround.

## 401 Unauthorized / Token Expiration

Azure AD tokens expire after ~60 minutes. If you get 401 errors:

1. Re-run the script -- each invocation fetches a fresh token automatically
2. For custom Python code making multiple API calls, re-call `get_token()`
   between requests

## Audio Too Quiet or Too Loud

Speaker profiles produce audio at different volume levels. Use the
normalization script:

```bash
uv run skills/voice-clone/scripts/normalize-and-combine.py \
    --input audio.wav --output normalized.wav --target-lufs -16
```

Target recommendations:
- **-16 LUFS**: Presentations, keynotes, videos
- **-23 LUFS**: Quiet narration, podcast-style

### Manual Normalization with ffmpeg

For ad-hoc normalization of individual clips:

```bash
# Pass 1: Measure loudness
ffmpeg -i input.wav \
    -af loudnorm=I=-23:TP=-1.5:LRA=11:print_format=json \
    -f null - 2>&1

# Pass 2: Apply with measured values
ffmpeg -i input.wav \
    -af "loudnorm=I=-23:TP=-1.5:LRA=11:measured_I=<value>:measured_TP=<value>:measured_LRA=<value>:measured_thresh=<value>:linear=true" \
    -ar 24000 -acodec pcm_s16le \
    output_normalized.wav -y
```

Replace `<value>` placeholders with the numbers from the Pass 1 JSON output.

## Audio Format Issues

Azure Speech API requires **24kHz 16-bit mono PCM WAV** for input audio
(consent and voice sample recordings). Use `convert-audio.py`:

```bash
uv run skills/voice-clone/scripts/convert-audio.py input.m4a output.wav
```

Common source formats that need conversion: `.m4a`, `.mp3`, `.ogg`, `.flac`,
`.aac`, `.webm`.

## Consent Processing Takes a Long Time

The consent upload (`POST /customvoice/consents`) is async. The
`clone-voice.py` script polls the operation URL every 5 seconds for up to 5
minutes. If it times out:

1. Check the Azure portal for the consent status
2. Re-run the script -- if the consent already exists (409), it continues

## Personal Voice Processing Fails

If the voice creation step fails:

1. Ensure the voice sample is at least ~20 seconds of clear speech
2. Ensure the audio is 24kHz 16-bit mono WAV (use `convert-audio.py`)
3. Ensure the consent audio clearly reads the Microsoft consent statement
4. Check that the speaker's voice is distinct and the recording has minimal background noise

## Speaker Profile ID Not Found

If `clone-voice.py` can't extract the speaker profile ID:

1. The personal voice may still be processing -- wait and check the Azure portal
2. Fetch it manually:

```bash
az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv
# Then use the token to curl the API:
curl -s -H "Authorization: Bearer <TOKEN>" \
    "https://<SUBDOMAIN>.cognitiveservices.azure.com/customvoice/personalvoices/voice-jane-doe?api-version=2024-02-01-preview" | python3 -m json.tool
```

The `speakerProfileId` field in the response is the UUID you need.

## `az` CLI Not Found

The `az` CLI is required for authentication. Install it:
- macOS: `brew install azure-cli`
- Ubuntu: `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`
- Windows: `winget install Microsoft.AzureCLI`

Then authenticate: `az login`
