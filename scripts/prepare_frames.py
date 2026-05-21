from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source" / "xiaodouni_sprite_sheet_green.png"
OUT_DIR = ROOT / "assets" / "frames"
KEY = (0, 255, 0)


def crop_box(cx: int, y1: int, y2: int, width: int, image_width: int) -> tuple[int, int, int, int]:
    half = width // 2
    return max(0, cx - half), y1, min(image_width, cx + half), y2


def remove_green(image: Image.Image, tolerance: int = 72) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if (
                abs(r - KEY[0]) <= tolerance
                and abs(g - KEY[1]) <= tolerance
                and abs(b - KEY[2]) <= tolerance
            ):
                pixels[x, y] = (0, 0, 0, 0)
            elif g > 180 and r < 80 and b < 80:
                pixels[x, y] = (r, g, b, 0)
    return rgba


def trim_alpha(image: Image.Image, padding: int = 8) -> Image.Image:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return image
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)
    return image.crop((left, top, right, bottom))


def make_entries(action: str, row: tuple[int, int], centers: Iterable[int], width: int) -> list[dict]:
    y1, y2 = row
    return [
        {"action": action, "cx": int(cx), "y1": y1, "y2": y2, "width": width}
        for cx in centers
    ]


FRAME_PLAN: list[dict] = []

# The generated source image came back as a 4-row sprite sheet. These crop centers
# select the best available poses and repeat a few near-duplicates where the model
# produced fewer poses than requested for an action.
FRAME_PLAN += make_entries("idle", (36, 184), [80, 192, 304, 416, 530, 416], 118)
FRAME_PLAN += make_entries("coding", (36, 184), [660, 765, 875, 990, 1105, 765, 990, 1105], 146)
FRAME_PLAN += make_entries("fix_bug", (36, 184), [1215, 1330, 1430, 1545, 1670, 2055], 154)
FRAME_PLAN += make_entries("error", (206, 372), [80, 190, 305, 420, 530, 640, 755, 530], 124)
FRAME_PLAN += make_entries("loading", (206, 372), [870, 980, 1095, 1210, 1210, 1210], 146)
FRAME_PLAN += make_entries("celebrate", (206, 372), [1370, 1505, 1630, 1765, 1900, 2055], 168)
FRAME_PLAN += make_entries("peek", (374, 510), [82, 198, 320, 442, 562, 690, 810, 320], 100)
FRAME_PLAN += make_entries("sleep", (374, 510), [975, 1175, 1350, 1530, 1700, 2045], 214)
FRAME_PLAN += make_entries("supervise", (520, 690), [90, 225, 355, 615, 750, 1130, 1875, 2100], 136)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing source sprite sheet: {SOURCE}")

    source = Image.open(SOURCE).convert("RGB")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, list[str]] = {}
    counts: dict[str, int] = {}

    for entry in FRAME_PLAN:
        action = entry["action"]
        index = counts.get(action, 0)
        counts[action] = index + 1

        box = crop_box(entry["cx"], entry["y1"], entry["y2"], entry["width"], source.width)
        frame = trim_alpha(remove_green(source.crop(box)))

        action_dir = OUT_DIR / action
        action_dir.mkdir(parents=True, exist_ok=True)
        name = f"{index:02d}.png"
        frame.save(action_dir / name)
        manifest.setdefault(action, []).append(str((Path("assets") / "frames" / action / name).as_posix()))

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "source": str(SOURCE.relative_to(ROOT).as_posix()),
                "actions": manifest,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {sum(len(v) for v in manifest.values())} frames to {OUT_DIR}")
    for action, frames in manifest.items():
        print(f"{action}: {len(frames)}")


if __name__ == "__main__":
    main()
