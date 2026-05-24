# Xiaodouni Codex Pet Package

**Language:** [中文](#中文) | [English](#english) | [日本語](#日本語)

## 中文

把整个 `xiaodouni-codex-pet` 文件夹复制到 Codex 的 `pets` 目录：

```powershell
$PET_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
New-Item -ItemType Directory -Force -Path (Join-Path $PET_HOME "pets") | Out-Null
Copy-Item -Recurse -Force ".\xiaodouni-codex-pet" (Join-Path $PET_HOME "pets\xiaodouni-codex-pet")
```

Codex 应能看到：

```text
<CODEX_HOME or %USERPROFILE%\.codex>\pets\xiaodouni-codex-pet\pet.json
<CODEX_HOME or %USERPROFILE%\.codex>\pets\xiaodouni-codex-pet\spritesheet.webp
```

`pet.json` 必须保持 UTF-8 without BOM。

这是 Nobeko 的 Xiaodouni / Azukisan 角色的非官方粉丝 package。角色身份和 artwork 不由本仓库开放授权；见仓库根目录的 `ASSET-LICENSE.md` 和 `NOTICE.md`。

## English

Copy the whole `xiaodouni-codex-pet` folder into your Codex `pets` directory:

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

## 日本語

`xiaodouni-codex-pet` フォルダ全体を Codex の `pets` ディレクトリへコピーします。

```powershell
$PET_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
New-Item -ItemType Directory -Force -Path (Join-Path $PET_HOME "pets") | Out-Null
Copy-Item -Recurse -Force ".\xiaodouni-codex-pet" (Join-Path $PET_HOME "pets\xiaodouni-codex-pet")
```

Codex から次のファイルが見える必要があります。

```text
<CODEX_HOME or %USERPROFILE%\.codex>\pets\xiaodouni-codex-pet\pet.json
<CODEX_HOME or %USERPROFILE%\.codex>\pets\xiaodouni-codex-pet\spritesheet.webp
```

`pet.json` は UTF-8 without BOM のままにしてください。

これは Nobeko の Xiaodouni / Azukisan キャラクターの非公式ファン package です。キャラクター identity と artwork は、このリポジトリからオープンライセンスされません。リポジトリルートの `ASSET-LICENSE.md` と `NOTICE.md` を参照してください。
