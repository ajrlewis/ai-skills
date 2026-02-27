#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import urllib.request
from dataclasses import dataclass


RAW_BASE = "https://raw.githubusercontent.com/nostr-protocol/nips/{ref}/{nip:02d}.md"


@dataclass(slots=True)
class NipEntry:
    nip: int
    url: str
    title: str
    status_hint: str
    content_sha256: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync selected NIP specs into a lockfile.")
    parser.add_argument("--nips", required=True, help="Comma-separated NIP numbers, e.g. 1,7,23,65")
    parser.add_argument("--out", required=True, help="Output lockfile path")
    parser.add_argument("--ref", default="master", help="Git ref in nostr-protocol/nips")
    return parser.parse_args()


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "nips-lock-sync/1.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8")


def extract_title(markdown: str, nip: int) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return f"NIP-{nip:02d}"


def detect_status_hint(markdown: str) -> str:
    head = markdown[:1200].lower()
    if "deprecated" in head:
        return "deprecated"
    if "draft" in head:
        return "draft-or-proposed"
    return "active-or-unspecified"


def parse_nip_list(raw: str) -> list[int]:
    out: list[int] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if not re.fullmatch(r"\d{1,3}", token):
            raise ValueError(f"Invalid NIP token: {token}")
        out.append(int(token))
    if not out:
        raise ValueError("No NIPs provided")
    return sorted(set(out))


def build_entries(nips: list[int], ref: str) -> list[NipEntry]:
    entries: list[NipEntry] = []
    for nip in nips:
        url = RAW_BASE.format(ref=ref, nip=nip)
        content = fetch_text(url)
        entries.append(
            NipEntry(
                nip=nip,
                url=url,
                title=extract_title(content, nip),
                status_hint=detect_status_hint(content),
                content_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            )
        )
    return entries


def main() -> int:
    args = parse_args()
    nips = parse_nip_list(args.nips)
    entries = build_entries(nips, args.ref)

    payload = {
        "source": {
            "repo": "nostr-protocol/nips",
            "ref": args.ref,
        },
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "nips": [
            {
                "nip": entry.nip,
                "url": entry.url,
                "title": entry.title,
                "status_hint": entry.status_hint,
                "content_sha256": entry.content_sha256,
            }
            for entry in entries
        ],
    }

    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=True, indent=2)
        handle.write("\n")
    print(f"Wrote {len(entries)} NIPs to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
