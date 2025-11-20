`agents/tech_readme_updater` ディレクトリ専用の `README.md` を作成します。


# `agents/tech_readme_updater`

## 機能と目的

このエージェントは、プロジェクト内のコードベース全体を解析し、ルートディレクトリの `README.md` と、`agents/` ディレクトリ配下にある各エージェントの `README.md` を自動で生成・更新することを目的としています。

主な機能は以下の通りです。

1.  **リポジトリファイル読み込み**: `read_repository_files()` 関数が、`.git`、`.venv`、`__pycache__` などの不要なディレクトリを除外し、`.py`、`.md`、`.yml`、`.json`、`.txt` などの主要なコードおよびドキュメントファイルを読み込みます。
2.  **Gemini API連携**: `call_gemini()` 関数を通じて Google Gemini API を呼び出し、読み込んだコードベースのコンテキストに基づいてドキュメントコンテンツを生成します。
3.  **ルートREADME更新**: `update_root_readme()` 関数が、プロジェクト全体の概要、ディレクトリ構成図、各エージェントの役割などを記述したルートディレクトリの `README.md` を生成・更新します。
4.  **エージェント別README更新**: `update_agent_readmes()` 関数が、各エージェントの機能詳細、目的、実行方法、依存モジュール、ファイル構成などを記述した個別の `README.md` を生成・更新します。

これにより、プロジェクトのドキュメントを常に最新の状態に保ち、手動でのドキュメント更新作業の負担を軽減します。

## 実行方法

このエージェントを実行するには、まず以下の環境変数を設定する必要があります。

*   `GOOGLE_AI_STUDIO_API_KEY`: Google Gemini API にアクセスするためのAPIキー。

ルートディレクトリから、以下のコマンドを実行してください。

bash
python agents/tech_readme_updater/main.py


実行後、プロジェクトのルートディレクトリおよび `agents/` 配下の各エージェントディレクトリに `README.md` ファイルが生成または更新されます。

## 依存モジュール

このエージェントが直接依存しているPythonモジュールは以下の通りです。

*   `google-generativeai`: Google Gemini API との連携に使用します。
*   `python-dotenv`: `.env` ファイルから環境変数をロードするために使用します。

`common/` ディレクトリ内の共通モジュール（例: `common/discord.py`, `common/scrapers/yahoo.py` など）には直接依存していません。ただし、このエージェントが他のエージェントの `README.md` を生成する際には、それらのエージェントが `common/` モジュールに依存している事実も考慮してドキュメントを作成します。

## ファイル構成

このエージェントのディレクトリ構成は以下の通りです。


agents/
└── tech_readme_updater/
    └── main.py


*   `main.py`: このエージェントの主要なロジックが記述されています。リポジトリ内のファイル読み込み、Gemini APIの呼び出し、READMEファイルの生成・更新処理が実装されています。