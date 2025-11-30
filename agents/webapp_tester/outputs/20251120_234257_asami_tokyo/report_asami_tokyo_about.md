# Webapp Test Report

**Target URL:** https://asami.tokyo/about
**Date:** 2025-11-21 01:27:14
**Status:** ❌ FAIL

## 1. Test Plan
## QAエンジニアによるテストシナリオ：asami.tokyo/about

### 前提

*   テスト対象URL: `https://asami.tokyo/about`
*   テストツール: Playwrightを想定
*   Webサイトは常に最新版がデプロイされていることを前提とします。
*   ネットワーク環境は安定していることを前提とします。

### テストケース

#### 1. Aboutページの基本表示と主要コンテンツの確認

*   **目的:** ページが正常にロードされ、ユーザーに意図した情報（自己紹介、スキル概要）が提供されていることを確認する。
*   **手順:**
    1.  ブラウザで `https://asami.tokyo/about` にアクセスする。
    2.  ページのタイトルが「About - Asami K.」であることを確認する。
    3.  ページ内に「I create visuals using TouchDesigner and Unreal Engine.」というテキストが表示されていることを確認する。
    4.  「Development」セクションに「I am developing the front-end of web applications using Vue.js and Nuxt.js.」というテキストが表示されていることを確認する。
*   **期待される結果:**
    *   ページが正常にロードされ、ステータスコードが200であること。
    *   ページタイトルが `About - Asami K.` であること。
    *   指定された主要な自己紹介テキストや開発内容のテキストがページ内に表示されていること。
*   **Playwrightでの自動化のポイント:** `page.goto()`, `expect(page).toHaveTitle()`, `expect(page.locator()).toHaveText()`

#### 2. ヘッダーナビゲーションリンクの動作確認 (Top, Art, Camera, Apps)

*   **目的:** ヘッダー内の主要ナビゲーションリンクが正しく機能し、適切な内部ページへ遷移することを確認する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  ヘッダー内の「Art」リンクをクリックする。
    3.  URLが `/art` に遷移したことを確認する。
    4.  他のナビゲーションリンク（「Top」「Camera」「Apps」）についても同様にクリックし、それぞれの対応するURLへの遷移を確認する。
*   **期待される結果:**
    *   各ナビゲーションリンクのクリック後、期待されるURL（例: `/art`, `/camera` など）に正しく遷移すること。
    *   遷移先のページが正常にロードされ、ステータスコードが200であること。
*   **Playwrightでの自動化のポイント:** `page.click()`, `expect(page).toHaveURL()`

#### 3. 「View the Works.」リンクの動作確認

*   **目的:** ユーザーが作品ポートフォリオへアクセスできることを確認する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  「Art」セクション内の「View the Works.」リンクをクリックする。
    3.  遷移先のURLが作品一覧ページを示すパス（例: `/art`）になっていることを確認する。
*   **期待される結果:**
    *   リンククリック後、URLが `/art` または作品一覧を示すURLに正しく遷移すること。
    *   遷移先のページが正常にロードされ、ステータスコードが200であること。
*   **Playwrightでの自動化のポイント:** `page.click()`, `expect(page).toHaveURL()`

#### 4. 「View the Video. ( Youtube / Vimeo )」リンクの動作確認 (外部遷移)

*   **目的:** ユーザーが動画コンテンツへアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  「Art」セクション内の「View the Video. ( Youtube / Vimeo )」リンクをクリックする。
    3.  新しいブラウザタブが開き、そのタブのURLがYouTubeまたはVimeoのドメインを含んでいることを確認する。
*   **期待される結果:**
    *   リンククリック後、新しいタブが開き、そのタブのURLが `youtube.com` または `vimeo.com` を含むこと。
*   **Playwrightでの自動化のポイント:** `context.waitForEvent('page')`, `expect(newPage).toHaveURL()`

#### 5. 「View the Shop.」リンクの動作確認 (外部遷移)

