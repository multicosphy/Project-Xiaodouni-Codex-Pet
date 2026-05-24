# Xiaodouni Codex Desktop Pet

**言語 / Language:** [中文](README.md) | [English](README.en.md) | 日本語

シャム猫 Xiaodouni の Codex カスタムデスクトップペット用パッケージと、それを再現・調整・再生成するための Python/Tkinter ローカルプロトタイプです。

## Codex へのインストール

Codex で使うだけの場合は、release ページから `xiaodouni-codex-pet-vX.Y.Z.zip` をダウンロードして展開し、`xiaodouni-codex-pet` フォルダを Codex の `pets` ディレクトリへコピーします。

```powershell
$PET_HOME = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
New-Item -ItemType Directory -Force -Path (Join-Path $PET_HOME "pets") | Out-Null
Copy-Item -Recurse -Force ".\xiaodouni-codex-pet" (Join-Path $PET_HOME "pets\xiaodouni-codex-pet")
```

コピー後、次のファイルが存在している必要があります。

```text
%USERPROFILE%\.codex\pets\xiaodouni-codex-pet\pet.json
%USERPROFILE%\.codex\pets\xiaodouni-codex-pet\spritesheet.webp
```

`CODEX_HOME` を設定している場合は、次の場所を使ってください。

```text
%CODEX_HOME%\pets\xiaodouni-codex-pet\
```

## プロジェクト構成

- `pet.py`: 透明な Tkinter デスクトップペットのローカルプロトタイプを実行します。
- `assets/source/xiaodouni_sprite_sheet_green.png`: 元のグリーンスクリーン sprite sheet。
- `scripts/prepare_frames.py`: 元画像から透明なアクションフレームを切り出します。
- `assets/frames/`: 生成されたローカルデスクトップペット用フレームと `manifest.json`。
- `scripts/build_hatch_pet.py`: ローカルフレームを Codex カスタムペット用 atlas 構造へ変換します。
- `scripts/package_release.py`: GitHub Release に添付する zip パッケージを生成します。
- `runs/xiaodouni-codex-pet/`: 生成された hatch-pet フレーム、最終 atlas、検証、QA 出力。
- `packages/xiaodouni-codex-pet/`: そのままインストールできる Codex カスタムペットパッケージ。

## 必要環境

- Windows + PowerShell。
- このワークスペースでは Python 3.12 を確認済みです。
- スクリプトと `pet.py` は `PIL` を import するため Pillow が必要です。
- `pet.py` には Tkinter が必要です。

ローカル開発用依存関係をインストールします。

```powershell
python -m pip install -r requirements.txt
```

## ローカルデスクトップペットの実行

```powershell
python .\scripts\prepare_frames.py
python .\pet.py
```

表示設定の例：

```powershell
python .\pet.py --scale 1.2 --fps 8
```

操作：

- 左ボタンドラッグ：ペットウィンドウを移動。
- 左ボタンダブルクリック：次のアクションへ切り替え。
- 右クリック：アクションメニューと終了コマンドを開く。
- `Esc`：終了。

## Codex ペットパッケージのビルド

ローカルフレームと hatch-pet フレームルートを再生成します。

```powershell
python .\scripts\prepare_frames.py
python .\scripts\build_hatch_pet.py
```

生成される Codex atlas は `1536x1872` で、`8 x 9` セル構成です。各セルは `192x208` です。

固定の Codex 行順：

| 行 | 状態 |
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

`scripts/build_hatch_pet.py` を実行する前に `XIAODOUNI_IDLE_MODE=workloop` を設定すると、alternate workloop idle row を生成できます。未設定の場合は `default` を使います。

## Release パッケージの作成

```powershell
python .\scripts\package_release.py --version 1.0.0
```

出力：

```text
dist\xiaodouni-codex-pet-v1.0.0.zip
```

zip には `xiaodouni-codex-pet/` インストールディレクトリと、`LICENSE`、`ASSET-LICENSE.md`、`NOTICE.md` が含まれます。

## 検証

Python 構文チェック：

