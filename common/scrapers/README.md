# common/scrapers/

## 概要
このディレクトリは、特定のWebサイトから情報を自動的に収集するためのスクレイピングモジュールを格納しています。主に、ECサイトからの商品情報収集を目的としており、収集したデータの整形や外部サービスへの通知機能（`common/discord.py` を介して）と連携します。

## ディレクトリ構成
このフォルダ内のファイルと、関連する上位ディレクトリのファイルは以下の通りです。

| ファイル/ディレクトリ | 説明 |
| :-------------------- | :------------------------------------------------------------------------------------------------------------- |
| `yahoo.py`            | Playwrightを使用してYahoo!ショッピングから商品リンクを収集するスクレイパーです。 |
| `zozo.py`             | PlaywrightとBeautifulSoupを使用してZOZOから商品リンクの収集を試みますが、現状ではアクセス拒否により成功していません。 |
| `__init__.py`         | Pythonパッケージであることを示す空ファイルです。                                                                 |
| `../discord.py`       | （common/直下）スクレイピング結果をDiscordチャンネルに通知するためのユーティリティ関数を提供します。              |

## 各ファイル/モジュールの説明

### `yahoo.py`
*   **目的**: Yahoo!ショッピングの検索結果ページから、特定の商品（例: 「DIESEL KIDS アウトレット」）の詳細ページへのリンクを複数ページにわたって自動的に収集します。
*   **機能**:
    *   `fetch_yahoo_links_playwright(target_url: str)`: Playwrightの `chromium` ブラウザをヘッドレスモードで起動し、指定されたURLにアクセス。特定のCSSセレクタ (`a[class*="ItemImageLink_SearchResultItemImageLink__link__"]`) を使用して商品リンクを抽出し、重複を除去したセットとして返します。
    *   `if __name__ == "__main__":` ブロック: `BASE_SEARCH_URL` と1ページあたりのアイテム数 (`ITEMS_PER_PAGE`) を基にURLを構築し、`fetch_yahoo_links_playwright` をループで呼び出すことで、存在するすべてのページのリンクを収集します。

### `zozo.py`
*   **目的**: ZOZOのブランドページから商品リンクの収集を試みる実験的なスクレイパーです。
*   **機能**:
    *   `fetch_product_links_playwright(target_url: str)`: PlaywrightとBeautifulSoupを使用して、指定されたZOZOのブランドページにアクセスし、商品カード (`div.c-items_item`) 内のリンクを抽出します。
    *   **制約**: ZOZOサイトは高度な自動化検知を導入しているため、`page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")` のようなステルス対策を講じていますが、現状では「Access Denied」となり、スクレイピングは成功していません。

### `../discord.py`
*   **目的**: 商品のURLリストなど、スクレイピングで得られた情報をDiscordチャンネルにリアルタイムで通知します。
*   **機能**:
    *   `send_discord_notification(webhook_url: str, items: list[str])`: DiscordのWebhook URLと通知したいアイテム（URL文字列のリスト）を受け取ります。メッセージを整形し、`requests` ライブラリを使用してDiscordにPOSTリクエストとして送信します。アイテムがない場合は通知をスキップします。

## 実行方法
この `common/scrapers/` ディレクトリ自体には `main.py` は存在しませんが、個々のスクレイパーモジュールは直接実行可能です。

### Yahoo!ショッピングスクレイパーの実行
bash
python common/scrapers/yahoo.py

*このスクリプトは、DIESEL KIDSのアウトレット商品を自動的に検索し、全てのページから商品リンクを収集します。*

### ZOZOスクレイパーの実行 (現在アクセス拒否されます)
bash
python common/scrapers/zozo.py

*このスクリプトはZOZOのDIESEL KIDSブランドページにアクセスを試みますが、現時点では「Access Denied」により商品リンクの収集に失敗します。*

これらのスクレイパーは、`agents/fashion_diesel_kids/main.py` のような上位のエージェントからインポートして利用されることが想定されています。

## 環境変数
このディレクトリ内のスクレイパーが直接利用する環境変数は、個々の実装に依存します。

*   **`DISCORD_WEBHOOK_URL`**: `common/discord.py` の `send_discord_notification` 関数を利用してDiscordに通知を送る際に必要です。通常は、`agents/fashion_diesel_kids/main.py` のようなエージェント側で設定され、`discord.py` に渡されます。
*   **`GOOGLE_AI_STUDIO_API_KEY`**: `agents/fashion_diesel_kids/main.py` など、スクレイパーの収集結果をAIで分析するエージェントで利用されます。`check_page_for_size` のような関数で商品詳細ページの内容をAIに渡し、特定の条件（例: サイズ）を判断させる場合に使用します。

これらの環境変数は、プロジェクトルートの `.env` ファイルに設定することが推奨されます。

---