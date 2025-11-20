# Webapp Test Report

**Target URL:** https://asami.tokyo/
**Date:** 2025-11-20 22:55:57
**Status:** ❌ FAIL

## 1. Test Plan
## QAエンジニアによるテストシナリオ

与えられたWebページのURLとコンテンツを分析し、Playwrightでの自動化を念頭に置いたテストシナリオを最大10個作成しました。

---

### 分析と主要機能の特定

**Webサイトの目的:**
「Asami K」氏のポートフォリオ兼作品展示サイト。フロントエンドエンジニアとしてのスキルと、テクノロジーを活用したアート表現への情熱をアピールしている。

**主要機能:**

1.  **ページナビゲーション:**
    *   ヘッダーのグローバルナビゲーション（Top, Art, Camera, Apps, Asami K）によるページ遷移。
    *   フッターのナビゲーション（About, law, contact）によるページ遷移。
2.  **コンテンツ表示:**
    *   トップページでの自己紹介文、スキルセットの表示。
    *   各作品ページ（Art, Camera, Apps）での作品コンテンツ（特に画像）の表示。
    *   プロフィールページ（Asami K / About）での詳細情報の表示。
    *   法的事項ページ（law）の表示。
    *   連絡先ページ（contact）の表示（フォームの有無は不明だが、ページ自体は存在すると仮定）。
3.  **レスポンシブデザイン:** 異なるデバイスサイズでのレイアウトの適応。
4.  **サイト健全性:** リンク切れの有無、JavaScriptエラーの有無、存在しないURLへの対応。

---

### テストシナリオ

#### 1. トップページの主要コンテンツ正常表示テスト

*   **目的:** サイトの入口が正しく機能し、自己紹介文やスキル情報など、最も重要なコンテンツが初期ロード時に表示されることを確認する。
*   **手順:**
    1.  ブラウザで `https://asami.tokyo/` にアクセスする。
    2.  ページタイトルが期待通りであることを確認する。
    3.  「I'm a front-end engineer and I use technology to express my art.」というテキストが存在することを確認する。
    4.  Work SkillとHobby Skillのリストヘッダーが存在することを確認する。
    5.  フッターの著作権表示「© 2025 Asami K.」が存在することを確認する。
*   **期待される結果:**
    *   ページが正常にロードされ、ステータスコードが200 OKである。
    *   指定された自己紹介文、スキルセット、フッターの著作権表示が画面上に表示されている。

#### 2. グローバルナビゲーションのページ遷移テスト

*   **目的:** ヘッダーの主要ナビゲーションリンクが正しく機能し、対応するページへ遷移することを確認する。
*   **手順:**
    1.  トップページにアクセスする。
    2.  ヘッダーにある各ナビゲーションリンク（例: `Art`, `Camera`, `Apps`, `Asami K`）を順にクリックする。
    3.  各クリック後、遷移先のURLが期待されるパス（例: `/art`, `/camera`）になっていること、およびページタイトルまたは各ページの特徴的な要素（例: h1タグの内容）が表示されていることを確認する。
    4.  各ページから「Top」リンクをクリックしてトップページに戻れることも確認する。
*   **期待される結果:**
    *   各ナビゲーションリンクをクリックすると、対応するページに正常に遷移する。
    *   遷移先のURLが正しく、各ページの主要なコンテンツ（例: Artページであれば作品リスト、Asami Kページであればプロフィール詳細）が表示される。

#### 3. フッターナビゲーションのページ遷移テスト

*   **目的:** フッターの補助ナビゲーションリンクが正しく機能し、対応するページへ遷移することを確認する。
*   **手順:**
    1.  トップページにアクセスする。
    2.  フッターにある各リンク（`About`, `law`, `contact`）を順にクリックする。
    3.  各クリック後、遷移先のURLが期待されるパス（例: `/about`, `/law`, `/contact`）になっていること、およびページタイトルまたは各ページの特徴的な要素が表示されていることを確認する。
*   **期待される結果:**
    *   各フッターリンクをクリックすると、対応するページに正常に遷移する。
    *   遷移先のURLが正しく、各ページの主要なコンテンツが表示される（例: `law`ページであれば法的事項テキスト）。

#### 4. サイト内全内部リンクのリンク切れチェック

