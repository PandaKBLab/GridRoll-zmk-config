# GridRoll

[English](README.md) · [简体中文](README.zh-CN.md) · **日本語** · [Deutsch](README.de.md)

PandaKB GridRoll 用 ZMK ファームウェア。47 キー、左エンコーダー、右 PAW3222 トラックボール、USB/Bluetooth、ZMK Studio/DYA Studio に対応します。**右側が PC、左側が右側に無線接続**します。機器名は **GridRoll**。PCB・回路図・配線・内部回路資料は公開しません。

## 更新

成功した [Actions](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml) の **GridRoll-firmware** ZIP には左・右・settings-reset の UF2 三つだけを含みます。対応する左右の通常ファームウェアを使い、**通常更新で settings-reset を書き込まないでください**。保存設定とペアリングは保持します。[初回導入](docs/first-flash.md)。成果物は 30 日間保存されます。

## 4 レイヤー

| レイヤー | 用途・操作 | エンコーダー CW/CCW |
|---|---|---|
| L0 Base | QWERTY、左 Space／右 Enter は通常キー | ホイール上／下 |
| L1 Mouse | ボールで自動、Fn+B で手動、Esc で終了 | ホイール上／下 |
| L2 Symbols | 左 Space 左隣の Symbols を保持 | ホイール上／下 |
| L3 Function | 右 Enter 右隣の Fn を保持、ボールスクロールも有効 | 音量上／下 |
| L4–L7 | 編集用の空き、キーと回転は無動作 | なし |

最下段は Ctrl、Alt、GUI、中クリック、Symbols、**Space**｜**Enter**、Fn、ボール開口、左、下、右。従来の 3 行目右端 Enter は右 Shift です。[全キー値と図](docs/keymap.md)。

保存済み配置は更新しても残ります。新配置を使うには旧配置をエクスポートしてから **ZMK Studio のキー配置 Restore Stock Settings** を実行し、保存します。ペアリングの消去は不要です。DYA の回転割当は独立し、L0–L2 ホイール上/下、L3 音量上/下、L4–L7 無動作に変更します。

## トラックボールと接続

既定値は承認済みのネイティブ **798 CPI（約 800 DPI）**。DYA 倍率 1/1 なら L1 左 4 行 6 列（Space 位置）を保持して 1/4、約 **200 DPI**、離すと通常速度です。J/K/H は左/右/中クリック、L は戻る、セミコロンは進む、U/I と O/P は縦/横ホイールです。Mouse の M または Base の Fn を保持するとボールでスクロールします。打鍵保護 200ms、終了 1200ms、ドラッグ保護を保持します。

Fn+A/S/D/F/G で BLE プロファイル 0–4、必要な場合だけ Fn+Z で選択中のペアリングを消去します。Fn+X は USB、Fn+C は BLE。PC に USB 認識されると自動で USB を優先し、充電のみでは切り替えません。

**ZMK Studio/DYA Studio は常時ロック解除**で、解除キーや切断時の再ロックは不要です。有線設定は右 USB・USB 出力・正しいシリアルポートを選びます。無線は同じ PC とペアリングして BLE 出力にし、**Fn+V** の後に DYA で再スキャンします。

発見ウィンドウは最大 **60 秒**。新しい BLE 接続や USB から BLE への選択でも一度開き、アイドル・USB 出力・切断・期限で追加広告を終了します。通常操作で無限に延長せず、既存 GATT 接続を意図的に切断しません。解除キーではありません。接続済みで広告を止めていた処理を修正し、スキャン応答に Studio UUID を追加します。Windows/ブラウザー実機の接続・保存は未検証です。[詳細](docs/studio-wireless.md)。

## 電力と表示

30 秒無入力でアイドル、電池で 15 分後に深いスリープ。左右それぞれのキーで復帰し、ボールや回転による深睡眠からの復帰は保証しません。USB 給電側は起動を維持します。無線 Studio の変更は睡眠前に保存してください。発見処理は入力を偽装せず、恒久的な広告や追加の電池ポーリングを行いません。

赤 LED は右の主機接続表示と各側の低電池表示、アイドル/睡眠では消灯。青はハードウェアの充電周期表示で、消灯だけでは満充電を保証しません。[LED](docs/led-status.md)。実機の電流・操作感・復帰は検証が必要です。

[保守](docs/maintenance.md) · [検証](docs/validation.md)。依存は固定、独自コードは MIT、[第三者ライセンス](THIRD_PARTY_NOTICES.md)。
