import os
import pytest
import re
from playwright.sync_api import Page, expect, sync_playwright, Error

# Define the page fixture as instructed
@pytest.fixture(scope="module")
def page():
    """
    Provides a Playwright Page object for tests.
    Launches a Chromium browser, creates a new page, and closes the browser after all tests in the module are complete.
    """
    with sync_playwright() as p:
        # Launch browser in headless mode for CI/performance, set to False for local debugging
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Set viewport size to ensure consistent rendering across different environments
        page.set_viewport_size({'width': 1920, 'height': 1080})
        yield page
        browser.close()

# Directory for saving screenshots, relative to the test file
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        expect(page).to_have_title("About - Asami K.")

        # Step 3: ページ内に「I create visuals using TouchDesigner and Unreal Engine.」というテキストが表示されていることを確認する。
        # 期待される結果: 指定された主要な自己紹介テキストが表示されていること。
        # Assertion: Check main introduction text visibility using partial text match.
        expect(page.get_by_text("I create visuals using TouchDesigner and Unreal Engine", exact=False)).to_be_visible()

        # Step 4: 「Development」セクションに「I am developing the front-end of web applications using Vue.js and Nuxt.js.」というテキストが表示されていることを確認する。
        # 期待される結果: 指定された開発内容のテキストが表示されていること。
        # Assertion: Check Development section text visibility using partial text match.
        expect(page.get_by_text("I am developing the front-end of web applications using Vue.js and Nuxt.js", exact=False)).to_be_visible()
        
        # Save screenshot for debugging purposes
        page.screenshot(path=os.path.join(SAVE_DIR, "test_1_about_page_basic_display_and_content.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_1_about_page_basic_display_and_content: {e}")

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
        pytest.fail(f"Playwright error in test_2_header_navigation_links: {e}")

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
        expect(page).to_have_url("https://asami.tokyo/art")
        
        page.screenshot(path=os.path.join(SAVE_DIR, "test_3_view_the_works_link.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_3_view_the_works_link: {e}")

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
        pytest.fail(f"Playwright error in test_4_view_the_video_link_external: {e}")

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
        pytest.fail(f"Playwright error in test_5_view_the_shop_link_external: {e}")

def test_6_view_the_ai_prompt_link_external(page: Page):
    """
    テストケース6: 「View the AI Prompt.」リンクの動作確認
    目的: ユーザーがAI関連のブログ記事（Mediumなど）へアクセスできることを確認する。
    """
    try:
        # Step 1: https://asami.tokyo/about にアクセスする。
        page.goto("https://asami.tokyo/about")
        # Assertion: Check initial URL
        expect(page).to_have_url("https://asami.tokyo/about")

        # Step 2: 「Art」セクション内の「View the AI Prompt.」リンクをクリックする。
        # Assuming this external link also opens in a new tab for robustness.
        # Assertion: Click "View the AI Prompt." link, expecting a new page/tab.
        with page.context.expect_page() as new_page_info:
            page.get_by_role("link", name=re.compile("View the AI Prompt", re.IGNORECASE)).click()
        new_page = new_page_info.value

        # 期待される結果: リンククリック後、URLがMedium（`medium.com`）のドメインを含む、または記事ページへ正しく遷移すること。
        # Assertion: Check new page URL to contain Medium domain using regex for partial match.
        expect(new_page).to_have_url(re.compile(r"medium\.com", re.IGNORECASE))
        
        new_page.wait_for_load_state("load")
        page.screenshot(path=os.path.join(SAVE_DIR, "test_6_view_the_ai_prompt_link_external_parent.png"))
        new_page.screenshot(path=os.path.join(SAVE_DIR, "test_6_view_the_ai_prompt_link_external_new_page.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_6_view_the_ai_prompt_link_external: {e}")

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
        expect(new_page).to_have_url(re.compile(r"github\.com", re.IGNORECASE))
        
        new_page.wait_for_load_state("load")
        page.screenshot(path=os.path.join(SAVE_DIR, "test_7_view_the_code_link_external_parent.png"))
        new_page.screenshot(path=os.path.join(SAVE_DIR, "test_7_view_the_code_link_external_new_page.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_7_view_the_code_link_external: {e}")

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
        pytest.fail(f"Playwright error in test_8_footer_copyright_display: {e}")

def test_9_footer_nav_contact_link(page: Page):
    """
    テストケース9: フッターナビゲーションの動作確認 (「contact」リンク)
    目的: ユーザーが連絡手段（お問い合わせフォームなど）へアクセスできることを確認する。
    """
    try:
        # Step 1: https://asami.tokyo/about にアクセスする。
        page.goto("https://asami.tokyo/about")
        # Assertion: Check initial URL
        expect(page).to_have_url("https://asami.tokyo/about")

        # Step 2: フッター内の「contact」リンクをクリックする。
        # Assertion: Click the "contact" link in the footer using get_by_role with case-insensitive name match.
        page.get_by_role("link", name=re.compile("contact", re.IGNORECASE)).click()

        # 期待される結果: リンククリック後、URLが `/contact` またはお問い合わせフォームを示すURLに正しく遷移すること。
        # Assertion: Check URL after clicking "contact" link.
        expect(page).to_have_url("https://asami.tokyo/contact")
        
        page.screenshot(path=os.path.join(SAVE_DIR, "test_9_footer_nav_contact_link.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_9_footer_nav_contact_link: {e}")

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
        expect(page.get_by_text(re.compile(r"404|Not Found|ページが見つかりません", re.IGNORECASE))).to_be_visible()
        
        page.screenshot(path=os.path.join(SAVE_DIR, "test_10_nonexistent_page_404.png"))

    except Error as e:
        pytest.fail(f"Playwright error in test_10_nonexistent_page_404: {e}")