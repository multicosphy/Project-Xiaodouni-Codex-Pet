# Repository Guidance for Codex

## Project Snapshot

This repository contains a Windows Python/Tkinter desktop pet prototype and a packaged Codex custom pet named `xiaodouni-codex-pet`.

Primary entry points:

- `pet.py` runs the local desktop pet UI from `assets/frames/manifest.json`.
- `scripts/prepare_frames.py` crops transparent action frames from `assets/source/xiaodouni_sprite_sheet_green.png`.
- `scripts/build_hatch_pet.py` maps the local action frames into the 9-row Codex custom pet atlas contract.
- `packages/xiaodouni-codex-pet/` contains the installable Codex pet package.

## Environment

- Shell: PowerShell on Windows.
- Verified Python version in this workspace: `Python 3.12.7`.
- Runtime dependency: Pillow, imported as `PIL` by the scripts and `pet.py`.
- No dependency manifest was found (`requirements.txt`, `pyproject.toml`, or package manager lockfile are absent).
- This directory is not currently a Git repository, so do not assume `git status`, branches, or diffs are available.
- `rg.exe` failed with `Access is denied` in this environment. Use PowerShell recursion such as `Get-ChildItem -Recurse` if `rg` is unavailable.

## Commands

Run the desktop pet:

```powershell
python .\scripts\prepare_frames.py
python .\pet.py
```

Optional runtime arguments:

```powershell
python .\pet.py --scale 1.2 --fps 8
```

Regenerate the Codex pet frame root:

```powershell
python .\scripts\prepare_frames.py
python .\scripts\build_hatch_pet.py
```

Validate Python syntax:

```powershell
python -m py_compile pet.py scripts\prepare_frames.py scripts\build_hatch_pet.py
```

Validate the hatch-pet output when the local hatch-pet skill is installed:

```powershell
$HATCH = "$env:USERPROFILE\.codex\skills\hatch-pet\scripts"
python "$HATCH\inspect_frames.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --json-out ".\runs\xiaodouni-codex-pet\qa\review.json" --require-components
python "$HATCH\compose_atlas.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --output ".\runs\xiaodouni-codex-pet\final\spritesheet.png" --webp-output ".\runs\xiaodouni-codex-pet\final\spritesheet.webp"
python "$HATCH\validate_atlas.py" ".\runs\xiaodouni-codex-pet\final\spritesheet.webp" --json-out ".\runs\xiaodouni-codex-pet\final\validation.json"
```

No lint, format, typecheck, test, or CI commands were discovered. Do not invent them; if a future task needs them, add the relevant tool configuration first.

## Project Conventions

- Keep behavior changes out of documentation-only tasks.
- Treat `scripts/prepare_frames.py` and `scripts/build_hatch_pet.py` as the source of truth for generated frame and atlas structure.
- The Codex custom pet atlas is `1536x1872`, with `8 x 9` cells of `192x208`.
- The Codex row order is fixed: `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`.
- `XIAODOUNI_IDLE_MODE=workloop` switches the generated atlas idle row to the workloop frame spec in `scripts/build_hatch_pet.py`; the default idle mode is `default`.
- Keep `pet.json` encoded as UTF-8 without BOM. PowerShell 5 `Set-Content -Encoding UTF8` may write a BOM, which can cause Codex to ignore the custom pet.

## Generated Files and Edit Boundaries

Avoid hand-editing generated raster assets or generated validation outputs. Regenerate them through the scripts instead.

Generated or derived paths:

- `assets/frames/`
- `runs/xiaodouni-codex-pet/frames/`
- `runs/xiaodouni-codex-pet/final/`
- `runs/xiaodouni-codex-pet/qa/`
- `packages/xiaodouni-codex-pet/spritesheet.webp`
- `__pycache__/` and `scripts/__pycache__/`

Stable source/config paths:

- `assets/source/xiaodouni_sprite_sheet_green.png`
- `pet.py`
- `scripts/prepare_frames.py`
- `scripts/build_hatch_pet.py`
- `packages/xiaodouni-codex-pet/pet.json`

Only edit generated package files when the task explicitly asks to repair or republish the pet package, and verify the atlas afterward.

## Safety Rules

- Delete files only by moving them to the system Recycle Bin. Confirm scope with the user before any large deletion. Do not use permanent `rm`-style deletion.
- If a command is unavailable, blocked by permissions, or depends on missing local tools, report that blocker explicitly.
- Prefer small, behavior-preserving changes unless the user requests implementation work.
- Do not assume network access.

## Done When

For future Codex tasks in this repository, work is done when:

- The requested files are changed and no unrelated behavior was altered.
- Relevant generation or validation commands above have been run, or a clear blocker is reported.
- For Python edits, `python -m py_compile pet.py scripts\prepare_frames.py scripts\build_hatch_pet.py` passes.
- For pet package edits, `inspect_frames.py`, `compose_atlas.py`, and `validate_atlas.py` pass and the output JSON has no errors.
- The final response lists changed files, commands run, results, blockers, and any recommended follow-up.