*   **目的:** サイト内の全ての内部リンクが有効であり、ユーザーがリンク切れのページに遭遇しないことを確認する。
*   **手順:**
    1.  トップページにアクセスする。
    2.  ページ内の全ての`<a>`タグを抽出し、その`href`属性が内部リンク（同じドメイン内のリンク）であるものをリストアップする。
    3.  リストアップされた各内部リンクについて、プログラム的にアクセス（`page.goto()`）し、HTTPステータスコードを確認する。
*   **期待される結果:**
    *   サイト内の全ての内部リンクがHTTP 200 OKを返し、正常にコンテンツが表示される。
    *   リンク切れ（404 Not Foundなど）が発生しない。

#### 5. レスポンシブデザインの主要ビューポート表示テスト

*   **目的:** 異なる画面幅（デスクトップ、タブレット、モバイル）でサイトのレイアウトが適切に表示され、コンテンツが崩れないことを確認する。
*   **手順:**
    1.  ブラウザのビューポートサイズを以下に設定し、トップページにアクセスする。
        *   デスクトップ (例: `1366x768`)
        *   タブレット (例: `768x1024`)
        *   モバイル (例: `375x667`)
    2.  各ビューポートサイズで、自己紹介文、スキルリスト、ナビゲーションメニュー、フッターなどが適切に配置され、レイアウトが崩れていないか、要素が重なっていないかなどを確認する。
    3.  （Playwrightで自動化する場合、主要な要素の表示・非表示、位置の簡易チェック、またはスクリーンショット比較を実装する）
*   **期待される結果:**
    *   各ビューポートサイズでコンテンツが適切に配置され、レイアウトの崩れ、要素の重なり、テキストの切断などが発生しない。
    *   モバイルビューでは、ナビゲーションメニューがハンバーガーメニューなどで適切に表示・操作できる（もしあれば）。

#### 6. 存在しないURLへのアクセス時のエラーページ表示テスト

*   **目的:** ユーザーが誤ったURLにアクセスした場合に、適切な404 Not Foundページが表示されることを確認し、サイトに戻る導線があるか検証する。
*   **手順:**
    1.  ブラウザで、サイトのドメインに対して存在しないパス（例: `https://asami.tokyo/nonexistent-page-12345`）に直接アクセスする。
    2.  表示されたページのHTTPステータスコードが404であることを確認する。
    3.  ページ上に「404 Not Found」や「ページが見つかりません」といったユーザーフレンドリーなメッセージが表示されていることを確認する。
    4.  サイトのトップページや他の主要ページに戻るためのリンクが存在するかを確認する。
*   **期待される結果:**
    *   HTTPステータスコードが404である。
    *   ユーザーフレンドリーなエラーメッセージと、サイト内の他のページへ戻るためのリンクが表示される。

#### 7. アート/作品ページでの画像コンテンツ表示テスト

*   **目的:** `Art`、`Camera`、`Apps`といった作品紹介ページで、主要な画像コンテンツが正しくロード・表示されることを確認する。
*   **手順:**
    1.  グローバルナビゲーションから「Art」ページに遷移する。
    2.  ページ上の全ての画像要素（`<img>`タグ）を取得する。
    3.  各画像が正常にロードされているか（`naturalWidth`プロパティが0より大きいかなど）、および代替テキスト（`alt`属性）が存在するかを確認する。
    4.  可能であれば、他の作品ページ（`Camera`, `Apps`）についても同様の確認を行う。
*   **期待される結果:**
    *   作品ページ上の全ての画像が正常にロードされ、表示される。
    *   各画像要素に適切な`alt`属性が設定されている。

#### 8. フッターの著作権表示年号の確認テスト

*   **目的:** フッターに表示されている著作権年号が「2025」と正しく表示されていることを確認する。これは未来の年号であるため、意図的な設定か、あるいは何らかの動的生成の問題がないかを確認する。
*   **手順:**
    1.  トップページにアクセスする。
    2.  フッター部分に表示されているテキストコンテンツを取得する。
    3.  取得したテキストが「© 2025 Asami K.」と完全に一致するか、または「2025」の文字列が含まれていることを確認する。
*   **期待される結果:**
    *   フッターの著作権表示が「© 2025 Asami K.」と正確に表示されている。

#### 9. コンソールログにおけるJavaScriptエラーの有無テスト

