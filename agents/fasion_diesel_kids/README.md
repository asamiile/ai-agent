# DIESEL KIDS ファッションアイテム監視エージェント

このディレクトリには、DIESEL KIDSのアウトレット商品の中から特定のサイズのアイテムを自動で検出し、Discordに通知するエージェントが含まれています。

## 🚀 機能詳細と目的

このエージェントの主な目的は以下の通りです。

1.  **Yahoo!ショッピングの商品リンク収集**:
    Yahoo!ショッピングの「DIESEL KIDS アウトレット」検索結果ページを巡回し、存在するすべての商品詳細ページのURLを自動で収集します。これにより、最新のアイテム情報を網羅的に取得します。

2.  **AIによるサイズ選定**:
    収集した各商品リンクにアクセスし、[Playwright](https://playwright.dev/) を用いてページのテキストコンテンツを抽出します。抽出したテキストは [Google Gemini](https://ai.google.dev/models/gemini) モデルに渡され、その商品に「**14Y**」または「**16Y**」のサイズが利用可能かどうかを高度な自然言語処理で判断させます。

3.  **Discord通知**:
    AIによって特定された「14Y」または「16Y」のサイズがある商品の一覧を、Discordの指定されたチャンネルに自動で通知します。これにより、ユーザーは希望するサイズのアイテムが新たに入荷・発見された際に迅速に情報を得ることができます。

## 🛠️ 実行方法

このエージェントは、プロジェクトのルートディレクトリから以下のコマンドで実行できます。

bash
python agents/fasion_diesel_kids/main.py


### 事前準備:

1.  **環境変数の設定**:
    プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の環境変数を設定してください。
    -   `GOOGLE_AI_STUDIO_API_KEY`: Google Gemini APIにアクセスするためのAPIキー。
    -   `DISCORD_WEBHOOK_URL`: Discordの通知を送りたいチャンネルのWebhook URL。

    `.env` ファイルの例:
    
    GOOGLE_AI_STUDIO_API_KEY="YOUR_GEMINI_API_KEY"
    DISCORD_WEBHOOK_URL="YOUR_DISCORD_WEBHOOK_URL"
    

2.  **依存ライブラリのインストール**:
    プロジェクトルートで `requirements.txt` に記載されているライブラリをインストールしてください。
    bash
    pip install -r requirements.txt
    playwright install
    
    `playwright install` コマンドは、Playwrightが動作するために必要なブラウザエンジンをダウンロードします。

## 🔗 依存共通モジュール

このエージェントは、プロジェクト内の `common/` ディレクトリに定義されている以下の共通モジュールに依存しています。

-   `common/scrapers/yahoo.py`:
    Yahoo!ショッピングからの商品リンク収集機能を提供します。特に `fetch_yahoo_links_playwright` 関数は、Playwrightを使用してYahoo!ショッピングの検索結果ページから商品リンクを効率的に収集する役割を担っています。

-   `common/discord.py`:
    Discordへの通知送信機能を提供します。`send_discord_notification` 関数は、特定のWebhook URLへ、指定された商品URLリストを整形して通知する際に使用されます。

これらの共通モジュールは、`sys.path.append` を用いて動的にパスに追加され、`main.py` からインポートされて利用されます。

## 📂 ファイル構成

`agents/fasion_diesel_kids/` ディレクトリは以下のファイルで構成されています。


agents/
└── fasion_diesel_kids/
    ├── main.py         # このエージェントのメイン処理ロジック
    └── __init__.py     # Pythonパッケージとして認識させるための空ファイル


-   `main.py`: 前述の通り、Yahoo!ショッピングからの商品リンク収集、AIによるサイズ選定、そしてDiscord通知の全フローを orchestrate する中心的なスクリプトです。