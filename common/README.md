# common/

## 概要
このディレクトリは、プロジェクト内の様々なエージェントやモジュールから共通して利用される汎用的なユーティリティ機能や基盤となるモジュール群を提供します。具体的には、外部サービスへの通知機能や、複数のウェブサイトに対応したスクレイピング機能などが含まれます。これにより、コードの再利用性を高め、各エージェントの責務をシンプルに保つことを目的としています。

## ディレクトリ構成


common/
├── discord.py
└── scrapers/
    ├── __init__.py
    ├── yahoo.py
    └── zozo.py


## 各ファイル/モジュールの説明

| ファイル/モジュール名 | 概要 | 主要機能/関数 | 依存関係 | 備考 |
| :-------------------- | :--- | :------------ | :------- | :--- |
| `discord.py`          | Discordへの通知送信機能を提供します。 | `send_discord_notification(webhook_url: str, items: list[str])`: 商品URLリストをDiscordに通知します。 | `requests`, `json` | 主に他のエージェントからのインポート利用を想定しています。 |
| `scrapers/`           | 各種ウェブサイトからの情報収集（スクレイピング）に関するモジュール群を格納します。 | - | - | - |
| `scrapers/yahoo.py`   | Playwrightを使用してYahoo!ショッピングから商品リンクを収集します。複数ページにわたる自動スクレイピングに対応しています。 | `fetch_yahoo_links_playwright(target_url: str) -> set[str]`: 指定されたYahoo!ショッピングの検索結果URLから商品詳細ページのURLを収集します。 | `playwright` | `agents/fashion_diesel_kids/main.py` で利用されています。単体で実行することも可能です。 |
| `scrapers/zozo.py`    | PlaywrightとBeautifulSoupを使用してZOZOTOWNの商品リンク収集を試みます。自動化検知を回避するためのスクリプト挿入を試みていますが、現状ではアクセス困難です。 | `fetch_product_links_playwright(target_url: str) -> set[str]`: 指定されたZOZOTOWNのURLから商品リンクを収集します（アクセス成功した場合）。 | `playwright`, `bs4`, `urllib.parse` | 現在は `Access Denied` によりアクセスが困難であることがコード内で明記されています。単体で実行することも可能です。 |

## 実行方法

`common/` ディレクトリ内のモジュールは、主に他のエージェントや上位のロジックからインポートされて使用される共通部品です。

ただし、`common/scrapers/` 配下のスクレイピングモジュールは、開発やテストのために単体で実行できる `if __name__ == "__main__":` ブロックを持っています。

### `common/scrapers/yahoo.py` の実行例

bash
python common/scrapers/yahoo.py


このコマンドを実行すると、Yahoo!ショッピングから「ディーゼルキッズ アウトレット」の検索結果を複数ページにわたってスクレイピングし、収集した商品リンクをコンソールに出力します。

### `common/scrapers/zozo.py` の実行例

bash
python common/scrapers/zozo.py


このコマンドを実行すると、ZOZOTOWNの「DIESEL KIDS」ブランドページから商品リンクの収集を試みます。ただし、コードのコメントにもあるように、現在は「Access Denied」により成功しない可能性が高いです。

## 環境変数

`common/` ディレクトリ内のモジュール自体は直接環境変数を読み込みません。

- `common/discord.py` が必要とするDiscordのWebhook URL (`webhook_url`) は、この関数を呼び出す側のモジュール（例: `agents/fashion_diesel_kids/main.py`）で環境変数 `DISCORD_WEBHOOK_URL` から読み込まれ、引数として渡されます。
- `common/scrapers/` 配下のモジュールは、ウェブブラウザ自動化ライブラリであるPlaywrightを利用しますが、Playwright自体の設定（例: ブラウザバイナリのパスなど）は、Playwrightライブラリのドキュメントを参照してください。