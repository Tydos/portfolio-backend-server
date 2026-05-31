"""Recursively upload a directory of .jpg/.jpeg images to the portfolio backend.

The server cannot read your local disk, so this script walks the directory
client-side and feeds the files to POST /api/upload-batch in chunks.

Usage:
    python upload_folder.py <directory> [--category nature]
                            [--url http://localhost:8000] [--key <api-key>]
                            [--batch-size 25]

Examples:
    python upload_folder.py "C:\\Users\\me\\Pictures\\portfolio"
    python upload_folder.py ./photos --category landscape --batch-size 50
"""

import argparse
import os
import sys
from pathlib import Path

import httpx

IMAGE_EXTS = {".jpg", ".jpeg"}


def find_images(directory: Path) -> list[Path]:
    """Return every .jpg/.jpeg file under `directory`, recursively, sorted."""
    return sorted(
        p for p in directory.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )


def chunked(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recursively upload a folder of images to /api/upload-batch"
    )
    parser.add_argument("directory", type=Path, help="Folder to scan recursively")
    parser.add_argument("--category", default="nature", help="Category for the whole run")
    parser.add_argument("--url", default=os.getenv("UPLOAD_URL", "http://localhost:8000"),
                        help="Server base URL (default: http://localhost:8000)")
    parser.add_argument("--key", default=os.getenv("ADMIN_API_KEY", "prasad"),
                        help="Admin API key (X-API-Key)")
    parser.add_argument("--batch-size", type=int, default=25,
                        help="Files per request (default: 25)")
    args = parser.parse_args()

    if not args.directory.is_dir():
        sys.exit(f"Not a directory: {args.directory}")

    images = find_images(args.directory)
    if not images:
        sys.exit(f"No .jpg/.jpeg files found under {args.directory}")

    print(f"Found {len(images)} image(s) under {args.directory}")

    # Warn about duplicate basenames — the bucket/DB key on filename only, so
    # same-named files in different subfolders will collide and be skipped.
    seen: dict[str, Path] = {}
    for p in images:
        if p.name.lower() in seen:
            print(f"  ! duplicate filename '{p.name}' "
                  f"({p} vs {seen[p.name.lower()]}) — second will be skipped")
        else:
            seen[p.name.lower()] = p

    endpoint = f"{args.url.rstrip('/')}/api/upload-batch"
    totals = {"uploaded": 0, "skipped": 0, "failed": 0}

    with httpx.Client(timeout=120) as client:
        for batch in chunked(images, args.batch_size):
            files = [("files", (p.name, p.read_bytes(), "image/jpeg")) for p in batch]
            resp = client.post(
                endpoint,
                headers={"X-API-Key": args.key},
                data={"category": args.category},
                files=files,
            )
            resp.raise_for_status()
            result = resp.json()
            for key in totals:
                totals[key] += len(result.get(key, []))
            for item in result.get("uploaded", []):
                print(f"  uploaded  {item['filename']}")
            for item in result.get("skipped", []):
                print(f"  skipped   {item['filename']} ({item['reason']})")
            for item in result.get("failed", []):
                print(f"  failed    {item['filename']} ({item['error']})")

    print(f"\nDone: {totals['uploaded']} uploaded, "
          f"{totals['skipped']} skipped, {totals['failed']} failed")


if __name__ == "__main__":
    main()
