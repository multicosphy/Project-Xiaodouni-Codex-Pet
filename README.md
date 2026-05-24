# Xiaodouni Codex Desktop Pet

**语言 / Language / 言語:** 中文 | [English](README.en.md) | [日本語](README.ja.md)

暹罗猫小豆泥的 Codex 自定义桌宠包，以及用于复现、调整和重新生成它的本地 Python/Tkinter 原型。

## 直接安装到 Codex

如果你只想在 Codex 里使用桌宠，下载 release 里的 `xiaodouni-codex-pet-vX.Y.Z.zip`，解压后把 `xiaodouni-codex-pet` 文件夹复制到 Codex 的 `pets` 目录：

```powershell
$PET_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
New-Item -ItemType Directory -Force -Path (Join-Path $PET_HOME "pets") | Out-Null
Copy-Item -Recurse -Force ".\xiaodouni-codex-pet" (Join-Path $PET_HOME "pets\xiaodouni-codex-pet")
```

复制后应存在：

```text
%USERPROFILE%\.codex\pets\xiaodouni-codex-pet\pet.json
%USERPROFILE%\.codex\pets\xiaodouni-codex-pet\spritesheet.webp
```

如果设置了 `CODEX_HOME`，请改用：

```text
%CODEX_HOME%\pets\xiaodouni-codex-pet\
```

## 项目结构

- `pet.py`：运行本地透明 Tkinter 桌宠原型。
- `assets/source/xiaodouni_sprite_sheet_green.png`：源绿幕 sprite sheet。
- `scripts/prepare_frames.py`：把源图裁剪为透明动作帧。
- `assets/frames/`：生成的本地桌宠动作帧和 `manifest.json`。
- `scripts/build_hatch_pet.py`：把本地动作帧映射成 Codex 自定义桌宠 atlas 结构。
- `scripts/package_release.py`：生成可上传到 GitHub Release 的安装 zip 包。
- `runs/xiaodouni-codex-pet/`：生成的 hatch-pet 帧、最终 atlas、验证和 QA 输出。
- `packages/xiaodouni-codex-pet/`：可直接安装的 Codex 自定义桌宠包。

## 环境要求

- Windows + PowerShell。
- 本工作区已验证 Python 3.12。
- 需要 Pillow，因为脚本和 `pet.py` 会导入 `PIL`。
- `pet.py` 需要 Tkinter。

安装本地开发依赖：

```powershell
python -m pip install -r requirements.txt
```

## 运行本地桌宠原型

```powershell
python .\scripts\prepare_frames.py
python .\pet.py
```

可选显示参数：

```powershell
python .\pet.py --scale 1.2 --fps 8
```

操作：

- 鼠标左键拖动：移动桌宠窗口。
- 鼠标左键双击：切换到下一个动作。
- 右键：打开动作菜单和退出命令。
- `Esc`：退出。

## 构建 Codex 桌宠包

重新生成本地帧和 hatch-pet 帧根目录：

```powershell
python .\scripts\prepare_frames.py
python .\scripts\build_hatch_pet.py
```

生成的 Codex atlas 尺寸为 `1536x1872`，排列为 `8 x 9` 个单元格，每格 `192x208`。

固定行顺序：

| 行 | 状态 |
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

运行 `scripts/build_hatch_pet.py` 前设置 `XIAODOUNI_IDLE_MODE=workloop`，可以生成 alternate workloop idle row。未设置时使用 `default`。

## 生成 Release 安装包

```powershell
python .\scripts\package_release.py --version 1.0.0
```

输出：

```text
dist\xiaodouni-codex-pet-v1.0.0.zip
```

压缩包内包含 `xiaodouni-codex-pet/` 安装目录，以及 `LICENSE`、`ASSET-LICENSE.md`、`NOTICE.md`。

## 验证

Python 语法检查：

```powershell
python -m py_compile pet.py scripts\prepare_frames.py scripts\build_hatch_pet.py scripts\package_release.py
```

本地安装包生成检查：

```powershell
python .\scripts\package_release.py --version 1.0.0
```

如果本地安装了 `hatch-pet` skill 脚本，可以继续做 atlas 验证：

```powershell
$HATCH = "$env:USERPROFILE\.codex\skills\hatch-pet\scripts"
python "$HATCH\inspect_frames.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --json-out ".\runs\xiaodouni-codex-pet\qa\review.json" --require-components
python "$HATCH\compose_atlas.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --output ".\runs\xiaodouni-codex-pet\final\spritesheet.png" --webp-output ".\runs\xiaodouni-codex-pet\final\spritesheet.webp"
python "$HATCH\validate_atlas.py" ".\runs\xiaodouni-codex-pet\final\spritesheet.webp" --json-out ".\runs\xiaodouni-codex-pet\final\validation.json"
```

期望结果：`runs/xiaodouni-codex-pet/qa/review.json` 和 `runs/xiaodouni-codex-pet/final/validation.json` 报告 `"ok": true` 且没有 errors。

## 生成文件

不要手工编辑生成的图像输出。请通过脚本重新生成。

生成或派生路径包括：

- `assets/frames/`
- `runs/xiaodouni-codex-pet/frames/`
- `runs/xiaodouni-codex-pet/final/`
- `runs/xiaodouni-codex-pet/qa/`
- `packages/xiaodouni-codex-pet/spritesheet.webp`
- `dist/`
- `__pycache__/`

`packages/xiaodouni-codex-pet/pet.json` 必须保持 UTF-8 without BOM。PowerShell 5 的 `Set-Content -Encoding UTF8` 可能写入 BOM，导致 Codex 忽略自定义桌宠。

## 许可证和 IP 声明

这是 Nobeko 的 Xiaodouni / Azukisan 角色的非官方粉丝项目。本项目不隶属于 Nobeko、KADOKAWA 或任何官方权利方，也未获得其认可、赞助或授权。

- 代码、脚本、文档和仓库配置使用 MIT License。见 `LICENSE`。
- 角色名称、角色身份、视觉素材、生成帧、spritesheet 和打包桌宠 artwork 不由本仓库开放授权。见 `ASSET-LICENSE.md`。

除非你已获得相关权利方许可，或你的使用在适用法律下另有合法依据，否则不要复用、再分发、remix、商业化或发布本仓库中的 Xiaodouni 角色 artwork 衍生作品。

本项目 artwork 由 OpenAI/Codex 工具在人类指导下生成，并由仓库所有者选择、编排、清理、打包和验证。AI provenance 和权利说明见 `NOTICE.md`。

## 贡献

欢迎 issue 和 pull request。适合贡献的方向包括：

- 改进 `scripts/build_hatch_pet.py` 的 atlas 映射；
- 改进安装文档或不同 Codex 设置下的使用说明；
- 增加可复现的验证或 release packaging；
- 提交你有权贡献的原创、非侵权素材或配置。

对于生成的 raster assets，请优先修改源脚本或源图，然后重新生成并验证输出。除非明确是在修复包，否则不要手工编辑单个生成帧。

贡献代码或文档即表示你同意你的贡献按 MIT License 授权。不要提交第三方角色图、官方商品图、logo、受版权保护素材或 Nobeko/Xiaodouni 衍生素材，除非你已获得相关权利方许可。

## 已知缺口

- 当前未发现 lint、format、typecheck、test 或 CI 配置。
- 在本环境中，`rg.exe` 曾因 `Access is denied` 失败；仓库检查使用 PowerShell `Get-ChildItem -Recurse`。