*   **目的:** ユーザーがショップへアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  「Art」セクション内の「View the Shop.」リンクをクリックする。
    3.  新しいブラウザタブが開き、そのタブのURLが外部ショップのドメインを含んでいることを確認する。
*   **期待される結果:**
    *   リンククリック後、新しいタブが開き、そのタブのURLが外部ショップのドメイン（例: `etsy.com`, `gumroad.com` など）を含むこと。
*   **Playwrightでの自動化のポイント:** `context.waitForEvent('page')`, `expect(newPage).toHaveURL()`

#### 6. 「View the AI Prompt.」リンクの動作確認

*   **目的:** ユーザーがAI関連のブログ記事（Mediumなど）へアクセスできることを確認する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  「Art」セクション内の「View the AI Prompt.」リンクをクリックする。
    3.  遷移先のURLがMediumなどの記事サイトのドメインを含んでいることを確認する。
*   **期待される結果:**
    *   リンククリック後、URLがMedium（`medium.com`）のドメインを含む、または記事ページへ正しく遷移すること。
*   **Playwrightでの自動化のポイント:** `page.click()`, `expect(page).toHaveURL()`

#### 7. 「View the Code.」リンクの動作確認 (外部遷移)

*   **目的:** ユーザーが開発コードリポジトリ（GitHubなど）へアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  「Development」セクション内の「View the Code.」リンクをクリックする。
    3.  新しいブラウザタブが開き、そのタブのURLがGitHubなどのコードリポジトリのドメインを含んでいることを確認する。
*   **期待される結果:**
    *   リンククリック後、新しいタブが開き、そのタブのURLが `github.com` などのリポジトリドメインを含むこと。
*   **Playwrightでの自動化のポイント:** `context.waitForEvent('page')`, `expect(newPage).toHaveURL()`

#### 8. フッターの著作権表示の確認

*   **目的:** ページの法的表示（著作権表示）が最新かつ正確であることを確認する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  ページ下部のフッターエリアに表示されている著作権表示のテキストを取得する。
*   **期待される結果:**
    *   著作権表示が「© 2025 Asami K.」というテキストで表示されていること。
*   **Playwrightでの自動化のポイント:** `expect(page.locator('footer')).toHaveText(/© 2025 Asami K./)`

#### 9. フッターナビゲーションの動作確認 (「contact」リンク)

*   **目的:** ユーザーが連絡手段（お問い合わせフォームなど）へアクセスできることを確認する。
*   **手順:**
    1.  `https://asami.tokyo/about` にアクセスする。
    2.  フッター内の「contact」リンクをクリックする。
    3.  遷移先のURLが `/contact` またはお問い合わせフォームのページURLになっていることを確認する。
*   **期待される結果:**
    *   リンククリック後、URLが `/contact` またはお問い合わせフォームを示すURLに正しく遷移すること。
    *   遷移先のページが正常にロードされ、ステータスコードが200であること。
*   **Playwrightでの自動化のポイント:** `page.click()`, `expect(page).toHaveURL()`

#### 10. 異常系: 存在しないパスへのアクセス時のエラーページ表示

*   **目的:** ユーザーが誤って存在しないURLにアクセスした場合に、サイト全体のエラーハンドリングが適切であることを確認する。
*   **手順:**
    1.  `https://asami.tokyo/about/nonexistentpage` のような、存在しないと想定されるURLに直接アクセスする。
    2.  ページのHTTPステータスコードを確認する。
    3.  ページ内に「404 Not Found」などのエラーメッセージが表示されていることを確認する。
*   **期待される結果:**
    *   HTTPステータスコードが `404` であること。
    *   ページコンテンツとして「404 Not Found」や「ページが見つかりません」といったユーザーフレンドリーなエラーメッセージが表示されていること。
*   **Playwrightでの自動化のポイント:** `const response = await page.goto()`, `expect(response.status()).toBe(404)`, `expect(page.locator()).toContainText('404 Not Found')`

