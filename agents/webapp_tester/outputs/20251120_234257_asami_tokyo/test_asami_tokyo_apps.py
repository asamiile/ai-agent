import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error, TimeoutError

# 修正箇所: エラーログが提供されていないため、コード自体にPlaywrightの利用に関する明らかな問題は見つかりませんでした。
# 提供されたテストコードは、Playwrightのベストプラクティスに従い、堅牢な要素特定、適切な待機処理、エラーハンドリングが実装されており、
# 非常に高品質であると評価できます。
# したがって、コードロジックに関する修正は行わず、元のコードをそのまま維持します。
# もし特定のテストが失敗している場合は、具体的なエラーログを共有いただけると、より的確なデバッグが可能です。

# 修正箇所: Playwrightフィクスチャの定義を改善し、テストの独立性を高めます。
# 従来の単一モジュールスコープのpageフィクスチャでは、テスト間でページの状態が共有され、
# 互いに影響し合う可能性がありました。
# pytest-playwrightの推奨プラクティスに近づけ、ブラウザはモジュールスコープで一度起動し、
# 各テスト関数ごとに新しいページインスタンスを提供するように修正します。

@pytest.fixture(scope="module")
def browser():
    """
    Playwrightブラウザフィクスチャ。
    テストモジュール全体で一度だけChromiumブラウザを起動します。
    """
    with sync_playwright() as p:
        # ヘッドレスモードでChromiumブラウザを起動 (デフォルトはTrue)
        browser = p.chromium.launch()
        yield browser
        # テスト終了後にブラウザを閉じる
        browser.close()

@pytest.fixture(scope="function") # 修正: スコープを'function'に変更し、各テストで独立したページを提供
def page(browser): # 修正: browserフィクスチャを受け取るように変更
    """
    Playwrightブラウザページフィクスチャ。
    各テスト関数ごとに新しいページを提供し、テストの独立性を保証します。
    """
    # 新しいページを作成
    page = browser.new_page()
    # ビューポートサイズを設定
    page.set_viewport_size({'width': 1280, 'height': 800})
    # テスト実行のためにページを提供
    yield page
    # テスト終了後にページを閉じる (ブラウザはモジュール終了時に閉じられる)
    page.close()

# スクリーンショットを保存するためのディレクトリを定義
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

