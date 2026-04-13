# /// script
# requires-python = ">=3.10"
# ///
"""Discover image-capable model deployments on an Azure AI Services account.

Usage:
    uv run skills/image-generation/scripts/discover-models.py \
        --resource-group <RG> --account <ACCOUNT_NAME>

Requires: az CLI logged in to the correct subscription.
"""

import argparse
import json
import subprocess
import sys


from typing import Any


def run_az(args: list[str]) -> Any:
    result = subprocess.run(
        ["az"] + args + ["--output", "json"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"az command failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover image-capable deployments")
    parser.add_argument("--resource-group", required=True, help="Azure resource group")
    parser.add_argument("--account", required=True, help="Cognitive Services account name")
    args = parser.parse_args()

    # Get account info
    account = run_az([
        "cognitiveservices", "account", "show",
        "--name", args.account,
        "--resource-group", args.resource_group,
    ])
    endpoint = account["properties"]["endpoint"]
    location = account["location"]
    kind = account["kind"]

    print(f"Account:  {args.account}")
    print(f"Kind:     {kind}")
    print(f"Location: {location}")
    print(f"Endpoint: {endpoint}")
    print()

    # List all deployments
    deployments = run_az([
        "cognitiveservices", "account", "deployment", "list",
        "--name", args.account,
        "--resource-group", args.resource_group,
    ])

    # Filter for image-capable deployments
    image_deployments = []
    for d in deployments:
        caps = d.get("properties", {}).get("capabilities", {})
        if caps.get("imageGenerations") == "true" or caps.get("imageEdits") == "true":
            image_deployments.append(d)

    if not image_deployments:
        print("No image-capable deployments found.")
        print("\nAll deployments:")
        for d in deployments:
            model = d["properties"]["model"]
            print(f"  {d['name']} ({model['format']}/{model['name']})")
        sys.exit(0)

    print(f"Found {len(image_deployments)} image-capable deployment(s):\n")

    for d in image_deployments:
        model = d["properties"]["model"]
        caps = d["properties"]["capabilities"]
        rate_limits = d["properties"].get("rateLimits") or []

        print(f"  Deployment:    {d['name']}")
        print(f"  Model:         {model['name']} ({model['format']})")
        print(f"  Version:       {model.get('version', 'N/A')}")
        print(f"  Capabilities:  ", end="")
        cap_list = []
        if caps.get("imageGenerations") == "true":
            cap_list.append("generation")
        if caps.get("imageEdits") == "true":
            cap_list.append("editing")
        print(", ".join(cap_list))

        for rl in rate_limits:
            if rl["key"] == "request":
                print(f"  Rate limit:    {int(rl['count'])} req/{int(rl['renewalPeriod'])}s")

        print()

    # Print usage hint
    print("To generate an image:")
    print(f"  uv run skills/image-generation/scripts/generate-image.py \\")
    print(f"    --endpoint {endpoint} \\")
    print(f"    --deployment {image_deployments[0]['name']} \\")
    print(f'    --prompt "Your description" \\')
    print(f"    --output image.png")


if __name__ == "__main__":
    main()