*   **目的:** ページロード時および主要な操作時に、ブラウザのコンソールに予期せぬJavaScriptエラーや重大な警告が出力されないことを確認する。
*   **手順:**
    1.  Playwrightの`page.on('console')`および`page.on('pageerror')`イベントをリッスンする設定を行う。
    2.  トップページにアクセスする。
    3.  グローバルナビゲーションの各リンクを順にクリックし、主要なページを巡回する。
    4.  テスト実行中にキャッチされたコンソールエラーやページエラーがないかを確認する。
*   **期待される結果:**
    *   ページロード時およびナビゲーション操作中に、ブラウザのコンソールにJavaScriptエラーや警告（特に`error`レベル）が出力されない。

#### 10. 連絡先（Contact）ページへのアクセスとフォームの存在確認

*   **目的:** フッターからアクセスできる「Contact」ページが存在し、もし連絡フォームがある場合はその基本的な表示を確認する。
*   **手順:**
    1.  トップページにアクセスする。
    2.  フッターの「contact」リンクをクリックして、連絡先ページに遷移する。
    3.  遷移先のURLが期待されるパス（例: `/contact`）であることを確認する。
    4.  ページタイトルまたは主要な見出しが「Contact」または類似のテキストであることを確認する。
    5.  もし入力フィールド（`input`、`textarea`）や送信ボタン（`button[type="submit"]`）が存在する場合、それらが画面上に表示されていることを確認する。
*   **期待される結果:**
    *   「Contact」ページに正常に遷移し、URLとタイトルが正しい。
    *   連絡先に関する情報（テキスト、メールアドレス、もしあれば連絡フォームの入力フィールドと送信ボタン）が画面に表示されている。

## 2. Execution Result
**Return Code:** 1

