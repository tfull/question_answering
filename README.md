# Erica (Question Answering)

This is a Japanese question answering system.

日本語の質問応答システム

# 導入手順

## 1. ファイルを配置

リポジトリ内のファイルを動作させたい場所へ配置する。

## 2. Configファイルの設定

この Readme があるディレクトリと同じ場所に、 config.template.yml があるため、それをコピーして同一ディレクトリ上に config.yml として配置する。  
別の場所に保存したい場合は、環境変数 `ERICA_CONFIG_PATH` にパスを指定して、その場所へ保存する。

## 3. コーパスの用意

現在使えるコーパス

- Wikipedia

## 4. コーパスの読み込み

コマンド整備中

```python commands/batch.py``` を実行すると、バッチ一覧が表示される。

## 5. 各種タスクの実行

各種タスクを行う

- 質問
- サーバー起動
