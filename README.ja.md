# GridRoll

[English](README.md) · [简体中文](README.zh-CN.md) · **日本語** · [Deutsch](README.de.md)

PandaKB GridRoll 分割キーボード用の ZMK ファームウェアです。47 キー、左側エンコーダー、右側 PAW3222 トラックボール、USB／Bluetooth、ZMK Studio と DYA Studio に対応します。

**右側が PC に接続する Central** で、左側は右側へ無線接続します。キーボード名、Bluetooth 名、USB 製品名はすべて **GridRoll** です。

このリポジトリにはファームウェア、ビルドツール、使用説明のみを含みます。PCB プロジェクト、回路図、配線、ネットリスト、内部回路資料は配布しません。ファームウェアに必要な GPIO 定義はボードのソースに保持します。

## ダウンロードと書き込み

1. [Build GridRoll firmware](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml) で成功した実行を開きます。
2. ダウンロードする ZIP は **GridRoll-firmware** 一つだけです。内容は **GridRoll-left.uf2**、**GridRoll-right.uf2**、**GridRoll-settings-reset.uf2** の三つだけです。
3. 各側をブートローダーモードにし、左側に GridRoll-left.uf2、右側に GridRoll-right.uf2 をコピーします。設定初期化用イメージは通常使用には使えません。
4. GridRoll ブートローダーが未導入の場合は、[初回書き込み手順](docs/first-flash.md)を参照してください。初回書き込みパッケージは別途ビルドするもので、この ZIP には含まれません。

成果物の保存期間は 30 日です。ビルド成功はソフトウェア検証であり、実機試験の合格を意味しません。

## Bluetooth と Studio

PC は**右側の GridRoll** とペアリングします。見つからない場合は未使用のプロファイルを選ぶか、現在のプロファイルと PC 側の古いペアリングを削除してください。通常の更新では保存済みペアリングは消去されません。

標準配置では **Fn + Mouse** で System レイヤーに入り、最上段の **Q** 位置でプロファイル 0、**Backspace** でそのプロファイルの消去、**U** で BLE 出力を選択します。Studio で保存した配置では位置が異なる場合があります。

[ZMK Studio](https://zmk.studio/) または [DYA Studio](https://studio.dya.cormoran.works/) では、**右側を USB 接続**し、USB 出力とシリアルポートを選択します。**編集は初めからロック解除状態で、解除キーは不要です。アイドルや切断でも再ロックしません。** 同じポートを使う他のページを閉じ、変更を保存してください。更新では Studio／DYA 設定を保持します。DYA で回転を手動補正していた場合は、その追加補正を解除してください。取り付け方向補正はマウス／スクロール処理より前に適用されます。

両方の UI でキー配置を編集でき、DYA では既存の mouse／scroll パラメーターも調整できます。CI で固定した DYA 拡張プロトコルとロック無効設定を確認します。センサー画像など未実装の DYA 専用機能は含みません。

## 省電力と復帰

- 無入力 **30 秒**でアイドル状態になり、Bluetooth を維持します。
- バッテリー動作中、無入力 **15 分**でディープスリープに入ります。スリープ中の左右それぞれでキーを押し、Bluetooth の再接続を待ちます。トラックボールやエンコーダーの回転による復帰は保証しません。
- USB 給電中の側は USB／Studio 用に起動状態を保ちます。スリープでは RAM 内の未保存編集が失われるため、Studio の変更を保存してください。
- トラックボールは MOTION 割り込みと既存のセンサー休止設定を使用します。実際の消費電流と復帰動作は実機で確認してください。
- BLE では移動量を保持し、レポートを最低 **8 ms** 間隔にまとめます。USB は即時出力を維持します。右側は **7.5 ms** の接続間隔とゼロの peripheral latency を要求しますが、実際の値はホストが決定します。接続待機中の消費電力が増える可能性があり、滑らかさと消費電流の実機確認が必要です。

[保守説明](docs/maintenance.md)、[対応ファームウェア](docs/hardware.md)、[検証状況](docs/validation.md)を参照してください。依存関係は config/west.yml に固定されています。独自コードは MIT ライセンスです。依存コードのライセンスは[第三者通知](THIRD_PARTY_NOTICES.md)に記載しています。