### Stdout
```text
============================= test session starts ==============================
platform darwin -- Python 3.11.5, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/asami/develop/app/ai-agent
plugins: base-url-2.1.0, playwright-0.7.1
collected 10 items

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py FFF.FFF. [ 80%]
F.                                                                       [100%]

=================================== FAILURES ===================================
________________________ test_homepage_content_display _________________________

page = <Page url='https://asami.tokyo/'>

    def test_homepage_content_display(page: Page):
        """
        Scenario 1: トップページの主要コンテンツ正常表示テスト
        目的: サイトの入口が正しく機能し、自己紹介文やスキル情報など、最も重要なコンテンツが初期ロード時に表示されることを確認する。
        """
        try:
            # Navigate to the homepage
            response = page.goto("https://asami.tokyo/")
    
            # Assert: Page loaded successfully (HTTP status 200)
            assert response.status == 200, f"Expected 200, got {response.status} for {page.url}"
            # Assert: Current URL is the expected one
            expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))
    
            # Assert: Page title contains "Asami K"
>           expect(page).to_have_title(re.compile(r"Asami K", re.IGNORECASE))
E           AssertionError: Page title expected to be 're.compile('Asami K', re.IGNORECASE)'
E           Actual value: About | asami.tokyo 
E           Call log:
E             - Expect "to_have_title" with timeout 5000ms
E               9 × unexpected value "About | asami.tokyo"

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:36: AssertionError
_________________________ test_global_navigation_links _________________________

page = <Page url='https://asami.tokyo/'>

    def test_global_navigation_links(page: Page):
        """
        Scenario 2: グローバルナビゲーションのページ遷移テスト
        目的: ヘッダーの主要ナビゲーションリンクが正しく機能し、対応するページへ遷移することを確認する。
        """
        try:
            page.goto("https://asami.tokyo/")
            expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))
    
            nav_links = {
                "Art": "/art",
                "Camera": "/camera",
                "Apps": "/apps",
                "Asami K": "/asami", # Assuming "Asami K" links to /asami
            }
    
            for link_name, expected_path in nav_links.items():
                # Assert: Navigate to the respective page
                nav_locator = page.get_by_role("link", name=re.compile(link_name, re.IGNORECASE)).first
>               expect(nav_locator).to_be_visible() # Ensure link is visible before clicking
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E               AssertionError: Locator expected to be visible
E               Actual value: None
E               Error: element(s) not found 
E               Call log:
E                 - Expect "to_be_visible" with timeout 5000ms
E                 - waiting for get_by_role("link", name=re.compile(r"Art", re.IGNORECASE)).first

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:70: AssertionError
_________________________ test_footer_navigation_links _________________________

page = <Page url='https://asami.tokyo/law'>

    def test_footer_navigation_links(page: Page):
        """
        Scenario 3: フッターナビゲーションのページ遷移テスト
        目的: フッターの補助ナビゲーションリンクが正しく機能し、対応するページへ遷移することを確認する。
        """
        try:
            page.goto("https://asami.tokyo/")
            expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))
    
            footer_links = {
                "About": "/about",
                "law": "/law",
                "contact": "/contact",
            }
    
            for link_name, expected_path in footer_links.items():
                # Assert: Navigate to the respective page
                # Use locator and filter by text within footer for robustness
                footer_link_locator = page.locator("footer").get_by_role("link", name=re.compile(link_name, re.IGNORECASE)).first
                expect(footer_link_locator).to_be_visible() # Ensure link is visible
                footer_link_locator.click()
    
                # Assert: URL matches the expected path
                expect(page).to_have_url(re.compile(rf"https://asami\.tokyo{expected_path}/?"))
                # Assert: A unique element/heading on the target page is visible
                # Use page.get_by_text as a robust way to check for page content
>               expect(page.get_by_role("heading", name=re.compile(link_name, re.IGNORECASE)).first).to_be_visible()
E               AssertionError: Locator expected to be visible
E               Actual value: None
E               Error: element(s) not found 
E               Call log:
E                 - Expect "to_be_visible" with timeout 5000ms
E                 - waiting for get_by_role("heading", name=re.compile(r"law", re.IGNORECASE)).first

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:113: AssertionError
_______________________ test_responsive_design_viewports _______________________

page = <Page url='https://asami.tokyo/'>

    def test_responsive_design_viewports(page: Page):
        """
        Scenario 5: レスポンシブデザインの主要ビューポート表示テスト
        目的: 異なる画面幅（デスクトップ、タブレット、モバイル）でサイトのレイアウトが適切に表示されることを確認する。
        """
        try:
            viewports = {
                "Desktop": {"width": 1366, "height": 768},
                "Tablet": {"width": 768, "height": 1024},
                "Mobile": {"width": 375, "height": 667},
            }
    
            save_dir = os.path.dirname(os.path.abspath(__file__))
    
            for name, size in viewports.items():
                page.set_viewport_size(size)
                page.goto("https://asami.tokyo/")
                expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))
    
                # Assert: Main heading/introduction visible
                expect(page.get_by_text("I'm a front-end engineer", exact=False)).to_be_visible()
                # Assert: Navigation element (e.g., "Top" link) is visible.
                # In mobile, it might be part of a hamburger menu, so check for the menu button.
                if name == "Mobile":
                    # Assuming a common pattern for a mobile menu button (e.g., a button with an icon or specific role)
                    # This might need adjustment based on the actual site's mobile menu implementation.
                    # If there's no hamburger menu, just check for a visible nav link.
                    mobile_menu_button = page.get_by_role("button", name=re.compile(r"menu|toggle navigation", re.IGNORECASE))
                    if mobile_menu_button.count() > 0: # If a mobile menu button exists
                        expect(mobile_menu_button).to_be_visible()
                    else: # Fallback: check if a top link is still visible (e.g., fixed header)
                        expect(page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
                else:
>                   expect(page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
E                   AssertionError: Locator expected to be visible
E                   Actual value: None
E                   Error: element(s) not found 
E                   Call log:
E                     - Expect "to_be_visible" with timeout 5000ms
E                     - waiting for get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:191: AssertionError
_______________________ test_nonexistent_url_error_page ________________________

page = <Page url='https://asami.tokyo/nonexistent-page-12345'>

    def test_nonexistent_url_error_page(page: Page):
        """
        Scenario 6: 存在しないURLへのアクセス時のエラーページ表示テスト
        目的: ユーザーが誤ったURLにアクセスした場合に、適切な404 Not Foundページが表示されることを確認する。
        """
        try:
            non_existent_url = "https://asami.tokyo/nonexistent-page-12345"
            response = page.goto(non_existent_url)
    
            # Assert: HTTP status code is 404
            assert response.status == 404, f"Expected 404, got {response.status} for {non_existent_url}"
            # Assert: Page contains a 404 error message
>           expect(page.get_by_text(re.compile(r"404 Not Found|ページが見つかりません", re.IGNORECASE))).to_be_visible()
E           AssertionError: Locator expected to be visible
E           Actual value: None
E           Error: element(s) not found 
E           Call log:
E             - Expect "to_be_visible" with timeout 5000ms
E             - waiting for get_by_text(re.compile(r"404 Not Found|ページが見つかりません", re.IGNORECASE))

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:215: AssertionError
_____________________ test_art_page_image_content_display ______________________

page = <Page url='https://asami.tokyo/art/'>

    def test_art_page_image_content_display(page: Page):
        """
        Scenario 7: アート/作品ページでの画像コンテンツ表示テスト
        目的: 'Art'ページで、主要な画像コンテンツが正しくロード・表示されることを確認する。
        """
        try:
            # Navigate to the Art page
            page.goto("https://asami.tokyo/art/")
            expect(page).to_have_url(re.compile(r"https://asami\.tokyo/art/?"))
    
            # Assert: Main heading for the Art page is visible
            expect(page.get_by_role("heading", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()
    
            # Get all image elements on the page
            image_locators = page.locator("img").all()
    
            if not image_locators:
                pytest.fail("No image elements found on the Art page.")
    
            # Iterate through images and assert their properties
            for img_locator in image_locators:
                # Assert: Image is visible
                expect(img_locator).to_be_visible()
                # Assert: Image has loaded (naturalWidth > 0)
                # Evaluate JavaScript directly on the element
                is_loaded = img_locator.evaluate("img => img.naturalWidth > 0")
>               assert is_loaded, f"Image failed to load: {img_locator.get_attribute('src')}"
E               AssertionError: Image failed to load: https://as1.ftcdn.net/v2/jpg/10/14/91/02/1000_F_1014910239_Cc8dAs6B9YfBUSYCxMYhDJBeqpG0Ojwf.jpg
E               assert False

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:248: AssertionError
_____________________ test_no_javascript_errors_on_console _____________________

page = <Page url='https://asami.tokyo/'>

    def test_no_javascript_errors_on_console(page: Page):
        """
        Scenario 9: コンソールログにおけるJavaScriptエラーの有無テスト
        目的: ページロード時および主要な操作時に、ブラウザのコンソールに予期せぬJavaScriptエラーや重大な警告が出力されないことを確認する。
        """
        try:
            console_errors = []
            page_errors = []
    
            # Listen for console messages and page errors
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
    
            # Navigate to homepage and a few other key pages
            page.goto("https://asami.tokyo/")
>           page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE)).click()

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:289: 
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

self = <playwright._impl._connection.Connection object at 0x1029d3a90>
cb = <function Channel.send.<locals>.<lambda> at 0x103cdf380>
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

page = <Page url='https://asami.tokyo/'>

    def test_no_javascript_errors_on_console(page: Page):
        """
        Scenario 9: コンソールログにおけるJavaScriptエラーの有無テスト
        目的: ページロード時および主要な操作時に、ブラウザのコンソールに予期せぬJavaScriptエラーや重大な警告が出力されないことを確認する。
        """
        try:
            console_errors = []
            page_errors = []
    
            # Listen for console messages and page errors
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda err: page_errors.append(str(err)))
    
            # Navigate to homepage and a few other key pages
            page.goto("https://asami.tokyo/")
            page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE)).click()
            page.get_by_role("link", name=re.compile(r"Camera", re.IGNORECASE)).click()
            page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE)).click() # Go back to homepage
            page.locator("footer").get_by_role("link", name=re.compile(r"About", re.IGNORECASE)).click()
    
            # Assert: No JavaScript errors logged to the console
            assert not console_errors, \
                f"JavaScript console errors found: \n{os.linesep.join(console_errors)}"
            # Assert: No uncaught page errors occurred
            assert not page_errors, \
                f"Page errors (uncaught exceptions) found: \n{os.linesep.join(page_errors)}"
    
        except Error as e:
>           pytest.fail(f"Playwright error during test_no_javascript_errors_on_console: {e}")
E           Failed: Playwright error during test_no_javascript_errors_on_console: Locator.click: Timeout 30000ms exceeded.
E           Call log:
E             - waiting for get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))

tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py:302: Failed
=========================== short test summary info ============================
FAILED tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py::test_homepage_content_display
FAILED tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py::test_global_navigation_links
FAILED tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py::test_footer_navigation_links
FAILED tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py::test_responsive_design_viewports
FAILED tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py::test_nonexistent_url_error_page
FAILED tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py::test_art_page_image_content_display
FAILED tests/generated/20251120_225329_asami_tokyo/test_asami_tokyo.py::test_no_javascript_errors_on_console
==================== 7 failed, 3 passed in 86.79s (0:01:26) ====================

```

### Stderr
```text

```
