# GridRoll

[English](README.md) · [简体中文](README.zh-CN.md) · **日本語** · [Deutsch](README.de.md)

PandaKB GridRoll 分割キーボード用の ZMK ファームウェアです。47 キー、左側エンコーダー、右側 PAW3222 トラックボール、USB／Bluetooth、ZMK Studio と DYA Studio に対応します。

**右側が PC に接続する Central** で、左側は右側へ無線接続します。キーボード名、Bluetooth 名、USB 製品名はすべて **GridRoll** です。

このリポジトリにはファームウェア、ビルドツール、使用説明のみを含みます。PCB プロジェクト、回路図、配線、ネットリスト、内部回路資料は配布しません。ファームウェアに必要な GPIO 定義はボードのソースに保持します。

## ダウンロードと書き込み

1. [Build GridRoll firmware](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml) で成功した実行を開きます。
2. **GridRoll-left** と **GridRoll-right** をダウンロードします。各 ZIP に対応する UF2 が入っています。**GridRoll-firmware** には診断用・設定初期化用イメージ、ログ、ビルド設定も含まれます。
3. 各側をブートローダーモードにし、左側に GridRoll-left.uf2、右側に GridRoll-right.uf2 をコピーします。設定初期化用イメージは通常使用には使えません。
4. GridRoll ブートローダーが未導入の場合は、[初回書き込み手順](docs/first-flash.md)を参照してください。

成果物の保存期間は 30 日です。ビルド成功はソフトウェア検証であり、実機試験の合格を意味しません。

## Bluetooth と Studio

PC は**右側の GridRoll** とペアリングします。見つからない場合は未使用のプロファイルを選ぶか、現在のプロファイルと PC 側の古いペアリングを削除してください。通常の更新では保存済みペアリングは消去されません。

標準配置では **Fn + Mouse** で System レイヤーに入り、最上段の **Q** 位置でプロファイル 0、**Backspace** でそのプロファイルの消去、**U** で BLE 出力を選択します。Studio で保存した配置では位置が異なる場合があります。

[ZMK Studio](https://zmk.studio/) または [DYA Studio](https://studio.dya.cormoran.works/) では、**右側を USB 接続**して USB 出力を選択し、System レイヤーの左上キーで編集ロックを解除します。同じシリアルポートを使う他のページを閉じ、変更を保存してください。更新では Studio／DYA 設定を保持します。DYA でトラックボールの回転を手動補正していた場合は、その追加補正を解除してください。新しい取り付け方向補正はマウス／スクロール処理より前に適用されます。

## 省電力と復帰

- 無入力 **30 秒**でアイドル状態になり、Bluetooth を維持します。
- バッテリー動作中、無入力 **15 分**でディープスリープに入ります。スリープ中の左右それぞれでキーを押し、Bluetooth の再接続を待ちます。トラックボールやエンコーダーの回転による復帰は保証しません。
- USB 給電中の側は USB／Studio 用に起動状態を保ちます。スリープでは RAM 内の未保存編集が失われるため、Studio の変更を保存してください。
- トラックボールは MOTION 割り込みと既存のセンサー休止設定を使用します。実際の消費電流と復帰動作は実機で確認してください。

[保守説明](docs/maintenance.md)、[対応ファームウェア](docs/hardware.md)、[検証状況](docs/validation.md)を参照してください。依存関係は config/west.yml に固定されています。独自コードは MIT ライセンスです。依存コードのライセンスは[第三者通知](THIRD_PARTY_NOTICES.md)に記載しています。
