#!/usr/bin/env python3
"""
Free Image Generation using Hugging Face Inference API (FLUX.1-schnell).
No billing required. Just a free HF token.

Usage:
    python3 generate_image_free.py --prompt "your description" --filename "output.png"
    python3 generate_image_free.py --prompt "your description" --filename "output.png" --model "black-forest-labs/FLUX.1-schnell"
"""

import argparse
import os
import sys
import urllib.request
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Free image generation via Hugging Face")
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--filename", "-f", required=True, help="Output filename")
    parser.add_argument("--model", "-m", default="black-forest-labs/FLUX.1-schnell",
                        help="HuggingFace model (default: FLUX.1-schnell)")
    parser.add_argument("--token", "-t", default=None, help="HF token (or set HF_TOKEN env)")
    args = parser.parse_args()

    token = args.token or os.environ.get("HF_TOKEN")
    if not token:
        print("Error: No HF token. Set HF_TOKEN env or pass --token", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"https://router.huggingface.co/hf-inference/models/{args.model}"
    data = json.dumps({"inputs": args.prompt}).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    print(f"Generating image with {args.model}...")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            image_data = resp.read()
            content_type = resp.headers.get("Content-Type", "")

            if "json" in content_type:
                error = json.loads(image_data)
                print(f"Error: {error}", file=sys.stderr)
                sys.exit(1)

            with open(output_path, "wb") as f:
                f.write(image_data)

            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
            print(f"MEDIA:{full_path}")

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
