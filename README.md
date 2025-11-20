# README.md

## プロジェクト概要

本プロジェクトは、Google Gemini AIとウェブスクレイピング技術を組み合わせ、特定の情報を自動収集、分析し、結果を通知するAIエージェントの集合体です。主に以下の2つの主要なエージェントで構成されています。

1.  **ファッションアイテム探索・通知エージェント**: 特定のブランドのファッションアイテム（DIESEL KIDS）をオンラインストア（Yahoo!ショッピング）からスクレイピングし、AIが商品詳細ページから特定のサイズ（14Yまたは16Y）の有無を判定。条件に合致する商品をDiscordに通知します。
2.  **README自動更新エージェント**: リポジトリ内のコードベースを解析し、その内容に基づいてプロジェクトの`README.md`を自動生成・更新します。CI/CDパイプラインへの組み込みを想定しています。

このプロジェクトは、定型的な情報収集・分析・通知タスクをAIと自動化ツールで効率化することを目指します。

## ディレクトリ構成


.
├── agents/
│   ├── fasion_diesel_kids/
│   │   ├── main.py
│   │   └── __init__.py
│   ├── tech_readme_updater/
│   │   ├── main.py
│   │   └── __init__.py
│   └── __init__.py
├── common/
│   ├── discord.py
│   ├── scrapers/
│   │   ├── yahoo.py
│   │   ├── zozo.py
│   │   └── __init__.py
│   └── __init__.py
├── .env.example
├── README.md
└── requirements.txt


## 各エージェントの役割

### 1. `agents/fasion_diesel_kids/main.py` (ファッションアイテム探索・通知エージェント)

DIESEL KIDSのアウトレット品の中から、特定のサイズの在庫がある商品を自動で探し出し、通知するエージェントです。

*   **役割**:
    *   `common/scrapers/yahoo.py` を利用して、Yahoo!ショッピングから「ディーゼルキッズ アウトレット」の全商品リンクを収集します。
    *   収集した各商品リンクに対し、Playwrightで詳細ページにアクセス。ページのテキストコンテンツをGoogle Gemini AI (`gemini-2.5-flash`) に渡し、「14Y」または「16Y」のサイズが利用可能か判断させます。
    *   AIによって特定サイズが利用可能と判断された商品リンクを、`common/discord.py` を利用して指定されたDiscordチャンネルに通知します。
*   **使用技術**: Playwright, Google Gemini API, Discord Webhook

### 2. `agents/tech_readme_updater/main.py` (README自動更新エージェント)

プロジェクトのコードベース全体を読み込み、その内容に基づいて`README.md`を自動生成するエージェントです。

*   **役割**:
    *   プロジェクト内の主要な`.py`, `.md`, `.yml`, `.json`, `.txt`ファイルを読み込み、その内容をコンテキストとしてGoogle Gemini AI (`gemini-2.5-flash`) に提供します。
    *   AIは提供されたコンテキストを基に、プロジェクト概要、ディレクトリ構成、各エージェントの役割、セットアップ/実行方法を含む`README.md`を生成します。
    *   生成された`README.md`をプロジェクトルートに書き込み、更新します。
*   **使用技術**: Google Gemini API, ファイルシステム操作
*   **備考**: `GOOGLE_AI_STUDIO_API_KEY`が環境変数に設定されていない場合、ローカルでの意図しない実行を防ぐため、処理をスキップするように設計されています。

### 共通モジュール

*   **`common/discord.py`**:
    *   DiscordのWebhook URLに対して、指定されたメッセージ（商品リンクのリスト）を送信する機能を提供します。
    *   特にDIESEL KIDSの通知用にメッセージ形式がカスタマイズされています。
*   **`common/scrapers/yahoo.py`**:
    *   Playwrightを使用してYahoo!ショッピングの検索結果ページから商品リンクを収集します。複数ページにわたる収集もサポートしています。
*   **`common/scrapers/zozo.py`**:
    *   PlaywrightとBeautifulSoupを使用してZOZOから商品リンクを収集しようと試みるスクレイパーです。
    *   **現状**: コメントに「Access Deniedになるため、ZOZOにアクセスすることは困難」と記載されており、ステルス技術を導入しているものの、アクセスが制限される可能性があります。このスクレイパーは現在、実用レベルでの機能は期待できません。

## セットアップと実行方法

### 前提条件

*   Python 3.8+
*   pip
*   Playwrightブラウザ

### 1. リポジトリのクローン

bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name


### 2. 仮想環境の作成と依存ライブラリのインストール

bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt


### 3. Playwrightブラウザのインストール

Playwrightがウェブページにアクセスするために必要なブラウザをインストールします。

bash
playwright install


### 4. 環境変数の設定

プロジェクトルートに`.env`ファイルを作成し、必要な環境変数を設定します。`env.example`を参考にしてください。

ini
# .env
GOOGLE_AI_STUDIO_API_KEY="YOUR_GEMINI_API_KEY"
DISCORD_WEBHOOK_URL="YOUR_DISCORD_WEBHOOK_URL"


*   `GOOGLE_AI_STUDIO_API_KEY`: Google AI Studio (Gemini) のAPIキー。
*   `DISCORD_WEBHOOK_URL`: Discordに通知を送信するためのWebhook URL。

### 5. 各エージェントの実行

#### 5.1. ファッションアイテム探索・通知エージェントの実行

DIESEL KIDSのアウトレット品を検索し、特定のサイズのアイテムがあればDiscordに通知します。

bash
python agents/fasion_diesel_kids/main.py


#### 5.2. README自動更新エージェントの実行

現在のプロジェクトのコードベースに基づいて`README.md`を自動更新します。

bash
python agents/tech_readme_updater/main.py