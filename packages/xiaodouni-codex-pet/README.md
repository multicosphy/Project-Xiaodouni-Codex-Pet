# Xiaodouni Codex Pet Package

Copy this whole folder into your Codex pet directory:

```powershell
$PET_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
New-Item -ItemType Directory -Force -Path (Join-Path $PET_HOME "pets") | Out-Null
Copy-Item -Recurse -Force ".\xiaodouni-codex-pet" (Join-Path $PET_HOME "pets\xiaodouni-codex-pet")
```

Codex should then see:

```text
<CODEX_HOME or %USERPROFILE%\.codex>\pets\xiaodouni-codex-pet\pet.json
<CODEX_HOME or %USERPROFILE%\.codex>\pets\xiaodouni-codex-pet\spritesheet.webp
```

`pet.json` must stay UTF-8 without BOM.

This is an unofficial fan package for Nobeko's Xiaodouni / Azukisan character. Character identity and artwork are not open licensed by this repository; see the root `ASSET-LICENSE.md` and `NOTICE.md`.