## 2. Execution Result
**Return Code:** 1

### Stdout
```text
============================= test session starts ==============================
platform darwin -- Python 3.11.5, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/asami/develop/app/ai-agent
plugins: base-url-2.1.0, playwright-0.7.1
collected 10 items

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py FF [ 20%]
FFF.FF.F                                                                 [100%]

=================================== FAILURES ===================================
_________________ test_1_about_page_basic_display_and_content __________________

page = <Page url='https://asami.tokyo/about'>

    def test_1_about_page_basic_display_and_content(page: Page):
        """
        テストケース1: Aboutページの基本表示と主要コンテンツの確認
        目的: ページが正常にロードされ、主要な自己紹介テキストと開発内容のテキストが表示されていることを確認する。
        """
        try:
            # Step 1: ブラウザで https://asami.tokyo/about にアクセスする。
            response = page.goto("https://asami.tokyo/about")
    
            # 期待される結果: ページが正常にロードされ、ステータスコードが200であること。
            # Assertion: Check HTTP status code
            assert response.status == 200, f"Expected 200 status code, but got {response.status}"
    
            # Assertion: Check that the current URL matches the expected About page URL.
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2: ページのタイトルが「About - Asami K.」であることを確認する。
            # 期待される結果: ページタイトルが `About - Asami K.` であること。
            # Assertion: Check page title
>           expect(page).to_have_title("About - Asami K.")
E           AssertionError: Page title expected to be 'About - Asami K.'
E           Actual value: About | asami.tokyo 
E           Call log:
E             - Expect "to_have_title" with timeout 5000ms
E               9 × unexpected value "About | asami.tokyo"

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:44: AssertionError
________________________ test_2_header_navigation_links ________________________

page = <Page url='https://asami.tokyo/about'>

    def test_2_header_navigation_links(page: Page):
        """
        テストケース2: ヘッダーナビゲーションリンクの動作確認 (Top, Art, Camera, Apps)
        目的: ヘッダー内の主要ナビゲーションリンクが正しく機能し、適切な内部ページへ遷移することを確認する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
            page.goto("https://asami.tokyo/about")
            # Assertion: Check initial URL
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2-4: 各ナビゲーションリンクをクリックし、URL遷移を確認する。
    
            # Test "Art" link
            # Assertion: Click the "Art" navigation link using get_by_role with case-insensitive name match.
>           page.get_by_role("link", name=re.compile("Art", re.IGNORECASE)).click()

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:77: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.11/site-packages/playwright/sync_api/_generated.py:15573: in click
    self._sync(
.venv/lib/python3.11/site-packages/playwright/_impl/_locator.py:160: in click
    return await self._frame.click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.11/site-packages/playwright/_impl/_frame.py:549: in click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:69: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x107468150>
cb = <function Channel.send.<locals>.<lambda> at 0x1079998a0>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        st: List[inspect.FrameInfo] = getattr(
            task, "__pw_stack__", None
        ) or inspect.stack(0)
    
        parsed_st = _extract_stack_trace_information_from_stack(st, is_internal, title)
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
E           Call log:
E             - waiting for get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))

.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:559: TimeoutError

During handling of the above exception, another exception occurred:

page = <Page url='https://asami.tokyo/about'>

    def test_2_header_navigation_links(page: Page):
        """
        テストケース2: ヘッダーナビゲーションリンクの動作確認 (Top, Art, Camera, Apps)
        目的: ヘッダー内の主要ナビゲーションリンクが正しく機能し、適切な内部ページへ遷移することを確認する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
            page.goto("https://asami.tokyo/about")
            # Assertion: Check initial URL
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2-4: 各ナビゲーションリンクをクリックし、URL遷移を確認する。
    
            # Test "Art" link
            # Assertion: Click the "Art" navigation link using get_by_role with case-insensitive name match.
            page.get_by_role("link", name=re.compile("Art", re.IGNORECASE)).click()
            # 期待される結果: クリック後、URLが `/art` に正しく遷移すること。
            # Assertion: Check URL after clicking "Art" link.
            expect(page).to_have_url("https://asami.tokyo/art")
            # Navigate back to about page for the next link test to ensure clean state.
            page.goto("https://asami.tokyo/about")
    
            # Test "Camera" link
            # Assertion: Click the "Camera" navigation link.
            page.get_by_role("link", name=re.compile("Camera", re.IGNORECASE)).click()
            # 期待される結果: クリック後、URLが `/camera` に正しく遷移すること。
            # Assertion: Check URL after clicking "Camera" link.
            expect(page).to_have_url("https://asami.tokyo/camera")
            page.goto("https://asami.tokyo/about")
    
            # Test "Apps" link
            # Assertion: Click the "Apps" navigation link.
            page.get_by_role("link", name=re.compile("Apps", re.IGNORECASE)).click()
            # 期待される結果: クリック後、URLが `/apps` に正しく遷移すること。
            # Assertion: Check URL after clicking "Apps" link.
            expect(page).to_have_url("https://asami.tokyo/apps")
            page.goto("https://asami.tokyo/about")
    
            # Test "Top" link
            # Assertion: Click the "Top" navigation link (Home).
            page.get_by_role("link", name=re.compile("Top", re.IGNORECASE)).click()
            # 期待される結果: クリック後、URLがルートドメインに正しく遷移すること。
            # Assertion: Check URL after clicking "Top" link.
            expect(page).to_have_url("https://asami.tokyo/")
    
            page.screenshot(path=os.path.join(SAVE_DIR, "test_2_header_navigation_links.png"))
    
        except Error as e:
>           pytest.fail(f"Playwright error in test_2_header_navigation_links: {e}")
E           Failed: Playwright error in test_2_header_navigation_links: Locator.click: Timeout 30000ms exceeded.
E           Call log:
E             - waiting for get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:110: Failed
__________________________ test_3_view_the_works_link __________________________

page = <Page url='https://asami.tokyo/about'>

    def test_3_view_the_works_link(page: Page):
        """
        テストケース3: 「View the Works.」リンクの動作確認
        目的: ユーザーが作品ポートフォリオへアクセスできることを確認する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
            page.goto("https://asami.tokyo/about")
            # Assertion: Check initial URL
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2: 「Art」セクション内の「View the Works.」リンクをクリックする。
            # Assertion: Click "View the Works." link using get_by_role with case-insensitive name match.
            page.get_by_role("link", name=re.compile("View the Works", re.IGNORECASE)).click()
    
            # 期待される結果: リンククリック後、URLが `/art` または作品一覧を示すURLに正しく遷移すること。
            # Assertion: Check URL after clicking the link.
>           expect(page).to_have_url("https://asami.tokyo/art")
E           AssertionError: Page URL expected to be 'https://asami.tokyo/art'
E           Actual value: https://asami.tokyo/about 
E           Call log:
E             - Expect "to_have_url" with timeout 5000ms
E               8 × unexpected value "https://asami.tokyo/about"

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:129: AssertionError
_____________________ test_4_view_the_video_link_external ______________________

page = <Page url='https://asami.tokyo/about'>

    def test_4_view_the_video_link_external(page: Page):
        """
        テストケース4: 「View the Video. ( Youtube / Vimeo )」リンクの動作確認 (外部遷移)
        目的: ユーザーが動画コンテンツへアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
>           page.goto("https://asami.tokyo/about")

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:143: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.11/site-packages/playwright/sync_api/_generated.py:9019: in goto
    self._sync(
.venv/lib/python3.11/site-packages/playwright/_impl/_page.py:555: in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.11/site-packages/playwright/_impl/_frame.py:153: in goto
    await self._channel.send(
.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:69: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x107468150>
cb = <function Channel.send.<locals>.<lambda> at 0x107999440>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        st: List[inspect.FrameInfo] = getattr(
            task, "__pw_stack__", None
        ) or inspect.stack(0)
    
        parsed_st = _extract_stack_trace_information_from_stack(st, is_internal, title)
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.Error: Page.goto: net::ERR_NETWORK_CHANGED at https://asami.tokyo/about
E           Call log:
E             - navigating to "https://asami.tokyo/about", waiting until "load"

.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:559: Error

During handling of the above exception, another exception occurred:

page = <Page url='https://asami.tokyo/about'>

    def test_4_view_the_video_link_external(page: Page):
        """
        テストケース4: 「View the Video. ( Youtube / Vimeo )」リンクの動作確認 (外部遷移)
        目的: ユーザーが動画コンテンツへアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
            page.goto("https://asami.tokyo/about")
            # Assertion: Check initial URL
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2: 「Art」セクション内の「View the Video. ( Youtube / Vimeo )」リンクをクリックする。
            # Assertion: Click "View the Video. ( Youtube / Vimeo )" link, expecting a new page/tab.
            with page.context.expect_page() as new_page_info:
                page.get_by_role("link", name=re.compile("View the Video", re.IGNORECASE)).click()
            new_page = new_page_info.value
    
            # 期待される結果: 新しいタブが開き、そのタブのURLが `youtube.com` または `vimeo.com` を含むこと。
            # Assertion: Check new page URL to contain Youtube or Vimeo domain using regex for partial match.
            expect(new_page).to_have_url(re.compile(r"youtube\.com|vimeo\.com", re.IGNORECASE))
    
            # Wait for the new page to fully load for robust screenshot and interaction.
            new_page.wait_for_load_state("load")
            page.screenshot(path=os.path.join(SAVE_DIR, "test_4_view_the_video_link_external_parent.png"))
            new_page.screenshot(path=os.path.join(SAVE_DIR, "test_4_view_the_video_link_external_new_page.png"))
    
        except Error as e:
>           pytest.fail(f"Playwright error in test_4_view_the_video_link_external: {e}")
E           Failed: Playwright error in test_4_view_the_video_link_external: Page.goto: net::ERR_NETWORK_CHANGED at https://asami.tokyo/about
E           Call log:
E             - navigating to "https://asami.tokyo/about", waiting until "load"

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:163: Failed
______________________ test_5_view_the_shop_link_external ______________________

page = <Page url='chrome-error://chromewebdata/'>

    def test_5_view_the_shop_link_external(page: Page):
        """
        テストケース5: 「View the Shop.」リンクの動作確認 (外部遷移)
        目的: ユーザーがショップへアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
>           page.goto("https://asami.tokyo/about")

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:172: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.11/site-packages/playwright/sync_api/_generated.py:9019: in goto
    self._sync(
.venv/lib/python3.11/site-packages/playwright/_impl/_page.py:555: in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.11/site-packages/playwright/_impl/_frame.py:153: in goto
    await self._channel.send(
.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:69: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x107468150>
cb = <function Channel.send.<locals>.<lambda> at 0x1079d0180>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        st: List[inspect.FrameInfo] = getattr(
            task, "__pw_stack__", None
        ) or inspect.stack(0)
    
        parsed_st = _extract_stack_trace_information_from_stack(st, is_internal, title)
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.Error: Page.goto: net::ERR_NETWORK_CHANGED at https://asami.tokyo/about
E           Call log:
E             - navigating to "https://asami.tokyo/about", waiting until "load"

.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:559: Error

During handling of the above exception, another exception occurred:

page = <Page url='chrome-error://chromewebdata/'>

    def test_5_view_the_shop_link_external(page: Page):
        """
        テストケース5: 「View the Shop.」リンクの動作確認 (外部遷移)
        目的: ユーザーがショップへアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
            page.goto("https://asami.tokyo/about")
            # Assertion: Check initial URL
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2: 「Art」セクション内の「View the Shop.」リンクをクリックする。
            # Assertion: Click "View the Shop." link, expecting a new page/tab.
            with page.context.expect_page() as new_page_info:
                page.get_by_role("link", name=re.compile("View the Shop", re.IGNORECASE)).click()
            new_page = new_page_info.value
    
            # 期待される結果: 新しいタブが開き、そのタブのURLが外部ショップのドメイン（例: `etsy.com`, `gumroad.com` など）を含むこと。
            # Assertion: Check new page URL to contain external shop domain using regex for partial match.
            expect(new_page).to_have_url(re.compile(r"etsy\.com|gumroad\.com", re.IGNORECASE))
    
            new_page.wait_for_load_state("load")
            page.screenshot(path=os.path.join(SAVE_DIR, "test_5_view_the_shop_link_external_parent.png"))
            new_page.screenshot(path=os.path.join(SAVE_DIR, "test_5_view_the_shop_link_external_new_page.png"))
    
        except Error as e:
>           pytest.fail(f"Playwright error in test_5_view_the_shop_link_external: {e}")
E           Failed: Playwright error in test_5_view_the_shop_link_external: Page.goto: net::ERR_NETWORK_CHANGED at https://asami.tokyo/about
E           Call log:
E             - navigating to "https://asami.tokyo/about", waiting until "load"

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:191: Failed
______________________ test_7_view_the_code_link_external ______________________

page = <Page url='https://asami.tokyo/about'>

    def test_7_view_the_code_link_external(page: Page):
        """
        テストケース7: 「View the Code.」リンクの動作確認 (外部遷移)
        目的: ユーザーが開発コードリポジトリ（GitHubなど）へアクセスできることを確認する。外部サイトへの遷移と新規タブでの開き方を検証する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
            page.goto("https://asami.tokyo/about")
            # Assertion: Check initial URL
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2: 「Development」セクション内の「View the Code.」リンクをクリックする。
            # Assertion: Click "View the Code." link, expecting a new page/tab.
            with page.context.expect_page() as new_page_info:
                page.get_by_role("link", name=re.compile("View the Code", re.IGNORECASE)).click()
            new_page = new_page_info.value
    
            # 期待される結果: 新しいタブが開き、そのタブのURLが `github.com` などのリポジトリドメインを含むこと。
            # Assertion: Check new page URL to contain GitHub domain using regex for partial match.
>           expect(new_page).to_have_url(re.compile(r"github\.com", re.IGNORECASE))
E           AssertionError: Page URL expected to be 're.compile('github\\.com', re.IGNORECASE)'
E           Actual value: chrome-error://chromewebdata/ 
E           Call log:
E             - Expect "to_have_url" with timeout 5000ms
E               8 × unexpected value "chrome-error://chromewebdata/"

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:241: AssertionError
_______________________ test_8_footer_copyright_display ________________________

page = <Page url='https://asami.tokyo/about'>

    def test_8_footer_copyright_display(page: Page):
        """
        テストケース8: フッターの著作権表示の確認
        目的: ページの法的表示（著作権表示）が最新かつ正確であることを確認する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
>           page.goto("https://asami.tokyo/about")

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:257: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.11/site-packages/playwright/sync_api/_generated.py:9019: in goto
    self._sync(
.venv/lib/python3.11/site-packages/playwright/_impl/_page.py:555: in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.venv/lib/python3.11/site-packages/playwright/_impl/_frame.py:153: in goto
    await self._channel.send(
.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:69: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x107468150>
cb = <function Channel.send.<locals>.<lambda> at 0x107c6d760>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        st: List[inspect.FrameInfo] = getattr(
            task, "__pw_stack__", None
        ) or inspect.stack(0)
    
        parsed_st = _extract_stack_trace_information_from_stack(st, is_internal, title)
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.Error: Page.goto: net::ERR_NETWORK_CHANGED at https://asami.tokyo/about
E           Call log:
E             - navigating to "https://asami.tokyo/about", waiting until "load"

.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py:559: Error

During handling of the above exception, another exception occurred:

page = <Page url='https://asami.tokyo/about'>

    def test_8_footer_copyright_display(page: Page):
        """
        テストケース8: フッターの著作権表示の確認
        目的: ページの法的表示（著作権表示）が最新かつ正確であることを確認する。
        """
        try:
            # Step 1: https://asami.tokyo/about にアクセスする。
            page.goto("https://asami.tokyo/about")
            # Assertion: Check initial URL
            expect(page).to_have_url("https://asami.tokyo/about")
    
            # Step 2: ページ下部のフッターエリアに表示されている著作権表示のテキストを取得する。
            # 期待される結果: 著作権表示が「© 2025 Asami K.」というテキストで表示されていること。
            # Assertion: Check footer copyright text using locator and to_contain_text for partial matching.
            # Note: The scenario specifies "2025". If the actual site shows a different year (e.g., current year),
            # this test will fail. Adjust the expected text if the site's copyright year is dynamic.
            expect(page.locator("footer")).to_contain_text("© 2025 Asami K.")
    
            page.screenshot(path=os.path.join(SAVE_DIR, "test_8_footer_copyright_display.png"))
    
        except Error as e:
>           pytest.fail(f"Playwright error in test_8_footer_copyright_display: {e}")
E           Failed: Playwright error in test_8_footer_copyright_display: Page.goto: net::ERR_NETWORK_CHANGED at https://asami.tokyo/about
E           Call log:
E             - navigating to "https://asami.tokyo/about", waiting until "load"

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:271: Failed
_________________________ test_10_nonexistent_page_404 _________________________

page = <Page url='https://asami.tokyo/about/nonexistentpage'>

    def test_10_nonexistent_page_404(page: Page):
        """
        テストケース10: 異常系: 存在しないパスへのアクセス時のエラーページ表示
        目的: ユーザーが誤って存在しないURLにアクセスした場合に、サイト全体のエラーハンドリングが適切であることを確認する。
        """
        try:
            # Step 1: 存在しないと想定されるURLに直接アクセスする。
            response = page.goto("https://asami.tokyo/about/nonexistentpage")
    
            # 期待される結果: HTTPステータスコードが `404` であること。
            # Assertion: Check HTTP status code for 404.
            assert response.status == 404, f"Expected 404 status code for non-existent page, but got {response.status}"
    
            # 期待される結果: ページコンテンツとして「404 Not Found」や「ページが見つかりません」といったユーザーフレンドリーなエラーメッセージが表示されていること。
            # Assertion: Check for 404 error message on the page.
            # Using regex to find common 404 phrases (case-insensitive) to be robust against minor text variations.
>           expect(page.get_by_text(re.compile(r"404|Not Found|ページが見つかりません", re.IGNORECASE))).to_be_visible()
E           AssertionError: Locator expected to be visible
E           Actual value: None
E           Error: strict mode violation: get_by_text(re.compile(r"404|Not Found|ページが見つかりません", re.IGNORECASE)) resolved to 3 elements:
E               1) <h1 data-v-4656b2ed="" class="font-semibold leading-none mb-4 sm:text-[110px] tabular-nums text-[80px]">404</h1> aka get_by_role("heading", name="404")
E               2) <h2 data-v-4656b2ed="" class="font-semibold mb-2 sm:text-3xl text-2xl">Page not found: /about/nonexistentpage</h2> aka get_by_role("heading", name="Page not found: /about/")
E               3) <p data-v-4656b2ed="" class="mb-4 px-2 text-[#64748B] text-md">Page not found: /about/nonexistentpage</p> aka get_by_role("paragraph")
E            
E           Call log:
E             - Expect "to_be_visible" with timeout 5000ms
E             - waiting for get_by_text(re.compile(r"404|Not Found|ページが見つかりません", re.IGNORECASE))

tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py:313: AssertionError
=========================== short test summary info ============================
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_1_about_page_basic_display_and_content
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_2_header_navigation_links
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_3_view_the_works_link
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_4_view_the_video_link_external
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_5_view_the_shop_link_external
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_7_view_the_code_link_external
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_8_footer_copyright_display
FAILED tests/generated/20251120_234257_asami_tokyo/test_asami_tokyo_about.py::test_10_nonexistent_page_404
========================= 8 failed, 2 passed in 58.33s =========================

```

