# Contributing

Contributions are welcome through GitHub issues and pull requests.

## License of contributions

By submitting a code, script, documentation, or repository-configuration contribution, you agree that it is licensed under the MIT License.

Do not submit third-party character art, Nobeko/Xiaodouni derivative artwork, official product images, logos, copyrighted material, or trademarked material unless you have permission from the relevant rights holder.

## Development checks

Run the basic syntax check after Python edits:

```powershell
python -m py_compile pet.py scripts\prepare_frames.py scripts\build_hatch_pet.py
```

Run the pet generation and validation flow after package or visual changes:

```powershell
python .\scripts\prepare_frames.py
python .\scripts\build_hatch_pet.py
$HATCH = "$env:USERPROFILE\.codex\skills\hatch-pet\scripts"
python "$HATCH\inspect_frames.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --json-out ".\runs\xiaodouni-codex-pet\qa\review.json" --require-components
python "$HATCH\compose_atlas.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --output ".\runs\xiaodouni-codex-pet\final\spritesheet.png" --webp-output ".\runs\xiaodouni-codex-pet\final\spritesheet.webp"
python "$HATCH\validate_atlas.py" ".\runs\xiaodouni-codex-pet\final\spritesheet.webp" --json-out ".\runs\xiaodouni-codex-pet\final\validation.json"
```
