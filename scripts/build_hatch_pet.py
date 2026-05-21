from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from collections import deque

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FRAMES = ROOT / "assets" / "frames"
RUN_DIR = ROOT / "runs" / "xiaodouni-codex-pet"
FRAMES_DIR = RUN_DIR / "frames"
FINAL_DIR = RUN_DIR / "final"
QA_DIR = RUN_DIR / "qa"

CELL_W = 192
CELL_H = 208

PET_ID = "xiaodouni-codex-pet"
DISPLAY_NAME = "暹罗猫小豆泥"
DESCRIPTION = "A cute Siamese Xiaodouni desktop pet for Codex coding companionship."

FrameSpec = dict[str, object]

IDLE_MODE = os.environ.get("XIAODOUNI_IDLE_MODE", "default").strip().lower()

DEFAULT_IDLE_SPECS: list[FrameSpec] = [
    {"path": "idle/00", "dy": 0, "scale": 1.00},
    {"path": "idle/00", "dy": 1, "scale": 1.006},
    {"path": "idle/00", "dy": 2, "scale": 1.012},
    {"path": "idle/02", "dy": 2, "scale": 1.010},
    {"path": "idle/00", "dy": 1, "scale": 1.006},
    {"path": "idle/00", "dy": 0, "scale": 1.00},
]

WORKLOOP_IDLE_SPECS: list[FrameSpec] = [
    {"path": "coding/00", "dx": -1, "dy": 1, "scale": 0.99},
    {"path": "coding/01", "dx": 0, "dy": 0, "scale": 0.99},
    {"path": "coding/02", "dx": 1, "dy": -1, "scale": 0.99},
    {"path": "coding/03", "dx": 0, "dy": 0, "scale": 0.99},
    {"path": "coding/02", "dx": 1, "dy": -1, "scale": 0.99},
    {"path": "coding/01", "dx": 0, "dy": 0, "scale": 0.99},
]


def idle_specs() -> list[FrameSpec]:
    if IDLE_MODE == "workloop":
        return WORKLOOP_IDLE_SPECS
    return DEFAULT_IDLE_SPECS


def load_font(size: int) -> ImageFont.ImageFont:
    for path in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


