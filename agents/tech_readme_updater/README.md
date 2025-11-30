# tech_readme_updater

## 概要
このディレクトリには、リポジトリ内の`README.md`ファイルを自動生成・更新するAIエージェントが含まれています。`google-generativeai` (Gemini) を利用して、指定されたディレクトリのコードベースを解析し、要件に基づいたマークダウン形式の`README.md`ファイルを生成します。プロジェクト全体のルート`README.md`と、`agents/`および`common/`配下にあるPythonファイルを含む各サブディレクトリの`README.md`の生成・更新を調整します。

## ディレクトリ構成


agents/tech_readme_updater/
├── main.py
└── README.md (このファイル)


## 各ファイル/モジュールの説明

| ファイル名 | 説明 |
| :--------- | :--- |
| `main.py` | このエージェントの主要な実行スクリプトです。リポジトリ内のコードベースを読み込み、`google-generativeai`モデルに`README.md`の生成を依頼し、結果を対応するディレクトリに書き込みます。ルートの`README.md`と、Pythonファイルを含むすべてのサブディレクトリの`README.md`の生成・更新を調整します。 |

## 実行方法

このエージェントは、以下のコマンドで実行できます。`main.py`は、プロジェクトルートと、`agents/`および`common/`配下にあるPythonファイルを含むすべてのサブディレクトリの`README.md`を自動的に更新します。

bash
python agents/tech_readme_updater/main.py


## 環境変数

このエージェントの実行には、以下の環境変数を設定する必要があります。

| 環境変数名 | 説明 |
| :--------- | :--- |
| `GOOGLE_AI_STUDIO_API_KEY` | Google AI Studio (Gemini API) にアクセスするためのAPIキーです。`genai.configure(api_key=API_KEY)` を通じてモデル認証に使用されます。 |