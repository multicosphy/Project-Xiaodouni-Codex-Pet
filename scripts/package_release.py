from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "packages" / "xiaodouni-codex-pet"
DIST_DIR = ROOT / "dist"
LEGAL_FILES = ("LICENSE", "ASSET-LICENSE.md", "NOTICE.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a zip package for the Xiaodouni Codex pet release."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Release version without the leading v, for example 1.0.0.",
    )
    return parser.parse_args()


def validate_version(version: str) -> str:
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        raise SystemExit(
            "Version must look like 1.0.0, optionally followed by a prerelease or build suffix."
        )
    return version


def validate_package() -> None:
    if not PACKAGE_DIR.is_dir():
        raise SystemExit(f"Missing package directory: {PACKAGE_DIR}")

    pet_json_path = PACKAGE_DIR / "pet.json"
    spritesheet_path = PACKAGE_DIR / "spritesheet.webp"
    if not pet_json_path.is_file():
        raise SystemExit(f"Missing required package file: {pet_json_path}")
    if not spritesheet_path.is_file():
        raise SystemExit(f"Missing required package file: {spritesheet_path}")

    raw_pet_json = pet_json_path.read_bytes()
    if raw_pet_json.startswith(b"\xef\xbb\xbf"):
        raise SystemExit("pet.json must be UTF-8 without BOM.")

    pet_config = json.loads(raw_pet_json.decode("utf-8"))
    expected_spritesheet = pet_config.get("spritesheetPath")
    if expected_spritesheet != "spritesheet.webp":
        raise SystemExit(
            f"pet.json spritesheetPath must be spritesheet.webp, got {expected_spritesheet!r}."
        )

    for filename in LEGAL_FILES:
        if not (ROOT / filename).is_file():
            raise SystemExit(f"Missing legal notice file: {filename}")


def write_release_zip(version: str) -> Path:
    DIST_DIR.mkdir(exist_ok=True)
    output_path = DIST_DIR / f"xiaodouni-codex-pet-v{version}.zip"

    with zipfile.ZipFile(output_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(PACKAGE_DIR.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(PACKAGE_DIR.parent))

        docs_root = Path("xiaodouni-codex-pet") / "docs"
        for filename in LEGAL_FILES:
            archive.write(ROOT / filename, docs_root / filename)

    return output_path


def main() -> None:
    args = parse_args()
    version = validate_version(args.version)
    validate_package()
    output_path = write_release_zip(version)
    print(output_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