ROW_MAP: list[tuple[str, list[FrameSpec]]] = [
    (
        "idle",
        idle_specs(),
    ),
    (
        "running-right",
        [
            {"path": "celebrate/01", "dx": -22, "dy": 7, "rot": -8, "scale": 0.96, "main_only": True},
            {"path": "celebrate/02", "dx": -14, "dy": -2, "rot": -4, "scale": 1.00, "main_only": True},
            {"path": "celebrate/03", "dx": -5, "dy": -12, "rot": 2, "scale": 1.03, "main_only": True},
            {"path": "celebrate/02", "dx": 4, "dy": -4, "rot": 6, "scale": 1.00, "main_only": True},
            {"path": "celebrate/01", "dx": 12, "dy": 7, "rot": 9, "scale": 0.96, "main_only": True},
            {"path": "idle/04", "dx": 20, "dy": 2, "rot": 5, "scale": 0.98},
            {"path": "idle/00", "dx": 27, "dy": 5, "rot": 0, "scale": 0.96},
            {"path": "idle/01", "dx": 32, "dy": 4, "rot": -4, "scale": 0.96},
        ],
    ),
    (
        "running-left",
        [
            {"path": "celebrate/01", "dx": 22, "dy": 7, "rot": 8, "scale": 0.96, "mirror": True, "main_only": True},
            {"path": "celebrate/02", "dx": 14, "dy": -2, "rot": 4, "scale": 1.00, "mirror": True, "main_only": True},
            {"path": "celebrate/03", "dx": 5, "dy": -12, "rot": -2, "scale": 1.03, "mirror": True, "main_only": True},
            {"path": "celebrate/02", "dx": -4, "dy": -4, "rot": -6, "scale": 1.00, "mirror": True, "main_only": True},
            {"path": "celebrate/01", "dx": -12, "dy": 7, "rot": -9, "scale": 0.96, "mirror": True, "main_only": True},
            {"path": "idle/04", "dx": -20, "dy": 2, "rot": -5, "scale": 0.98, "mirror": True},
            {"path": "idle/00", "dx": -27, "dy": 5, "rot": 0, "scale": 0.96, "mirror": True},
            {"path": "idle/01", "dx": -32, "dy": 4, "rot": 4, "scale": 0.96, "mirror": True},
        ],
    ),
    (
        "waving",
        [
            {"path": "idle/00", "dy": 3, "scale": 0.98},
            {"path": "celebrate/01", "dx": -1, "dy": -2, "scale": 0.98, "main_only": True},
            {"path": "celebrate/02", "dx": 1, "dy": -4, "scale": 1.00, "main_only": True},
            {"path": "celebrate/01", "dx": -1, "dy": -1, "scale": 0.98, "main_only": True},
        ],
    ),
    (
        "jumping",
        [
            {"path": "idle/04", "dy": 11, "scale": 0.96, "celebrate_effect": 0},
            {"path": "celebrate/01", "dy": -7, "scale": 0.98, "main_only": True, "celebrate_effect": 1},
            {"path": "celebrate/02", "dy": -22, "scale": 1.04, "main_only": True, "celebrate_effect": 2},
            {"path": "celebrate/03", "dy": -11, "scale": 1.02, "main_only": True, "celebrate_effect": 3},
            {"path": "idle/00", "dy": 7, "scale": 0.98, "celebrate_effect": 4},
        ],
    ),
    (
        "failed",
        [
            {"path": "error/00"},
            {"path": "error/01", "dx": -1},
            {"path": "error/02", "dx": 1},
            {"path": "error/03", "dy": -1},
            {"path": "error/04"},
            {"path": "error/05", "dx": 1},
            {"path": "error/06", "dx": -1},
            {"path": "error/07"},
        ],
    ),
    (
        "waiting",
        [
            {"path": "idle/00", "dy": 1, "waiting_cue": 0},
            {"path": "idle/00", "dy": 0, "waiting_cue": 1},
            {"path": "idle/04", "dy": -1, "waiting_cue": 2},
            {"path": "idle/04", "dy": 0, "waiting_cue": 3},
            {"path": "idle/00", "dy": 1, "waiting_cue": 2},
            {"path": "idle/02", "dy": 1, "waiting_cue": 1},
        ],
    ),
    (
        "running",
        [
            {"path": "coding/00", "dx": -1, "dy": 1},
            {"path": "coding/01", "dx": 0, "dy": 0},
            {"path": "coding/02", "dx": 1, "dy": -1},
            {"path": "coding/03", "dx": 0, "dy": 0},
            {"path": "coding/02", "dx": 1, "dy": -1},
            {"path": "coding/01", "dx": 0, "dy": 0},
        ],
    ),
    (
        "review",
        [
            {"path": "peek/00", "dx": -8, "dy": 2, "scale": 0.98, "review_badge": 0},
            {"path": "peek/01", "dx": -5, "dy": 1, "scale": 0.98, "review_badge": 1},
            {"path": "peek/02", "dx": -2, "dy": 0, "scale": 0.98, "review_badge": 2},
            {"path": "peek/03", "dx": -5, "dy": 1, "scale": 0.98, "review_badge": 1},
            {"path": "peek/04", "dx": -8, "dy": 2, "scale": 0.98, "review_badge": 0},
            {"path": "peek/05", "dx": -10, "dy": 2, "scale": 0.98, "review_badge": 1},
        ],
    ),
]