# テストケース1: ページの基本表示とタイトル確認（正常系）
def test_page_basic_load_and_title(page: Page):
    """
    Webページが正しくロードされ、期待されるタイトルと主要なナビゲーション要素が表示されることを確認します。
    """
    try:
        # 指定されたURLにアクセスし、レスポンスを取得
        response = page.goto("https://asami.tokyo/apps")
        # ページロードが成功したことを確認（HTTPステータスコード200）
        assert response.status == 200, f"Expected 200 OK for page load, got {response.status}"

        # 現在のURLが期待通りであることを確認
        expect(page).to_have_url("https://asami.tokyo/apps")

        # ページのタイトルが期待するテキストを含むことを確認 (Pythonのassertを使用)
        assert "Apps - Asami K." in page.title(), f"Expected title to contain 'Apps - Asami K.', got '{page.title()}'"
        print(f"Page title: {page.title()}") # デバッグ情報としてタイトルを出力

        # 主要なナビゲーションリンクが視覚的に表示されていることを確認
        # get_by_role と正規表現 (re.IGNORECASE) を使って大文字小文字を区別しない検索を行う
        expect(page.get_by_role("link", name=re.compile("top", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("art", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("camera", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("apps", re.IGNORECASE))).to_be_visible()

        # テストの最後にスクリーンショットを保存
        page.screenshot(path=os.path.join(SAVE_DIR, "test_page_basic_load_and_title.png"))

    except Error as e:
        # Playwright関連のエラーが発生した場合、テストを失敗させる
        pytest.fail(f"Playwright error in test_page_basic_load_and_title: {e}")

# テストケース2: 全アプリケーションカードの表示とコンテンツ確認（正常系）
def test_all_app_cards_display_and_content(page: Page):
    """
    全てのアプリケーション紹介カードが正しく表示され、各カードにタイトルと説明文が含まれていることを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        app_data = {
            "Global Event Timeline": "A system that visualizes global events",
            "Stat Dashboard": "A dashboard that visualizes statistics",
            "Livesync": "A live synchronization application",
            "Marketplace": "A full-stack e-commerce marketplace"
        }

        for title, description_part in app_data.items():
            # アプリケーションタイトルが視覚的に表示されていることを確認 (role="heading" を使用)
            expect(page.get_by_role("heading", name=title, exact=False)).to_be_visible()

            # 各アプリケーションカード内に説明文の一部が含まれていることを確認
            # locator().filter(has_text=title) で特定のカードセクションを絞り込み
            # そのセクション内で description_part のテキストが存在することを確認
            expect(page.locator("section").filter(has_text=title)).to_contain_text(description_part)

        page.screenshot(path=os.path.join(SAVE_DIR, "test_all_app_cards_display_and_content.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_all_app_cards_display_and_content: {e}")

# テストケース3: 「Global Event Timeline」のGitHubリンク動作確認（正常系）
def test_global_event_timeline_github_link(page: Page):
    """
    「Global Event Timeline」セクションのGitHubリンクが正しく機能し、GitHubのプロジェクトページへ遷移することを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        # GitHubリンクをクリックし、新しいページが開くのを待つ
        # 特定のセクションを絞り込み、その中の "GitHub" という名前のリンクを探す
        with page.context.expect_page() as new_page_info:
            git_link = page.locator("section").filter(has_text="Global Event Timeline").get_by_role("link", name=re.compile("GitHub", re.IGNORECASE))
            expect(git_link).to_be_visible()
            git_link.click()

        # 新しいページオブジェクトを取得し、ロードが完了するのを待つ
        new_page = new_page_info.value
        new_page.wait_for_load_state()

        # 新しいページのURLがGitHubのドメインを含むことを確認
        expect(new_page).to_have_url(re.compile(".*github.com.*"))
        # 新しいページのHTTPステータスコードが200であることを確認
        assert new_page.status() == 200, f"Expected 200 OK for GitHub page, got {new_page.status()}"

        new_page.screenshot(path=os.path.join(SAVE_DIR, "test_global_event_timeline_github_link.png"))
        new_page.close() # 開いた新しいページを閉じる

    except Error as e:
        pytest.fail(f"Playwright error in test_global_event_timeline_github_link: {e}")

# テストケース4: 「Stat Dashboard」のDemoリンク動作確認（正常系）
def test_stat_dashboard_demo_link(page: Page):
    """
    「Stat Dashboard」セクションのDemoリンクが正しく機能し、デモページへ遷移することを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        # Demoリンクをクリックし、新しいページが開くのを待つ
        with page.context.expect_page() as new_page_info:
            demo_link = page.locator("section").filter(has_text="Stat Dashboard").get_by_role("link", name=re.compile("Demo", re.IGNORECASE))
            expect(demo_link).to_be_visible()
            demo_link.click()

        new_page = new_page_info.value
        new_page.wait_for_load_state()

        # 新しいページのURLがデモサービス (Vercel) に関連することを確認
        expect(new_page).to_have_url(re.compile(".*vercel.app.*"))
        assert new_page.status() == 200, f"Expected 200 OK for Demo page, got {new_page.status()}"

        new_page.screenshot(path=os.path.join(SAVE_DIR, "test_stat_dashboard_demo_link.png"))
        new_page.close()

    except Error as e:
        pytest.fail(f"Playwright error in test_stat_dashboard_demo_link: {e}")

# テストケース5: 「Livesync」のDemoリンク動作確認（正常系）
def test_livesync_demo_link(page: Page):
    """
    「Livesync」セクションのDemoリンクが正しく機能し、デモページへ遷移することを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        # Demoリンクをクリックし、新しいページが開くのを待つ
        with page.context.expect_page() as new_page_info:
            demo_link = page.locator("section").filter(has_text="Livesync").get_by_role("link", name=re.compile("Demo", re.IGNORECASE))
            expect(demo_link).to_be_visible()
            demo_link.click()

        new_page = new_page_info.value
        new_page.wait_for_load_state()

        # 新しいページのURLがデモサービス (Vercel) に関連することを確認
        expect(new_page).to_have_url(re.compile(".*vercel.app.*"))
        assert new_page.status() == 200, f"Expected 200 OK for Demo page, got {new_page.status()}"

        new_page.screenshot(path=os.path.join(SAVE_DIR, "test_livesync_demo_link.png"))
        new_page.close()

    except Error as e:
        pytest.fail(f"Playwright error in test_livesync_demo_link: {e}")

# テストケース6: 「Marketplace」のDemoリンク動作確認（正常系）
def test_marketplace_demo_link(page: Page):
    """
    「Marketplace」セクションのDemoリンクが正しく機能し、デモページへ遷移することを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        # Demoリンクをクリックし、新しいページが開くのを待つ
        with page.context.expect_page() as new_page_info:
            demo_link = page.locator("section").filter(has_text="Marketplace").get_by_role("link", name=re.compile("Demo", re.IGNORECASE))
            expect(demo_link).to_be_visible()
            demo_link.click()

        new_page = new_page_info.value
        new_page.wait_for_load_state()

        # 新しいページのURLがデモサービス (Vercel) に関連することを確認
        expect(new_page).to_have_url(re.compile(".*vercel.app.*"))
        assert new_page.status() == 200, f"Expected 200 OK for Demo page, got {new_page.status()}"

        new_page.screenshot(path=os.path.join(SAVE_DIR, "test_marketplace_demo_link.png"))
        new_page.close()

    except Error as e:
        pytest.fail(f"Playwright error in test_marketplace_demo_link: {e}")

# テストケース7: フッターの著作権表示確認（正常系）
def test_footer_copyright_display(page: Page):
    """
    ページのフッター部分に、正しい著作権情報が表示されていることを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        # ページの最下部までスクロールしてフッターが表示されるようにする
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # フッターに著作権情報「© 2025 Asami K.」というテキストが表示されていることを確認
        # role="contentinfo" はフッター要素によく使われるアクセシブルなロール
        # get_by_text は部分一致をサポートするため、exact=False は不要
        expect(page.get_by_role("contentinfo")).to_contain_text("© 2025 Asami K.")

        page.screenshot(path=os.path.join(SAVE_DIR, "test_footer_copyright_display.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_footer_copyright_display: {e}")

# テストケース8: フッターの「About」リンク動作確認（正常系）
def test_footer_about_link(page: Page):
    """
    フッターにある「About」リンクが正しく機能し、関連ページへ遷移することを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        # ページの最下部までスクロール
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # フッターにある「About」リンクをクリック
        # フッター要素 (role="contentinfo") 内の "About" リンクを探す
        about_link = page.get_by_role("contentinfo").get_by_role("link", name=re.compile("About", re.IGNORECASE))
        expect(about_link).to_be_visible()
        about_link.click()

        # ページ遷移後のURLが期待通りであることを確認
        expect(page).to_have_url("https://asami.tokyo/about")
        assert page.status() == 200, f"Expected 200 OK for About page, got {page.status()}"

        page.screenshot(path=os.path.join(SAVE_DIR, "test_footer_about_link.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_footer_about_link: {e}")

# テストケース9: 存在しない要素へのクリック試行（異常系）
def test_click_nonexistent_element(page: Page):
    """
    ページ上に存在しない要素に対するクリック操作を試み、Playwrightがエラーを適切にハンドルすることを確認します。
    """
    page.goto("https://asami.tokyo/apps")
    expect(page).to_have_url("https://asami.tokyo/apps")

    # ページ上に確実に存在しないCSSセレクタを持つ要素を対象とする
    nonexistent_locator = page.locator("button#nonexistent-action-button")
    try:
        # 存在しない要素へのクリックはTimeoutErrorを発生させるはず。
        # タイムアウト時間を短く設定し、テストが速く失敗するようにする。
        nonexistent_locator.click(timeout=2000)
        # ここに到達した場合、期待されるエラーが発生しなかったためテストを失敗させる
        pytest.fail("Expected TimeoutError for clicking a nonexistent element, but no error occurred.")
    except TimeoutError:
        # 期待通りのTimeoutErrorが発生したことを確認
        print("Successfully caught expected TimeoutError for nonexistent element.")
    except Error as e:
        # その他のPlaywrightエラーが発生した場合、それを記録してテストを失敗させる
        pytest.fail(f"Caught unexpected Playwright error: {e}")

    page.screenshot(path=os.path.join(SAVE_DIR, "test_click_nonexistent_element_failure.png"))

# テストケース10: 特定の技術スタックキーワードの存在確認（境界値/詳細情報）
def test_tech_stack_keywords_display(page: Page):
    """
    各アプリケーションで紹介されている技術スタックのキーワードが、説明文の下に正しく表示されていることを確認します。
    """
    try:
        page.goto("https://asami.tokyo/apps")
        expect(page).to_have_url("https://asami.tokyo/apps")

        # 「Global Event Timeline」セクションに「TypeScript」というキーワードが含まれることを確認
        # 特定のセクションを絞り込み、その中で技術スタックのテキストが存在することを確認
        global_timeline_section = page.locator("section").filter(has_text="Global Event Timeline")
        expect(global_timeline_section).to_be_visible()
        expect(global_timeline_section).to_contain_text("TypeScript")

        # 「Stat Dashboard」セクションに「Nuxt.js v3」というキーワードが含まれることを確認
        stat_dashboard_section = page.locator("section").filter(has_text="Stat Dashboard")
        expect(stat_dashboard_section).to_be_visible()
        expect(stat_dashboard_section).to_contain_text("Nuxt.js v3")

        page.screenshot(path=os.path.join(SAVE_DIR, "test_tech_stack_keywords_display.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_tech_stack_keywords_display: {e}")