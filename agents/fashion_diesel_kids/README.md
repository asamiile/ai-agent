# agents/fashion_diesel_kids/

## 1. 概要

このディレクトリは、Yahoo!ショッピングから「DIESEL KIDS アウトレット」の商品情報をスクレイピングし、特定のサイズ（14Y または 16Y）が利用可能な商品をAI（Google Gemini）で選定し、その結果をDiscordに通知するエージェントです。DIESEL KIDSの特定のサイズのアイテムを効率的に見つけることを目的としています。

## 2. ディレクトリ構成


agents/fashion_diesel_kids/
├── main.py
└── __init__.py


## 3. 各ファイル/モジュールの説明

| ファイル/モジュール名 | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `main.py`             | このエージェントのメインスクリプトです。 <br> Yahoo!ショッピングのDIESEL KIDSアウトレット検索結果ページから全商品リンクを収集します。 <br> 収集した各商品ページにPlaywrightでアクセスし、ページコンテンツをAI（Google Gemini）に渡して「14Y」または「16Y」のサイズが利用可能か判定させます。 <br> サイズが利用可能な商品が見つかった場合、そのURLリストをDiscordの指定されたWebhook URLに通知します。 <br> `common/scrapers/yahoo.py` と `common/discord.py` の機能を利用しています。 |
| `__init__.py`         | Pythonパッケージとして認識させるための空ファイルです。                                                                                                                                                                                                                                                                                                                                                                                                                  |

## 4. 実行方法

このエージェントは、以下のコマンドで実行できます。実行前に、必要な環境変数を設定し、依存ライブラリをインストールしてください。

bash
python agents/fashion_diesel_kids/main.py


### 前提条件

- Python 3.9+
- `requirements.txt` に記載されている依存ライブラリがインストールされていること
- Playwrightのブラウザがインストールされていること (`playwright install` コマンドを使用)

### セットアップ手順

1. **リポジトリのクローン**
   bash
   git clone [リポジトリのURL]
   cd [リポジトリ名]
   

2. **仮想環境の作成と有効化**
   bash
   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   

3. **依存ライブラリのインストール**
   bash
   pip install -r requirements.txt
   

4. **Playwrightブラウザのインストール**
   bash
   playwright install
   

## 5. 環境変数

このエージェントを実行するには、以下の環境変数をプロジェクトのルートディレクトリにある `.env` ファイルに設定する必要があります。

| 環境変数名             | 説明                                                                     |
| :--------------------- | :----------------------------------------------------------------------- |
| `GOOGLE_AI_STUDIO_API_KEY` | Google Generative AI (Gemini) のAPIキー。AIによるサイズ判定に使用します。 |
| `DISCORD_WEBHOOK_URL`    | DiscordのWebhook URL。選定された商品の通知に使用します。                 |

`.env.example` を参考に、`.env` ファイルを作成してください。

dotenv
# .env.example
GOOGLE_AI_STUDIO_API_KEY="your_google_ai_studio_api_key_here"
DISCORD_WEBHOOK_URL="your_discord_webhook_url_here"