def resolve_frame(path_spec: str) -> Path:
    state, stem = path_spec.split("/", 1)
    path = SOURCE_FRAMES / state / f"{stem}.png"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def keep_main_components(image: Image.Image, min_area: int = 80, keep_nearby: bool = True) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    width, height = rgba.size
    alpha_bytes = alpha.load()
    visited: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []

    for y in range(height):
        for x in range(width):
            if (x, y) in visited or alpha_bytes[x, y] == 0:
                continue
            queue: deque[tuple[int, int]] = deque([(x, y)])
            visited.add((x, y))
            component: list[tuple[int, int]] = []
            while queue:
                px, py = queue.popleft()
                component.append((px, py))
                for nx, ny in ((px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)):
                    if (
                        0 <= nx < width
                        and 0 <= ny < height
                        and (nx, ny) not in visited
                        and alpha_bytes[nx, ny] > 0
                    ):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            if len(component) >= min_area:
                components.append(component)

    if not components:
        return rgba

    components.sort(key=len, reverse=True)
    main = components[0]
    xs = [point[0] for point in main]
    main_left, main_right = min(xs), max(xs)
    keep: set[tuple[int, int]] = set(main)

    if keep_nearby:
        for component in components[1:]:
            area = len(component)
            cx = sum(point[0] for point in component) / area
            if area > len(main) * 0.08 and main_left - 16 <= cx <= main_right + 16:
                keep.update(component)

    pixels = rgba.load()
    for y in range(height):
        for x in range(width):
            if alpha_bytes[x, y] > 0 and (x, y) not in keep:
                pixels[x, y] = (0, 0, 0, 0)
    return rgba


