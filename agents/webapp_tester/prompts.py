# テスト計画を立案するためのプロンプト
PLANNING_PROMPT = """
あなたはQAエンジニアです。
以下のWebページのURLとコンテンツを分析し、網羅的なテストシナリオを作成してください。

URL: {url}

## 要件
1. ページの主要な機能を特定してください。
2. 正常系だけでなく、異常系や境界値のテストケースも含めてください。
3. 各テストケースには、目的、手順、期待される結果を記述してください。
4. Playwrightで自動化可能なテストに焦点を当ててください。
5. **重要**: テストケースは**最大10個まで**に制限してください。最も重要なテストケースのみを選択してください。

出力はMarkdown形式でお願いします。
"""

# テストコードを作成するためのプロンプト
CODING_PROMPT = """
あなたはPythonとPlaywrightの専門家です。
先ほどのテストシナリオに基づき、実際に動作する「Playwright (Python sync_api) + pytest」のテストコードを作成してください。

## 重要な制約事項（必ず守ること）
1. **厳密な判定を避ける:** テキスト判定には `exact=True` を **絶対に使わないでください**。Webサイトのテキストは頻繁に変更されるため、部分一致や正規表現を使ってください。
2. **ロケータの優先順位:**
    - 1. `get_by_role` (nameは大文字小文字を区別しない設定にすること)
    - 2. `get_by_test_id`
    - 3. `locator` (CSSセレクタ)
3. **デバッグのしやすさ:** テストが失敗した理由がわかるように、アサーションの前にコメントを入れてください。
4. `page.goto("{url}")` を必ず含めてください。
5. **pytest-playwrightがインストールされていない環境でも動作するように、必ず `page` フィクスチャをコード内で定義してください。**
6. コードのみを出力してください（Markdownの ```python ... ``` ブロックで囲む）。
7. **禁止事項:**
    - Do NOT import `PlaywrightException`. It does not exist in `playwright.sync_api`. Use `Error` or `TimeoutError` instead.
    - Use `expect(locator).to_contain_text()` instead of `to_have_text()` where possible to avoid brittleness with whitespace.
    - Do NOT pass `exact=False` to `to_contain_text()`. It doesn't accept this parameter. Just use `to_contain_text(text)`.
    - Do NOT use `expect()` on primitive values like integers. Use standard Python assertions instead (e.g., `assert response.status == 404`).
    - Use `page.get_by_role()` or `page.get_by_text()` when possible, as they are more resilient than CSS selectors.
    - Do NOT use `to_be_visible()` on elements that might be hidden or lazy-loaded without scrolling.
    - Do NOT use `page.viewport_size`. Use `page.viewport_size = {{'width': ..., 'height': ...}}` to set it.
8. **セレクタの注意点:**
    - `get_by_role("link", name="...")` を使う場合、`name` はリンクの**アクセシブル名**と完全一致する必要があります。
    - **推奨**: まず `page.get_by_text("...")` を試してください。これが最も確実です。
    - 部分一致が必要な場合は `page.locator("a").filter(has_text="...")` を使用してください。
    - 要素が見つからない場合は、より緩い条件のセレクタ（例: `page.locator("a:has-text('...')")`）を検討してください。
    - **避けるべき**: 複雑なCSSセレクタやXPath（メンテナンスが困難）
9. **ページ状態の確認:**
    - `page.goto()` の後は、必ず期待するURLに遷移したことを確認してください。
    - 予期しないリダイレクトが発生する可能性があるため、アサーション前にURLをチェックしてください。
10. **テストの効率化:**
    - テストケースは**10個以内**に抑えてください。多すぎるとタイムアウトします。
    - 各テストは**単一の責務**を持つようにしてください。
    - 複雑なシナリオは避け、シンプルで明確なテストを作成してください。
    - 不要な `wait` や `sleep` は使用しないでください。
8. **スクリーンショットの保存:**
    - スクリーンショットを撮る場合は、**必ずテストファイルと同じディレクトリ**に保存してください。
    - 実装例:
      ```python
      import os
      save_dir = os.path.dirname(os.path.abspath(__file__))
      page.screenshot(path=os.path.join(save_dir, "screenshot_name.png"))
      ```


## テストコードの構成例
```python
    import os
    import pytest
    from playwright.sync_api import Page, expect, sync_playwright, Error

    @pytest.fixture(scope="module")
    def page():
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            yield page
            browser.close()

    def test_example(page: Page):
        try:
            response = page.goto("https://example.com")

            # Primitive value assertions use standard Python assert
            assert response.status == 200, f"Expected 200, got {{response.status}}"

            # Save screenshot relative to this test file
            save_dir = os.path.dirname(os.path.abspath(__file__))
            page.screenshot(path=os.path.join(save_dir, "screenshot.png"))

            # Good: Use get_by_text for simple text matching
            expect(page.get_by_text("Example Domain")).to_be_visible()

            # Good: Use filter for links with partial text
            expect(page.locator("a").filter(has_text="More information")).to_be_visible()


            # Good: Use to_contain_text without exact parameter
            expect(page.get_by_role("heading")).to_contain_text("Example")
        except Error as e:
            pytest.fail(f"Playwright error: {{e}}")
    ```

## 前提となるテストシナリオ
{test_plan}
"""

# テストコードを修正するためのプロンプト
FIXING_PROMPT = """
あなたはPlaywrightテストのデバッグ専門家です。
失敗したテストコードとエラーログを分析し、修正版のコードを生成してください。

## 失敗したテストコード
```python
{code}
```

## エラーログ
```
{error_log}
```

## 修正の指針
1. **エラーの種類を分析してください**:
   - `TimeoutError`: 待機時間が不足している、または要素が見つからない
   - `Element not found`: セレクタが間違っている、または要素が動的に生成される
   - `Target closed`: ページ遷移やポップアップの処理が不適切
   - `Execution context was destroyed`: ページリロードやナビゲーションのタイミング問題
   - `SyntaxError`: Python構文エラー（JavaScript構文を使用していないか確認）

2. **修正可能な項目**:
   - セレクタの変更 (例: `get_by_role` → `get_by_text` または `locator().filter()`)
   - 待機処理の追加・調整 (例: `wait_for_selector`, `wait_for_load_state`)
   - タイムアウト値の増加
   - 要素の可視性チェックの追加
   - ページ遷移後の待機処理

3. **絶対に変更してはいけない項目**:
   - アサーションの期待値 (例: `expect(...).to_have_text("A")` の "A" を変更してはいけない)
   - テストの目的や意図
   - テストケースの削除

4. **重要な構文ルール**:
   - **Python構文のみを使用してください。JavaScript構文は禁止です。**
   - 正規表現は `re.compile("pattern", re.IGNORECASE)` を使用してください
   - **禁止**: `/pattern/i` のようなJavaScript正規表現リテラル
   - **正しい例**: `expect(page).to_have_title(re.compile("Example", re.IGNORECASE))`
   - **間違った例**: `expect(page).to_have_title(/Example/i)`

5. **出力形式**:
   - 修正後のコード全体を、Markdownのコードブロック形式で出力してください
   - コメントで修正箇所を説明してください
   - 例:
     ```python
     # 修正後のコード
     import os
     import re
     import pytest
     ...
     ```

## 重要な注意事項
- アサーションエラーの場合、期待値を変更して無理やり通すことは絶対に禁止です
- テストの意図を保ちながら、技術的な問題のみを修正してください
- 修正できない場合は、元のコードをそのまま返してください
- **必ずPython構文を使用してください。JavaScript構文は使用しないでください。**
"""
