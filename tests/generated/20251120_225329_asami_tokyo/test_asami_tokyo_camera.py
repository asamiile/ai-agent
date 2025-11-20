import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

# Define the base URL for convenience
BASE_URL = "https://asami.tokyo"
CAMERA_PAGE_URL = f"{BASE_URL}/camera"

@pytest.fixture(scope="module")
def page():
    """
    Playwright page fixture.
    This fixture ensures a Playwright page is available for tests
    even if pytest-playwright is not explicitly installed or configured.
    """
    with sync_playwright() as p:
        # Launch a Chromium browser
        browser = p.chromium.launch()
        # Create a new browser page
        page = browser.new_page()
        # Yield the page to the tests
        yield page
        # Close the browser after all tests in the module are done
        browser.close()

def save_screenshot_on_failure(page: Page, test_name: str):
    """Saves a screenshot if a test fails."""
    save_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_path = os.path.join(save_dir, f"fail_{test_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")

def test_01_page_load_and_main_content(page: Page):
    """
    [正常系] ページロードと主要コンテンツの表示
    「Camera」ページが正常にロードされ、期待される主要なテキストコンテンツおよび
    画像コンテンツのプレースホルダーが正しく表示されることを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL}...")
        response = page.goto(CAMERA_PAGE_URL)

        # アサーション: ページのURLが正しいことを確認
        print(f"Asserting page URL is {CAMERA_PAGE_URL}...")
        expect(page).to_have_url(CAMERA_PAGE_URL)
        assert response.status == 200, f"Expected status 200, got {response.status}"

        # アサーション: ページのタイトルに「Camera」が含まれていることを確認
        print("Asserting page title contains 'Camera'...")
        expect(page).to_have_title(re.compile(r"Camera", re.IGNORECASE))

        # アサーション: 「Tools: DJI Osmo Pocket 3...」というテキストが表示されていることを確認
        print("Asserting 'Tools: DJI Osmo Pocket 3...' text is visible...")
        expect(page.get_by_text("Tools: DJI Osmo Pocket 3", exact=False)).to_be_visible()

        # アサーション: 「Water's Edge」など、コンテンツリストに含まれる複数の項目が可視状態であることを確認
        print("Asserting 'Water's Edge' content is visible...")
        expect(page.get_by_text("Water's Edge", exact=False).first).to_be_visible()

    except Error as e:
        save_screenshot_on_failure(page, "test_01_page_load_and_main_content")
        pytest.fail(f"Playwright error during test_01_page_load_and_main_content: {e}")

def test_02_global_nav_top_link(page: Page):
    """
    [正常系] グローバルナビゲーション「Top」への遷移
    ヘッダーの「Top」リンクが正しく機能し、ウェブサイトのトップページへ遷移することを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_02...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: ヘッダーナビゲーション内の「Top」リンクをクリック
        print("Clicking 'Top' navigation link...")
        page.get_by_role("link", name=re.compile(r"top", re.IGNORECASE)).click()

        # アサーション: ページがトップページへ遷移したことを確認
        print(f"Asserting page URL is {BASE_URL}/...")
        expect(page).to_have_url(f"{BASE_URL}/")

    except Error as e:
        save_screenshot_on_failure(page, "test_02_global_nav_top_link")
        pytest.fail(f"Playwright error during test_02_global_nav_top_link: {e}")

def test_03_global_nav_art_link(page: Page):
    """
    [正常系] グローバルナビゲーション「Art」への遷移
    ヘッダーの「Art」リンクが正しく機能し、対応する「Art」ページへ遷移することを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_03...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: ヘッダーナビゲーション内の「Art」リンクをクリック
        print("Clicking 'Art' navigation link...")
        page.get_by_role("link", name=re.compile(r"art", re.IGNORECASE)).click()

        # アサーション: ページが「Art」ページへ遷移したことを確認
        print(f"Asserting page URL is {BASE_URL}/art...")
        expect(page).to_have_url(f"{BASE_URL}/art")

    except Error as e:
        save_screenshot_on_failure(page, "test_03_global_nav_art_link")
        pytest.fail(f"Playwright error during test_03_global_nav_art_link: {e}")

def test_04_global_nav_apps_link(page: Page):
    """
    [正常系] グローバルナビゲーション「Apps」への遷移
    ヘッダーの「Apps」リンクが正しく機能し、対応する「Apps」ページへ遷移することを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_04...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: ヘッダーナビゲーション内の「Apps」リンクをクリック
        print("Clicking 'Apps' navigation link...")
        page.get_by_role("link", name=re.compile(r"apps", re.IGNORECASE)).click()

        # アサーション: ページが「Apps」ページへ遷移したことを確認
        print(f"Asserting page URL is {BASE_URL}/apps...")
        expect(page).to_have_url(f"{BASE_URL}/apps")

    except Error as e:
        save_screenshot_on_failure(page, "test_04_global_nav_apps_link")
        pytest.fail(f"Playwright error during test_04_global_nav_apps_link: {e}")

