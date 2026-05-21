from __future__ import annotations

import argparse
import json
import random
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "assets" / "frames" / "manifest.json"
CHROMA = "#00ff00"

ACTION_LABELS = {
    "idle": "待机眨眼",
    "coding": "敲代码",
    "fix_bug": "修 Bug",
    "error": "报错摊手",
    "loading": "加载等待",
    "celebrate": "完成庆祝",
    "peek": "偷看屏幕",
    "sleep": "困倦睡觉",
    "supervise": "监督工作",
}

ACTION_ORDER = [
    "idle",
    "coding",
    "fix_bug",
    "error",
    "loading",
    "celebrate",
    "peek",
    "sleep",
    "supervise",
]


class DesktopPet:
    def __init__(self, scale: float = 1.0, fps: int = 8) -> None:
        if not MANIFEST.exists():
            raise FileNotFoundError(
                "Missing frame manifest. Run `python scripts/prepare_frames.py` first."
            )

        self.scale = scale
        self.delay = max(30, int(1000 / fps))
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg=CHROMA)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", CHROMA)

        self.label = tk.Label(self.root, bg=CHROMA, bd=0, highlightthickness=0)
        self.label.pack()

        self.frames = self.load_frames()
        self.action = "idle"
        self.frame_index = 0
        self.drag_origin: tuple[int, int] | None = None
        self.idle_loops = 0

        self.root.geometry("+120+220")
        self.bind_events()
        self.animate()

    def load_frames(self) -> dict[str, list[ImageTk.PhotoImage]]:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        loaded: dict[str, list[ImageTk.PhotoImage]] = {}

        for action, paths in data["actions"].items():
            loaded[action] = []
            for rel_path in paths:
                image = Image.open(ROOT / rel_path).convert("RGBA")
                if self.scale != 1.0:
                    size = (
                        max(1, round(image.width * self.scale)),
                        max(1, round(image.height * self.scale)),
                    )
                    image = image.resize(size, Image.Resampling.LANCZOS)
                loaded[action].append(ImageTk.PhotoImage(image))

        return loaded

    def bind_events(self) -> None:
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<Double-Button-1>", lambda _event: self.next_action())
        self.root.bind("<Button-3>", self.show_menu)
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

    def start_drag(self, event: tk.Event) -> None:
        self.drag_origin = (event.x_root - self.root.winfo_x(), event.y_root - self.root.winfo_y())

    def drag(self, event: tk.Event) -> None:
        if self.drag_origin is None:
            return
        dx, dy = self.drag_origin
        self.root.geometry(f"+{event.x_root - dx}+{event.y_root - dy}")

    def show_menu(self, event: tk.Event) -> None:
        menu = tk.Menu(self.root, tearoff=False)
        for action in ACTION_ORDER:
            menu.add_command(
                label=ACTION_LABELS[action],
                command=lambda selected=action: self.set_action(selected),
            )
        menu.add_separator()
        menu.add_command(label="退出", command=self.root.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    def set_action(self, action: str) -> None:
        if action not in self.frames:
            return
        self.action = action
        self.frame_index = 0
        self.idle_loops = 0

    def next_action(self) -> None:
        current = ACTION_ORDER.index(self.action)
        self.set_action(ACTION_ORDER[(current + 1) % len(ACTION_ORDER)])

    def animate(self) -> None:
        action_frames = self.frames[self.action]
        self.label.configure(image=action_frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(action_frames)

        if self.action != "idle" and self.frame_index == 0:
            self.set_action("idle")
        elif self.action == "idle" and self.frame_index == 0:
            self.idle_loops += 1
            if self.idle_loops >= random.randint(4, 8):
                self.set_action(random.choice(ACTION_ORDER[1:]))

        self.root.after(self.delay, self.animate)

    def run(self) -> None:
        self.root.mainloop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Xiaodouni Codex desktop pet.")
    parser.add_argument("--scale", type=float, default=1.0, help="Display scale, for example 0.8 or 1.4.")
    parser.add_argument("--fps", type=int, default=8, help="Animation frames per second.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    DesktopPet(scale=args.scale, fps=args.fps).run()


if __name__ == "__main__":
    main()