### Stderr
```text

```

## 3. Screenshots

**Total Screenshots:** 31

### 01 Initial Load
![01 Initial Load](./01_initial_load.png)

### 01 Main Content Display
![01 Main Content Display](./01_main_content_display.png)

### 02 Global Navigation Start
![02 Global Navigation Start](./02_global_navigation_start.png)

### 03 Works List Display
![03 Works List Display](./03_works_list_display.png)

### 04 Footer Links About
![04 Footer Links About](./04_footer_links_about.png)

### 04 Footer Links Contact
![04 Footer Links Contact](./04_footer_links_contact.png)

### 04 Footer Links Start
![04 Footer Links Start](./04_footer_links_start.png)

### 05 Image Loading Check
![05 Image Loading Check](./05_image_loading_check.png)

### 06 Responsive Mobile
![06 Responsive Mobile](./06_responsive_mobile.png)

### 07 Page Title Check
![07 Page Title Check](./07_page_title_check.png)

### 08 Non Existent Url
![08 Non Existent Url](./08_non_existent_url.png)

### 09 Mobile Camera Page
![09 Mobile Camera Page](./09_mobile_camera_page.png)

### 09 No Console Errors
![09 No Console Errors](./09_no_console_errors.png)

### 10 Copyright Accuracy
![10 Copyright Accuracy](./10_copyright_accuracy.png)