def test_05_current_page_camera_nav_display(page: Page):
    """
    [正常系] 現在のページ「Camera」のナビゲーション表示
    現在のページ（Camera）に対応するグローバルナビゲーション要素が、
    クリックで同じページに留まることを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_05...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: ヘッダーナビゲーション内の「Camera」要素を探し、クリック
        print("Clicking 'Camera' navigation link (current page)...")
        page.get_by_role("link", name=re.compile(r"camera", re.IGNORECASE)).click()

        # アサーション: URLが変わらない（現在のページに留まる）ことを検証
        print(f"Asserting page URL remains {CAMERA_PAGE_URL}...")
        expect(page).to_have_url(CAMERA_PAGE_URL)

    except Error as e:
        save_screenshot_on_failure(page, "test_05_current_page_camera_nav_display")
        pytest.fail(f"Playwright error during test_05_current_page_camera_nav_display: {e}")

def test_06_footer_about_link(page: Page):
    """
    [正常系] フッター「About」リンクへの遷移
    フッターの「About」リンクが正しく機能し、対応するページへ遷移することを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_06...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: フッターナビゲーション内の「About」リンクをクリック
        print("Clicking 'About' footer link...")
        page.get_by_role("link", name=re.compile(r"about", re.IGNORECASE)).click()

        # アサーション: ページが「About」ページへ遷移したことを確認
        print(f"Asserting page URL is {BASE_URL}/about...")
        expect(page).to_have_url(f"{BASE_URL}/about")

    except Error as e:
        save_screenshot_on_failure(page, "test_06_footer_about_link")
        pytest.fail(f"Playwright error during test_06_footer_about_link: {e}")

def test_07_footer_law_link(page: Page):
    """
    [正常系] フッター「law」リンクへの遷移
    フッターの「law」リンクが正しく機能し、対応するページへ遷移することを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_07...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: フッターナビゲーション内の「law」リンクをクリック
        print("Clicking 'law' footer link...")
        page.get_by_role("link", name=re.compile(r"law", re.IGNORECASE)).click()

        # アサーション: ページが「law」ページへ遷移したことを確認
        print(f"Asserting page URL is {BASE_URL}/law...")
        expect(page).to_have_url(f"{BASE_URL}/law")

    except Error as e:
        save_screenshot_on_failure(page, "test_07_footer_law_link")
        pytest.fail(f"Playwright error during test_07_footer_law_link: {e}")

def test_08_footer_contact_link(page: Page):
    """
    [正常系] フッター「contact」リンクへの遷移
    フッターの「contact」リンクが正しく機能し、対応するページへ遷移することを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_08...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: フッターナビゲーション内の「contact」リンクをクリック
        print("Clicking 'contact' footer link...")
        page.get_by_role("link", name=re.compile(r"contact", re.IGNORECASE)).click()

        # アサーション: ページが「contact」ページへ遷移したことを確認
        print(f"Asserting page URL is {BASE_URL}/contact...")
        expect(page).to_have_url(f"{BASE_URL}/contact")

    except Error as e:
        save_screenshot_on_failure(page, "test_08_footer_contact_link")
        pytest.fail(f"Playwright error during test_08_footer_contact_link: {e}")

def test_09_copyright_text_accuracy(page: Page):
    """
    [異常系/境界値] 著作権表示の正確性
    ページフッターに表示される著作権情報（特に年号）が最新かつ正確であることを確認する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_09...")
        page.goto(CAMERA_PAGE_URL)

        # アサーション: 著作権表示のテキストが「© 2025 Asami K.」と正確に一致することを確認
        # 部分一致および正規表現の制約に従い、まずテキストを含む要素を見つけ、
        # その後、そのテキストが期待する文字列を「含む」ことを検証する。
        # Scenario explicitly asks for "正確に一致する", so we locate by the exact text.
        print("Asserting copyright text is '© 2025 Asami K.'...")
        copyright_locator = page.get_by_text("© 2025 Asami K.", exact=False)
        expect(copyright_locator).to_be_visible() # 要素が存在し、表示されていることを確認
        expect(copyright_locator).to_contain_text("© 2025 Asami K.") # テキスト内容が一致することを確認

    except Error as e:
        save_screenshot_on_failure(page, "test_09_copyright_text_accuracy")
        pytest.fail(f"Playwright error during test_09_copyright_text_accuracy: {e}")

def test_10_image_loading_validation(page: Page):
    """
    [異常系/境界値] メインコンテンツ画像の読み込み検証
    ページ内に表示される主要な画像コンテンツが、全て正しく読み込まれて表示されていることを確認する。
    破損した画像や読み込みに失敗した画像がないことを検証する。
    """
    try:
        print(f"Navigating to {CAMERA_PAGE_URL} for test_10...")
        page.goto(CAMERA_PAGE_URL)

        # ページ内のすべての img 要素を取得
        print("Retrieving all <img> elements...")
        img_locators = page.locator("img").all()

        print(f"Found {len(img_locators)} image elements. Validating loading...")
        for i, img_locator in enumerate(img_locators):
            # 各 img 要素について、naturalWidth と naturalHeight が0より大きいことを評価
            # これは画像が正常にデコードされ、表示可能な状態であることを示します
            # アサーション: 画像が正常にロードされたことを確認
            print(f"  Validating image {i+1}/{len(img_locators)}...")
            assert img_locator.evaluate(
                "img => img.complete && img.naturalWidth > 0 && img.naturalHeight > 0"
            ), f"Image at index {i} failed to load or has invalid dimensions."
        print("All image elements validated successfully.")

    except Error as e:
        save_screenshot_on_failure(page, "test_10_image_loading_validation")
        pytest.fail(f"Playwright error during test_10_image_loading_validation: {e}")
