# AI Agent

## プロジェクト概要

本プロジェクトは、Google Gemini AIとWebスクレイピング・ブラウザ自動化技術を組み合わせた、AIエージェントの集合体です。定型的な情報収集・分析・通知タスクをAIと自動化ツールで効率化することを目指します。

### エージェント一覧

| エージェント | 概要 |
|-------------|------|
| `agents/fashion_diesel_kids/` | DIESEL KIDSの特定サイズ（14Y/16Y）商品をYahoo!ショッピングから検索し、Discordに通知 |
| `agents/tech_readme_updater/` | リポジトリのコードベースを解析し、README.mdを自動生成・更新 |
| `agents/webapp_tester/` | AIを活用してWebアプリケーションのテストコードを自動生成・実行 |

### ツール

| ツール | 概要 |
|--------|------|
| `tools/playwright-mcp/` | Playwright MCPを使ったWeb探索テストのガイドとレポート |

### 共通モジュール

| モジュール | 概要 |
|-----------|------|
| `common/discord.py` | Discord Webhook通知 |
| `common/scrapers/` | Yahoo!ショッピング等のスクレイパー |

## セットアップと実行方法

### 前提条件

- Python 3.9以上
- pip

### 1. リポジトリのクローン

```bash
git clone https://github.com/asamiile/ai-agent.git
cd ai-agent
```

### 2. 仮想環境の作成と有効化

```bash
# macOS/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. Playwrightブラウザのインストール

```bash
playwright install
```

### 5. 環境変数の設定

`.env`ファイルを作成し、必要な環境変数を設定します。

```dotenv
# Google AI Studio (Gemini) のAPIキー
GOOGLE_AI_STUDIO_API_KEY="your_api_key_here"

# Discord Webhook URL（通知用）
DISCORD_WEBHOOK_URL="your_webhook_url_here"
```

### 6. 実行例

```bash
# DIESEL KIDS商品検索エージェント
python agents/fashion_diesel_kids/main.py

# README自動更新エージェント
python agents/tech_readme_updater/main.py

# Webアプリテストエージェント
python agents/webapp_tester/main.py https://example.com/
```