### Fail 01 Main Content Display
![Fail 01 Main Content Display](./FAIL_01_main_content_display.png)

### Fail 02 Global Navigation Links
![Fail 02 Global Navigation Links](./FAIL_02_global_navigation_links.png)

### Fail 03 Works List Display
![Fail 03 Works List Display](./FAIL_03_works_list_display.png)

### Fail 09 No Console Errors
![Fail 09 No Console Errors](./FAIL_09_no_console_errors.png)

### Test 1 Homepage Main Elements
![Test 1 Homepage Main Elements](./test_1_homepage_main_elements.png)

### Test 4 Footer About
![Test 4 Footer About](./test_4_footer_about.png)

### Test 5 Footer Law
![Test 5 Footer Law](./test_5_footer_law.png)

### Test 6 Footer Contact
![Test 6 Footer Contact](./test_6_footer_contact.png)

### Test 6 View The Ai Prompt Link External New Page
![Test 6 View The Ai Prompt Link External New Page](./test_6_view_the_ai_prompt_link_external_new_page.png)

### Test 6 View The Ai Prompt Link External Parent
![Test 6 View The Ai Prompt Link External Parent](./test_6_view_the_ai_prompt_link_external_parent.png)

### Test 7 404 Page
![Test 7 404 Page](./test_7_404_page.png)

### Test 8 Mobile View Layout
![Test 8 Mobile View Layout](./test_8_mobile_view_layout.png)

### Test 9 Copyright Year
![Test 9 Copyright Year](./test_9_copyright_year.png)

### Test 9 Footer Nav Contact Link
![Test 9 Footer Nav Contact Link](./test_9_footer_nav_contact_link.png)

### Test Click Nonexistent Element Failure
![Test Click Nonexistent Element Failure](./test_click_nonexistent_element_failure.png)

### Test Footer Copyright Display
![Test Footer Copyright Display](./test_footer_copyright_display.png)

### Test Tech Stack Keywords Display
![Test Tech Stack Keywords Display](./test_tech_stack_keywords_display.png)