def normalize_frame(spec: FrameSpec) -> Image.Image:
    path = resolve_frame(str(spec["path"]))
    source = keep_main_components(
        Image.open(path).convert("RGBA"),
        keep_nearby=not bool(spec.get("main_only", False)),
    )
    if bool(spec.get("mirror", False)):
        source = ImageOps.mirror(source)
    scale = float(spec.get("scale", 1.0))
    if scale != 1.0:
        source = source.resize(
            (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
            Image.Resampling.LANCZOS,
        )
    rotation = float(spec.get("rot", 0))
    if rotation:
        source = source.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)

    source.thumbnail((CELL_W - 18, CELL_H - 18), Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    x = (CELL_W - source.width) // 2 + int(spec.get("dx", 0))
    y = CELL_H - source.height - 8 + int(spec.get("dy", 0))
    cell.alpha_composite(source, (x, max(0, y)))
    remove_chroma_halo(cell)
    if "celebrate_effect" in spec:
        add_celebration_effect(cell, int(spec["celebrate_effect"]))
    if "waiting_cue" in spec:
        add_waiting_cue(cell, int(spec["waiting_cue"]))
    if "review_badge" in spec:
        add_review_badge(cell, int(spec["review_badge"]))
    return cell


def clear_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def remove_chroma_halo(cell: Image.Image) -> None:
    pixels = cell.load()
    for y in range(cell.height):
        for x in range(cell.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            semi_transparent_halo = a < 245 and g > 120 and g > r + 30 and g > b + 30
            opaque_chroma_residue = g > 115 and r < 50 and b < 50
            if semi_transparent_halo or opaque_chroma_residue:
                pixels[x, y] = (0, 0, 0, 0)


def add_celebration_effect(cell: Image.Image, phase: int) -> None:
    draw = ImageDraw.Draw(cell)
    palettes = [
        [(245, 84, 92, 255), (56, 152, 255, 255), (255, 203, 53, 255), (90, 199, 112, 255)],
        [(255, 142, 48, 255), (83, 108, 255, 255), (255, 91, 171, 255), (76, 201, 180, 255)],
    ]
    colors = palettes[phase % len(palettes)]
    pieces = [
        (53, 59, 8, -10),
        (72, 40, -8, 8),
        (103, 35, 10, 9),
        (128, 56, -10, -8),
        (41, 90, -7, 7),
        (143, 90, 8, -7),
        (66, 116, 10, -6),
        (124, 119, -8, 6),
    ]
    drift = [0, -5, -9, -4, 2][phase]
    for index, (x, y, dx, dy) in enumerate(pieces):
        px = x + phase * dx // 6
        py = y + drift + phase * dy // 7
        color = colors[index % len(colors)]
        if index % 3 == 0:
            draw.line((px, py, px + 12, py + 5), fill=color, width=4)
        elif index % 3 == 1:
            draw.rounded_rectangle((px, py, px + 8, py + 5), radius=2, fill=color)
        else:
            draw.arc((px, py, px + 15, py + 12), start=20, end=260, fill=color, width=3)


def add_waiting_cue(cell: Image.Image, phase: int) -> None:
    draw = ImageDraw.Draw(cell)
    font = load_font(25)
    x_shift = [0, 2, 4, 2][phase % 4]
    bubble = (118 + x_shift, 36, 159 + x_shift, 74)
    tail = [
        (121 + x_shift, 70),
        (111 + x_shift, 84),
        (132 + x_shift, 73),
    ]
    draw.rounded_rectangle(bubble, radius=12, fill=(255, 255, 244, 255), outline=(24, 28, 22, 255), width=3)
    draw.polygon(tail, fill=(255, 255, 244, 255), outline=(24, 28, 22, 255))
    draw.line((122 + x_shift, 70, 113 + x_shift, 82), fill=(24, 28, 22, 255), width=3)
    draw.text((132 + x_shift, 38), "?", fill=(24, 28, 22, 255), font=font)
    if phase % 4 in (1, 2):
        draw.ellipse((112 + x_shift, 88, 119 + x_shift, 95), fill=(92, 160, 255, 255), outline=(24, 28, 22, 255), width=1)


def add_review_badge(cell: Image.Image, phase: int) -> None:
    draw = ImageDraw.Draw(cell)
    y = 44 + [0, -2, 0][phase % 3]
    draw.rounded_rectangle((119, y, 166, y + 25), radius=7, fill=(244, 251, 255, 255), outline=(24, 28, 22, 255), width=3)
    draw.line((130, y + 13, 138, y + 20, 154, y + 6), fill=(44, 150, 78, 255), width=4)


def write_request() -> None:
    request = {
        "pet_id": PET_ID,
        "display_name": DISPLAY_NAME,
        "description": DESCRIPTION,
        "source": "assets/source/xiaodouni_sprite_sheet_green.png",
        "notes": (
            "Built from the generated Siamese Xiaodouni green-screen source. "
            "The user's 16 semantic states are mapped into the Codex 9-row custom pet contract. "
            f"Idle mode: {IDLE_MODE}."
        ),
        "state_mapping": {
            "idle": (
                "coding idle / running fallback workloop"
                if IDLE_MODE == "workloop"
                else "idle / 待机眨眼"
            ),
            "running-right": "drag or jump-right style movement using celebration source frames",
            "running-left": "mirrored running-right row",
            "waving": "happy paw wave greeting",
            "jumping": "surprised / complete jump",
            "failed": "error / cry / failed task",
            "waiting": "needs input / approval prompt",
            "running": "coding active work",
            "review": "peek_screen / review ready",
        },
    }
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    (RUN_DIR / "pet_request.json").write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_frames() -> None:
    clear_dir(FRAMES_DIR)
    rows = []

    for state, specs in ROW_MAP:
        state_dir = FRAMES_DIR / state
        state_dir.mkdir(parents=True, exist_ok=True)
        for index, spec in enumerate(specs):
            normalize_frame(spec).save(state_dir / f"{index:02d}.png")
        rows.append(
            {
                "state": state,
                "count": len(specs),
                "source_frames": [spec["path"] for spec in specs],
                "method": "components",
                "mirrored": any(bool(spec.get("mirror", False)) for spec in specs),
            }
        )

    manifest = {
        "cell": {"width": CELL_W, "height": CELL_H},
        "chroma_key": {"rgb": [0, 255, 0]},
        "rows": rows,
    }
    (FRAMES_DIR / "frames-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if not (SOURCE_FRAMES / "manifest.json").exists():
        raise FileNotFoundError("Run `python scripts/prepare_frames.py` before building the hatch pet.")
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    write_request()
    write_frames()
    print(f"Wrote hatch-pet frame root: {FRAMES_DIR}")
    print(f"Wrote pet request: {RUN_DIR / 'pet_request.json'}")


if __name__ == "__main__":
    main()
