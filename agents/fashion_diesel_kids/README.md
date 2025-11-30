# agents/fashion_diesel_kids/

## 概要
このディレクトリには、DIESEL KIDSの商品をYahoo!ショッピングで自動的に監視し、特定のサイズ（14Yまたは16Y）が入荷された場合にDiscordに通知するエージェントが含まれています。PlaywrightによるWebスクレイピングとGoogle Gemini APIを活用したAIによるサイズ判定を組み合わせることで、効率的な商品追跡を実現します。

## ディレクトリ構成


agents/fashion_diesel_kids/
├── main.py
└── __init__.py


## 各ファイル/モジュールの説明

-   **`main.py`**
    このエージェントの主要な実行スクリプトです。以下の処理を順に実行します。
    1.  `common/scrapers/yahoo.py` を使用して、Yahoo!ショッピングで「DIESEL KIDS アウトレット」の検索結果から全ての商品リンクを収集します。
    2.  収集した各商品リンクにPlaywrightでアクセスし、ページコンテンツをAI（Google Gemini）に渡し、「14Y」または「16Y」のサイズが利用可能かを判定させます。AIは「はい」または「いいえ」で回答します。
    3.  AIによって特定のサイズが「はい」と判定された商品リンクを抽出し、`common/discord.py` を使用してDiscordチャンネルに通知を送信します。

-   **`__init__.py`**
    Pythonパッケージとして認識させるための空のファイルです。

-   **依存モジュール（`common` フォルダから）**
    -   **`common/scrapers/yahoo.py`**
        Playwrightを利用してYahoo!ショッピングの検索結果ページから商品詳細ページのURLを効率的に収集するためのモジュールです。ページネーションを考慮し、すべての関連リンクを網羅的に取得します。
    -   **`common/discord.py`**
        商品のURLリストを受け取り、指定されたDiscord Webhook URLを介して、整形された通知メッセージをDiscordチャンネルに送信する機能を提供します。

## 実行方法
以下の手順でエージェントを実行できます。

1.  **依存ライブラリのインストール**
    プロジェクトルートディレクトリで、以下のコマンドを実行して必要なライブラリをインストールします。

    bash
    pip install -r requirements.txt
    

2.  **Playwrightブラウザのインストール**
    Playwrightを使用するためには、対応するブラウザ（Chromium）をインストールする必要があります。

    bash
    playwright install
    

3.  **エージェントの実行**
    エージェントを実行するには、`main.py` スクリプトを直接実行します。

    bash
    python agents/fashion_diesel_kids/main.py
    

## 環境変数
エージェントを実行する前に、以下の環境変数を設定する必要があります。これらは、`.env` ファイルに記述するか、実行環境の環境変数として設定してください。

| 環境変数名                 | 説明                                                 |
| :------------------------- | :--------------------------------------------------- |
| `GOOGLE_AI_STUDIO_API_KEY` | Google Gemini APIにアクセスするためのAPIキー。       |
| `DISCORD_WEBHOOK_URL`      | Discordチャンネルに通知を送信するためのWebhook URL。 |