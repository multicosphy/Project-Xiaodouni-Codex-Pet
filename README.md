# Xiaodouni Codex Desktop Pet

暹罗猫小豆泥的 Codex 自定义桌宠包，以及用于复现、调整和重新生成它的本地 Python/Tkinter 原型。

If you only want to use the pet in Codex, copy the packaged folder:

```powershell
$PET_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
New-Item -ItemType Directory -Force -Path (Join-Path $PET_HOME "pets") | Out-Null
Copy-Item -Recurse -Force ".\packages\xiaodouni-codex-pet" (Join-Path $PET_HOME "pets\xiaodouni-codex-pet")
```

After copying, the installed files should be:

```text
%USERPROFILE%\.codex\pets\xiaodouni-codex-pet\pet.json
%USERPROFILE%\.codex\pets\xiaodouni-codex-pet\spritesheet.webp
```

If `CODEX_HOME` is set, use `%CODEX_HOME%\pets\xiaodouni-codex-pet\` instead.

## Layout

- `pet.py`: runs the local transparent Tkinter desktop pet.
- `assets/source/xiaodouni_sprite_sheet_green.png`: source green-screen sprite sheet.
- `scripts/prepare_frames.py`: crops source frames into transparent action frames.
- `assets/frames/`: generated local desktop-pet frames and `manifest.json`.
- `scripts/build_hatch_pet.py`: maps local frames into the Codex custom pet atlas structure.
- `runs/xiaodouni-codex-pet/`: generated hatch-pet frames, final atlas, validation, and QA output.
- `packages/xiaodouni-codex-pet/`: packaged Codex custom pet files.

## Requirements

- Windows with PowerShell.
- Python 3.12 was verified in this workspace.
- Pillow is required because the code imports `PIL`.
- Tkinter is required by `pet.py`.

Install the Python dependency for local development:

```powershell
python -m pip install -r requirements.txt
```

## Run the Desktop Pet

```powershell
python .\scripts\prepare_frames.py
python .\pet.py
```

Optional display settings:

```powershell
python .\pet.py --scale 1.2 --fps 8
```

Controls:

- Left-button drag: move the pet window.
- Left-button double-click: switch to the next action.
- Right-click: open the action menu and exit command.
- `Esc`: exit.

## Build the Codex Pet Package

Regenerate local frames and the hatch-pet frame root:

```powershell
python .\scripts\prepare_frames.py
python .\scripts\build_hatch_pet.py
```

The generated Codex atlas is `1536x1872`, arranged as `8 x 9` cells. Each cell is `192x208`.

The fixed Codex row order is:

| Row | State |
| --- | --- |
| 0 | `idle` |
| 1 | `running-right` |
| 2 | `running-left` |
| 3 | `waving` |
| 4 | `jumping` |
| 5 | `failed` |
| 6 | `waiting` |
| 7 | `running` |
| 8 | `review` |

Set `XIAODOUNI_IDLE_MODE=workloop` before running `scripts/build_hatch_pet.py` to generate the alternate workloop idle row. If unset, the script uses `default`.

## Verify

Python syntax check:

```powershell
python -m py_compile pet.py scripts\prepare_frames.py scripts\build_hatch_pet.py
```

Hatch-pet validation, when the local `hatch-pet` skill scripts are installed:

```powershell
$HATCH = "$env:USERPROFILE\.codex\skills\hatch-pet\scripts"
python "$HATCH\inspect_frames.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --json-out ".\runs\xiaodouni-codex-pet\qa\review.json" --require-components
python "$HATCH\compose_atlas.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --output ".\runs\xiaodouni-codex-pet\final\spritesheet.png" --webp-output ".\runs\xiaodouni-codex-pet\final\spritesheet.webp"
python "$HATCH\validate_atlas.py" ".\runs\xiaodouni-codex-pet\final\spritesheet.webp" --json-out ".\runs\xiaodouni-codex-pet\final\validation.json"
```

Expected validation result: `runs/xiaodouni-codex-pet/qa/review.json` and `runs/xiaodouni-codex-pet/final/validation.json` should report `"ok": true` and no errors.

## Generated Files

Do not hand-edit generated image outputs. Regenerate them through the scripts.

Generated paths include:

- `assets/frames/`
- `runs/xiaodouni-codex-pet/frames/`
- `runs/xiaodouni-codex-pet/final/`
- `runs/xiaodouni-codex-pet/qa/`
- `packages/xiaodouni-codex-pet/spritesheet.webp`
- `__pycache__/`

`packages/xiaodouni-codex-pet/pet.json` must remain UTF-8 without BOM. Windows PowerShell 5 `Set-Content -Encoding UTF8` can write a BOM, which may cause Codex to ignore the custom pet.

## Contributing

Issues and pull requests are welcome. Useful contributions include:

- improving the atlas mapping in `scripts/build_hatch_pet.py`;
- adding cleaner source art or alternate animation states;
- improving installation docs for different Codex setups;
- adding reproducible validation or release packaging.

For generated raster assets, update the source script or source image first, then regenerate and validate the output. Do not edit individual generated frames by hand unless the change is explicitly a package repair.

## Known Gaps

- No lint, format, typecheck, test, or CI configuration was found.
- The current folder is not a Git repository.
- In this environment, `rg.exe` failed with `Access is denied`; PowerShell `Get-ChildItem -Recurse` was used for repository inspection.