```powershell
python -m py_compile pet.py scripts\prepare_frames.py scripts\build_hatch_pet.py scripts\package_release.py
```

Release パッケージ生成チェック：

```powershell
python .\scripts\package_release.py --version 1.0.0
```

ローカルに `hatch-pet` skill スクリプトがある場合は、atlas 検証も実行できます。

```powershell
$HATCH = "$env:USERPROFILE\.codex\skills\hatch-pet\scripts"
python "$HATCH\inspect_frames.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --json-out ".\runs\xiaodouni-codex-pet\qa\review.json" --require-components
python "$HATCH\compose_atlas.py" --frames-root ".\runs\xiaodouni-codex-pet\frames" --output ".\runs\xiaodouni-codex-pet\final\spritesheet.png" --webp-output ".\runs\xiaodouni-codex-pet\final\spritesheet.webp"
python "$HATCH\validate_atlas.py" ".\runs\xiaodouni-codex-pet\final\spritesheet.webp" --json-out ".\runs\xiaodouni-codex-pet\final\validation.json"
```

期待される結果：`runs/xiaodouni-codex-pet/qa/review.json` と `runs/xiaodouni-codex-pet/final/validation.json` が `"ok": true` を報告し、errors がないこと。

## 生成ファイル

生成された画像出力を手で編集しないでください。スクリプトから再生成してください。

生成または派生されるパス：

- `assets/frames/`
- `runs/xiaodouni-codex-pet/frames/`
- `runs/xiaodouni-codex-pet/final/`
- `runs/xiaodouni-codex-pet/qa/`
- `packages/xiaodouni-codex-pet/spritesheet.webp`
- `dist/`
- `__pycache__/`

`packages/xiaodouni-codex-pet/pet.json` は UTF-8 without BOM のままにしてください。PowerShell 5 の `Set-Content -Encoding UTF8` は BOM を書き込むことがあり、Codex がカスタムペットを認識しない原因になります。

## ライセンスと IP に関する注意

これは Nobeko の Xiaodouni / Azukisan キャラクターの非公式ファンプロジェクトです。本プロジェクトは Nobeko、KADOKAWA、またはいかなる公式権利者にも所属せず、承認・後援・許諾されたものではありません。

- コード、スクリプト、ドキュメント、リポジトリ設定は MIT License で提供されます。`LICENSE` を参照してください。
- キャラクター名、キャラクター identity、ビジュアル素材、生成フレーム、spritesheet、パッケージ化されたペット artwork は、このリポジトリからオープンライセンスされません。`ASSET-LICENSE.md` を参照してください。

関連する権利者から許可を得ている場合、または適用法上の別の有効な法的根拠がある場合を除き、このリポジトリ内の Xiaodouni キャラクター artwork を再利用、再配布、remix、商用利用、または派生作品として公開しないでください。

本プロジェクトの artwork は、人間の指示のもと OpenAI/Codex ツールで生成され、リポジトリ所有者によって選択、配置、清理、パッケージ化、検証されました。AI provenance と権利に関する注記は `NOTICE.md` を参照してください。

## コントリビュート

Issue と pull request を歓迎します。主な貢献例：

- `scripts/build_hatch_pet.py` の atlas mapping 改善。
- Codex 設定ごとのインストール文書の改善。
- 再現可能な検証や release packaging の追加。
- 自分が投稿する権利を持つ、オリジナルで非侵害の素材または設定。

生成された raster assets については、まず元スクリプトまたは元画像を更新し、その後に再生成して検証してください。明示的なパッケージ修復でない限り、個別の生成フレームを手で編集しないでください。

コードまたはドキュメントを貢献する場合、その貢献を MIT License で提供することに同意したものとします。関連する権利者の許可がない限り、第三者のキャラクターアート、公式商品画像、logo、著作権保護素材、または Nobeko/Xiaodouni の派生素材を投稿しないでください。

## 既知の不足

- 現在、lint、format、typecheck、test、CI の設定は見つかっていません。
- この環境では以前 `rg.exe` が `Access is denied` で失敗したため、リポジトリ調査には PowerShell `Get-ChildItem -Recurse` を使用しました。
