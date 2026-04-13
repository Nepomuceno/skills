# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx", "python-dotenv"]
# ///
"""Shared helpers for voice-clone scripts.

Not meant to be run directly -- imported by the other scripts.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Load .env from the current working directory."""
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def get_azure_config() -> dict[str, str]:
    """Return Azure configuration from environment variables."""
    region = os.environ.get("AZURE_REGION", "eastus2")
    subdomain = os.environ.get("AZURE_CUSTOM_SUBDOMAIN", "")
    api_version = os.environ.get("API_VERSION", "2024-02-01-preview")

    if subdomain:
        base_url = f"https://{subdomain}.cognitiveservices.azure.com"
        tts_path = "/tts/cognitiveservices/v1"
        voices_path = "/tts/cognitiveservices/voices/list"
    else:
        base_url = f"https://{region}.api.cognitive.microsoft.com"
        tts_path = "/cognitiveservices/v1"
        voices_path = "/cognitiveservices/voices/list"

    return {
        "region": region,
        "subdomain": subdomain,
        "api_version": api_version,
        "base_url": base_url,
        "tts_path": tts_path,
        "voices_path": voices_path,
    }


def get_token() -> str:
    """Get an Azure AD access token via the az CLI."""
    try:
        result = subprocess.run(
            [
                "az", "account", "get-access-token",
                "--resource", "https://cognitiveservices.azure.com",
                "--query", "accessToken",
                "-o", "tsv",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        token = result.stdout.strip()
        if not token:
            print("ERROR: Empty token returned. Run 'az login' first.", file=sys.stderr)
            sys.exit(1)
        return token
    except FileNotFoundError:
        print("ERROR: 'az' CLI not found. Install it: https://aka.ms/installazurecli", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to get Azure AD token: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def safe_name(name: str) -> str:
    """Convert a display name to a URL/file-safe slug."""
    slug = name.lower().replace(" ", "-")
    return re.sub(r"[^a-z0-9-]", "", slug)


def resolve_path(p: str) -> Path:
    """Resolve a path, making relative paths absolute from cwd."""
    path = Path(p)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def human_size(path: Path) -> str:
    """Return a human-readable file size."""
    size = path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def log_step(msg: str) -> None:
    """Print a visible step header."""
    print()
    print("=" * 60)
    print(f"  {msg}")
    print("=" * 60)
