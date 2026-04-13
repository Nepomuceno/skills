# /// script
# requires-python = ">=3.10"
# ///
"""Generate an image via Azure AI Foundry and save to disk.

Supports both OpenAI models (gpt-image-1.5) and Black Forest Labs models
(FLUX.2-pro, FLUX.2-flex) through their respective API paths.

Usage:
    uv run skills/image-generation/scripts/generate-image.py \
        --endpoint https://ACCOUNT.cognitiveservices.azure.com/ \
        --deployment gpt-image-1.5 \
        --prompt "A blue circle on white background" \
        --output image.png \
        [--size 1024x1024] [--quality medium] \
        [--background opaque] [--output-format png]

Requires: az CLI logged in. Uses Azure AD token auth (no API keys).

Model routing:
    - OpenAI models (gpt-image-*): uses /openai/deployments/ path on
      cognitiveservices.azure.com, supports transparent background and quality.
    - FLUX models (FLUX.*): uses /providers/blackforestlabs/ path on
      services.ai.azure.com. FLUX doesn't support native transparency, so
      when --background transparent is requested, the script appends a
      chroma-key background instruction to the prompt. Run chroma-key.py
      afterward to strip the background to transparency.
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from typing import NoReturn


VALID_SIZES = ["1024x1024", "1024x1536", "1536x1024", "auto"]
VALID_QUALITIES = ["low", "medium", "high"]
VALID_BACKGROUNDS = ["opaque", "transparent"]

OPENAI_API_VERSION = "2025-04-01-preview"
FLUX_API_VERSION = "preview"

# Chroma key color appended to FLUX prompts when --background transparent.
# FLUX won't render this exact hex, but it biases the background toward magenta.
# Run chroma-key.py afterward to detect the actual color and strip it.
FLUX_CHROMA_KEY = "#FF00FE"

# Map deployment names to FLUX API slug (lowercased, dots become dashes)
FLUX_PATTERN = re.compile(r"^FLUX[.\-]", re.IGNORECASE)


def is_flux_model(deployment: str) -> bool:
    """Check if a deployment name is a FLUX model."""
    return bool(FLUX_PATTERN.match(deployment))


def flux_api_slug(deployment: str) -> str:
    """Convert deployment name to FLUX API path slug.

    e.g. "FLUX.2-pro" -> "flux-2-pro"
    """
    return deployment.lower().replace(".", "-")


def get_azure_token() -> str:
    """Get Azure AD token for Cognitive Services."""
    result = subprocess.run(
        ["az", "account", "get-access-token",
         "--resource", "https://cognitiveservices.azure.com",
         "--query", "accessToken", "-o", "tsv"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Failed to get Azure token: {result.stderr.strip()}", file=sys.stderr)
        print("Make sure you are logged in: az login", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def cognitiveservices_to_ai_services(endpoint: str) -> str:
    """Convert cognitiveservices.azure.com endpoint to services.ai.azure.com.

    e.g. https://foo.cognitiveservices.azure.com/ -> https://foo.services.ai.azure.com
    """
    return re.sub(
        r"\.cognitiveservices\.azure\.com",
        ".services.ai.azure.com",
        endpoint.rstrip("/"),
    )


def generate_openai(
    endpoint: str,
    deployment: str,
    prompt: str,
    size: str,
    quality: str,
    background: str,
    output_format: str,
    n: int,
) -> dict:
    """Call the OpenAI-compatible image generation API (gpt-image-*)."""
    token = get_azure_token()

    url = (
        f"{endpoint.rstrip('/')}/openai/deployments/{deployment}"
        f"/images/generations?api-version={OPENAI_API_VERSION}"
    )

    body = {
        "prompt": prompt,
        "n": n,
        "size": size,
        "quality": quality,
        "background": background,
        "output_format": output_format,
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        _handle_http_error(e)


def generate_flux(
    endpoint: str,
    deployment: str,
    prompt: str,
    size: str,
    n: int,
) -> dict:
    """Call the Black Forest Labs FLUX API.

    Uses the services.ai.azure.com endpoint with the
    /providers/blackforestlabs/v1/{slug} path.
    """
    token = get_azure_token()

    ai_endpoint = cognitiveservices_to_ai_services(endpoint)
    slug = flux_api_slug(deployment)

    url = (
        f"{ai_endpoint}/providers/blackforestlabs/v1/{slug}"
        f"?api-version={FLUX_API_VERSION}"
    )

    # FLUX uses width/height instead of size string
    if size == "auto":
        width, height = 1024, 1024
    else:
        width, height = (int(x) for x in size.split("x"))

    body = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "n": n,
        "model": deployment,
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        _handle_http_error(e)


def _handle_http_error(e: urllib.error.HTTPError) -> NoReturn:
    """Print HTTP error details and exit."""
    error_body = e.read().decode("utf-8", errors="replace")
    try:
        error_json = json.loads(error_body)
        msg = error_json.get("error", {}).get("message", error_body)
    except json.JSONDecodeError:
        msg = error_body
    print(f"API error ({e.code}): {msg}", file=sys.stderr)
    sys.exit(1)


def flux_chroma_prompt(prompt: str) -> str:
    """Append chroma key background instruction to a prompt for FLUX models."""
    return (
        f"{prompt} "
        f"The background must be solid {FLUX_CHROMA_KEY} color everywhere "
        f"that is not a foreground element. No gradients or patterns in the "
        f"background — only flat solid {FLUX_CHROMA_KEY}."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an image via Azure AI Foundry")
    parser.add_argument("--endpoint", required=True, help="Azure AI Services endpoint URL")
    parser.add_argument("--deployment", required=True, help="Model deployment name")
    parser.add_argument("--prompt", required=True, help="Image description")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--size", default="1024x1024", choices=VALID_SIZES,
                        help="Image size (default: 1024x1024)")
    parser.add_argument("--quality", default="medium", choices=VALID_QUALITIES,
                        help="Image quality (default: medium). Ignored for FLUX models.")
    parser.add_argument("--background", default="opaque", choices=VALID_BACKGROUNDS,
                        help="Background type (default: opaque). For FLUX models, transparency is emulated via chroma key.")
    parser.add_argument("--output-format", default="png", choices=["png"],
                        help="Output format (default: png)")
    parser.add_argument("-n", type=int, default=1, help="Number of images (default: 1)")
    args = parser.parse_args()

    flux = is_flux_model(args.deployment)
    flux_transparent = flux and args.background == "transparent"

    # For FLUX + transparent, inject chroma key into the prompt
    prompt = args.prompt
    if flux_transparent:
        prompt = flux_chroma_prompt(prompt)

    print(f"Generating image with {args.deployment}...")
    print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"  Size: {args.size}", end="")
    if flux:
        if flux_transparent:
            print(f"  (FLUX — chroma key {FLUX_CHROMA_KEY} for transparency)")
        else:
            print(f"  (FLUX — opaque, quality ignored)")
    else:
        print(f"  Quality: {args.quality}  Background: {args.background}")

    if flux:
        response = generate_flux(
            endpoint=args.endpoint,
            deployment=args.deployment,
            prompt=prompt,
            size=args.size,
            n=args.n,
        )
    else:
        response = generate_openai(
            endpoint=args.endpoint,
            deployment=args.deployment,
            prompt=prompt,
            size=args.size,
            quality=args.quality,
            background=args.background,
            output_format=args.output_format,
            n=args.n,
        )

    # Decode and save images
    images = response.get("data", [])
    if not images:
        print("No images in response", file=sys.stderr)
        sys.exit(1)

    for i, img in enumerate(images):
        b64 = img.get("b64_json")
        if not b64:
            print(f"Image {i}: no b64_json in response", file=sys.stderr)
            continue

        raw = base64.b64decode(b64)

        if len(images) == 1:
            out_path = args.output
        else:
            base, ext = os.path.splitext(args.output)
            out_path = f"{base}_{i}{ext}"

        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(raw)

        print(f"  Saved: {out_path} ({len(raw):,} bytes)")

    # Hint for FLUX + transparent
    if flux_transparent:
        print(f"\n  Next: remove chroma key background with:")
        print(f"  uv run skills/image-generation/scripts/chroma-key.py \\")
        print(f"    --input {args.output} --output {args.output}")

    # Print usage info (OpenAI only — FLUX doesn't return usage)
    usage = response.get("usage", {})
    if usage:
        print(f"  Tokens: {usage.get('total_tokens', 'N/A')} total "
              f"({usage.get('input_tokens', '?')} in, {usage.get('output_tokens', '?')} out)")


if __name__ == "__main__":
    main()
