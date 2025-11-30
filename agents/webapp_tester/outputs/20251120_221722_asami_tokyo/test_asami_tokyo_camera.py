import os
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error, TimeoutError
import re

# ベースURLを定義
BASE_URL = "https://asami.tokyo/camera"

@pytest.fixture(scope="module")
def page():
    """
    pytest-playwrightがインストールされていない環境でも動作するように、
    Playwrightブラウザインスタンスとページをセットアップするフィクスチャ。
    """
    with sync_playwright() as p:
        # headless=True はデフォルトだが、明示的に指定可能
        browser = p.chromium.launch(headless=True)
        # ビューポートサイズを設定する例 (必要に応じてコメント解除)
        # page = browser.new_page(viewport={'width': 1280, 'height': 720})
        page = browser.new_page()
        yield page
        browser.close()

def save_screenshot_on_failure(page: Page, test_name: str):
    """
    テストが失敗した場合にスクリーンショットを保存するヘルパー関数。
    """
    save_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_path = os.path.join(save_dir, f"fail_screenshot_{test_name}.png")
    try:
        page.screenshot(path=screenshot_path)
        print(f"\nスクリーンショットを保存しました: {screenshot_path}")
    except Exception as e:
        print(f"\nスクリーンショットの保存中にエラーが発生しました: {e}")

# -----------------------------------------------------------------------------
# 3.1. ページロードと基本表示テスト
# -----------------------------------------------------------------------------

def test_tc_001_page_load_and_title(page: Page):
    """TC-001: ページの正常ロードとタイトル表示"""
    test_name = "tc_001_page_load_and_title"
    try:
        print(f"\n--- Running {test_name} ---")
        # 1. https://asami.tokyo/camera にアクセスする。
        print(f"Navigating to {BASE_URL}...")
        response = page.goto(BASE_URL)

        # 1. ページがHTTP 200 OKでロードされる。
        assert response.status == 200, f"Expected HTTP 200, got {response.status}"
        print(f"Page loaded successfully with status {response.status}.")

        # 2. ブラウザのタイトルが「Camera - asami.tokyo」または類似の適切なタイトルである。
        # 部分一致で大文字小文字を区別しない正規表現を使用
        expect(page).to_have_title(re.compile(r"Camera - asami\.tokyo", re.IGNORECASE))
        print(f"Page title is as expected: '{page.title()}'.")

        # 3. ページの主要コンテンツ（ヘッダー、ナビゲーション、コンテンツ領域、フッター）が表示される。
        # ナビゲーションが表示されていることを確認
        # get_by_role(name=...)はアクセシブル名をチェック。汎用的な名称で試みる。
        expect(page.get_by_role("navigation")).to_be_visible()
        print("Navigation bar is visible.")

        # フッターが表示されていることを確認 (contentinfoロールを想定)
        expect(page.get_by_role("contentinfo")).to_be_visible()
        print("Footer is visible.")

        # ページが期待するURLにあることを確認
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Current URL is as expected: {page.url}.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_002_main_content_display(page: Page):
    """TC-002: 主要なページコンテンツの表示確認"""
    test_name = "tc_002_main_content_display"
    try:
        print(f"\n--- Running {test_name} ---")
        # 1. https://asami.tokyo/camera にアクセスする。
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 1. ページタイトル「Camera」が表示される。
        # headingロールで、名前が「Camera」を含む要素を探す (大文字小文字を区別しない)
        expect(page.get_by_role("heading", name=re.compile(r"Camera", re.IGNORECASE))).to_be_visible()
        print("Main heading 'Camera' is visible.")

        # 2. グローバルナビゲーション（Top, Art, Camera, Apps）が表示される。
        expect(page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile(r"Camera", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile(r"Apps", re.IGNORECASE))).to_be_visible()
        print("Global navigation links are visible.")

        # 3. 「Tools」セクションのヘッダーと各ツール名が表示される。
        # "Tools:"というテキストを含む要素が表示されていることを確認
        expect(page.get_by_text("Tools:")).to_be_visible()
        print("'Tools:' section header is visible.")
        expect(page.get_by_text(re.compile(r"DJI Osmo Pocket 3", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"DJI Action 2", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"Google Pixel 8 Pro", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"Davinci Resolve", re.IGNORECASE))).to_be_visible()
        print("All tool names in 'Tools' section are visible.")

        # 4. ギャラリーアイテム（例: Water's Edge, stream）が表示される。
        # "Water's Edge"というテキストを含む要素が表示されていることを確認 (最初の1つで十分)
        expect(page.get_by_text(re.compile(r"Water's Edge", re.IGNORECASE)).first).to_be_visible()
        expect(page.get_by_text(re.compile(r"stream", re.IGNORECASE))).to_be_visible()
        print("Gallery items 'Water's Edge' and 'stream' are visible.")

        # 5. フッター（© 2025 Asami K., About / law / contact）が表示される。
        # 著作権表示のテキストが含まれていることを確認
        expect(page.get_by_text(re.compile(r"© 2025 Asami K\.", re.IGNORECASE))).to_be_visible()
        print("Footer copyright information is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

# -----------------------------------------------------------------------------
# 3.2. グローバルナビゲーションテスト
# -----------------------------------------------------------------------------

def test_tc_003_top_link_navigation(page: Page):
    """TC-003: 「Top」リンクの正常動作確認"""
    test_name = "tc_003_top_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        # 1. https://asami.tokyo/camera にアクセスする。
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 2. 「Top」リンクをクリックする。
        # nameを正規表現で指定し、大文字小文字を区別しない
        print("Clicking 'Top' link...")
        page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE)).click()

        # 1. トップページ (https://asami.tokyo/ または /) へ遷移する。
        # URLがベースドメインであること、パスが空またはスラッシュであることを確認
        expect(page).to_have_url(re.compile(r"https:\/\/asami\.tokyo\/?$", re.IGNORECASE))
        print(f"Navigated to Top page: {page.url}.")

        # 2. トップページの主要コンテンツが正しく表示される。（トップページのヘッディングを想定）
        expect(page.get_by_role("heading").first).to_be_visible()
        print("Top page main heading is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_004_art_link_navigation(page: Page):
    """TC-004: 「Art」リンクの正常動作確認"""
    test_name = "tc_004_art_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        # 1. https://asami.tokyo/camera にアクセスする。
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 2. 「Art」リンクをクリックする。
        print("Clicking 'Art' link...")
        page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE)).click()

        # 1. 「Art」ページ (https://asami.tokyo/art または類似) へ遷移する。
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/art", re.IGNORECASE))
        print(f"Navigated to Art page: {page.url}.")

        # 2. 「Art」ページの主要コンテンツが正しく表示される。（「Art」という見出しを想定）
        expect(page.get_by_role("heading", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()
        print("Art page main heading 'Art' is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_005_apps_link_navigation(page: Page):
    """TC-005: 「Apps」リンクの正常動作確認"""
    test_name = "tc_005_apps_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        # 1. https://asami.tokyo/camera にアクセスする。
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 2. 「Apps」リンクをクリックする。
        print("Clicking 'Apps' link...")
        page.get_by_role("link", name=re.compile(r"Apps", re.IGNORECASE)).click()

        # 1. 「Apps」ページ (https://asami.tokyo/apps または類似) へ遷移する。
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/apps", re.IGNORECASE))
        print(f"Navigated to Apps page: {page.url}.")

        # 2. 「Apps」ページの主要コンテンツが正しく表示される。（「Apps」という見出しを想定）
        expect(page.get_by_role("heading", name=re.compile(r"Apps", re.IGNORECASE))).to_be_visible()
        print("Apps page main heading 'Apps' is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_006_camera_link_current_page(page: Page):
    """TC-006: 「Camera」リンク（現在ページ）の挙動確認 (境界値)"""
    test_name = "tc_006_camera_link_current_page"
    try:
        print(f"\n--- Running {test_name} ---")
        # 1. https://asami.tokyo/camera にアクセスする。
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 2. 現在のページを示す「Camera」リンクをクリックする。
        # exact=Trueは禁止されているため、nameを正規表現で指定
        print("Clicking 'Camera' link on the current page...")
        page.get_by_role("link", name=re.compile(r"Camera", re.IGNORECASE)).click()

        # 1. ページが再読み込みされるか、または何も起こらない。
        # 2. URLは https://asami.tokyo/camera のままである。
        # URLが変わらないことを確認
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"URL remained unchanged: {page.url}.")

        # 3. ページコンテンツに変更がない。（メインの見出しが引き続き表示されることを確認）
        expect(page.get_by_role("heading", name=re.compile(r"Camera", re.IGNORECASE))).to_be_visible()
        print("Main heading 'Camera' is still visible after clicking current page link.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

# -----------------------------------------------------------------------------
# 3.3. Toolsセクションテスト
# -----------------------------------------------------------------------------

def test_tc_007_tool_names_display(page: Page):
    """TC-007: 各ツール名の表示確認"""
    test_name = "tc_007_tool_names_display"
    try:
        print(f"\n--- Running {test_name} ---")
        # 1. https://asami.tokyo/camera にアクセスする。
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 2. 「Tools」セクションにあるすべてのツール名が表示されていることを確認する。
        print("Checking visibility of all tool names...")
        expect(page.get_by_text(re.compile(r"DJI Osmo Pocket 3", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"DJI Action 2", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"Google Pixel 8 Pro", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"Davinci Resolve", re.IGNORECASE))).to_be_visible()
        print("All specified tool names are visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_008_dji_osmo_link_navigation(page: Page):
    """TC-008: 「DJI Osmo Pocket 3」リンクの正常動作確認"""
    test_name = "tc_008_dji_osmo_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 「DJI Osmo Pocket 3」リンクをクリックし、新しいタブが開くのを待つ
        print("Clicking 'DJI Osmo Pocket 3' link and waiting for new page...")
        with page.expect_popup() as popup_info:
            page.get_by_role("link", name=re.compile(r"DJI Osmo Pocket 3", re.IGNORECASE)).click()
        new_page = popup_info.value

        # 新しいページのURLがDJI Osmo Pocket 3に関連するものであることを確認
        expect(new_page).to_have_url(re.compile(r"dji\.com.*pocket-3", re.IGNORECASE))
        print(f"New page opened with URL: {new_page.url}. (Matches DJI Osmo Pocket 3)")

        # 新しいページを閉じる（オプション）
        new_page.close()

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_009_dji_action_link_navigation(page: Page):
    """TC-009: 「DJI Action 2」リンクの正常動作確認"""
    test_name = "tc_009_dji_action_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 「DJI Action 2」リンクをクリックし、新しいタブが開くのを待つ
        print("Clicking 'DJI Action 2' link and waiting for new page...")
        with page.expect_popup() as popup_info:
            page.get_by_role("link", name=re.compile(r"DJI Action 2", re.IGNORECASE)).click()
        new_page = popup_info.value

        # 新しいページのURLがDJI Action 2に関連するものであることを確認
        expect(new_page).to_have_url(re.compile(r"dji\.com.*action-2", re.IGNORECASE))
        print(f"New page opened with URL: {new_page.url}. (Matches DJI Action 2)")
        new_page.close()

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_010_google_pixel_link_navigation(page: Page):
    """TC-010: 「Google Pixel 8 Pro」リンクの正常動作確認"""
    test_name = "tc_010_google_pixel_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 「Google Pixel 8 Pro」リンクをクリックし、新しいタブが開くのを待つ
        print("Clicking 'Google Pixel 8 Pro' link and waiting for new page...")
        with page.expect_popup() as popup_info:
            page.get_by_role("link", name=re.compile(r"Google Pixel 8 Pro", re.IGNORECASE)).click()
        new_page = popup_info.value

        # 新しいページのURLがGoogle Pixel 8 Proに関連するものであることを確認
        expect(new_page).to_have_url(re.compile(r"store\.google\.com.*pixel-8-pro", re.IGNORECASE))
        print(f"New page opened with URL: {new_page.url}. (Matches Google Pixel 8 Pro)")
        new_page.close()

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_011_davinci_resolve_link_navigation(page: Page):
    """TC-011: 「Davinci Resolve」リンクの正常動作確認"""
    test_name = "tc_011_davinci_resolve_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 「Davinci Resolve」リンクをクリックし、新しいタブが開くのを待つ
        print("Clicking 'Davinci Resolve' link and waiting for new page...")
        with page.expect_popup() as popup_info:
            page.get_by_role("link", name=re.compile(r"Davinci Resolve", re.IGNORECASE)).click()
        new_page = popup_info.value

        # 新しいページのURLがDavinci Resolveに関連するものであることを確認
        expect(new_page).to_have_url(re.compile(r"blackmagicdesign\.com.*davinci-resolve", re.IGNORECASE))
        print(f"New page opened with URL: {new_page.url}. (Matches Davinci Resolve)")
        new_page.close()

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

# -----------------------------------------------------------------------------
# 3.4. ギャラリー/作品表示テスト
# -----------------------------------------------------------------------------

def test_tc_012_all_gallery_items_display(page: Page):
    """TC-012: 全てのギャラリーアイテムの表示確認"""
    test_name = "tc_012_all_gallery_items_display"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 全ての作品タイトルが表示されていることを確認
        print("Checking visibility of all gallery item titles...")
        expect(page.get_by_text(re.compile(r"Water's Edge", re.IGNORECASE))).to_have_count(11)
        expect(page.get_by_text(re.compile(r"stream", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"walk in sunset", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"sunset coast", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"Port Tower", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"Palm Tree", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"ship enters the port", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"Sunset with bird", re.IGNORECASE))).to_be_visible()
        print("All specified gallery item titles are visible and 'Water's Edge' count is correct.")

        # 各タイトルには対応するサムネイル画像が紐づいており、正しくロードされ表示されていることを確認
        # imgロールで、名前が「Water's Edge」を含む最初の画像を確認 (汎用的なチェック)
        expect(page.get_by_role("img", name=re.compile(r"Water's Edge", re.IGNORECASE)).first).to_be_visible()
        print("First 'Water's Edge' thumbnail image is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_013_gallery_item_click_action(page: Page):
    """TC-013: 各ギャラリーアイテムのクリック動作確認 (正常系)"""
    test_name = "tc_013_gallery_item_click_action"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # 最初の「Water's Edge」アイテムをクリック
        print("Clicking first 'Water's Edge' item...")
        page.get_by_text(re.compile(r"Water's Edge", re.IGNORECASE)).first.click()

        # 画像拡大表示モーダルまたは詳細ページが表示されることを確認
        # モーダルコンテンツの表示を確認 (CSSセレクタは現状の情報に基づき)
        expect(page.locator(".modal-content")).to_be_visible()
        print("Modal content is visible after clicking 'Water's Edge'.")

        # 表示されたコンテンツが「Water's Edge」に関連するものであることを確認 (モーダル内のタイトルを想定)
        expect(page.locator(".modal-content").filter(has_text=re.compile(r"Water's Edge", re.IGNORECASE))).to_be_visible()
        print("Modal content relates to 'Water's Edge'.")

        # モーダルを閉じる (Escapeキーを想定)
        print("Closing modal with Escape key...")
        page.keyboard.press("Escape")
        expect(page.locator(".modal-content")).not_to_be_visible()
        print("Modal is closed.")

        # 「stream」アイテムをクリック
        print("Clicking 'stream' item...")
        page.get_by_text(re.compile(r"stream", re.IGNORECASE)).click()

        # 同様にモーダルが表示され、コンテンツが「stream」に関連することを確認
        expect(page.locator(".modal-content")).to_be_visible()
        print("Modal content is visible after clicking 'stream'.")
        expect(page.locator(".modal-content").filter(has_text=re.compile(r"stream", re.IGNORECASE))).to_be_visible()
        print("Modal content relates to 'stream'.")

        # モーダルを閉じる
        print("Closing modal with Escape key...")
        page.keyboard.press("Escape")
        expect(page.locator(".modal-content")).not_to_be_visible()
        print("Modal is closed.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_014_water_s_edge_unique_content(page: Page):
    """TC-014: 各「Water's Edge」アイテムのユニーク性確認 (境界値)"""
    test_name = "tc_014_water_s_edge_unique_content"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        water_edges_locators = page.get_by_text(re.compile(r"Water's Edge", re.IGNORECASE))
        count = water_edges_locators.count()
        print(f"Found {count} 'Water's Edge' items.")

        modal_image_srcs = []

        # 各「Water's Edge」アイテムをクリックし、表示内容を確認
        for i in range(count):
            print(f"Clicking 'Water's Edge' item {i+1}/{count}...")
            water_edges_locators.nth(i).click()

            # モーダルが表示されることを確認
            expect(page.locator(".modal-content")).to_be_visible()
            print("Modal content is visible.")

            # モーダル内の画像ソースURLを取得
            # タイムアウトを短めに設定して、画像が読み込まれるのを待つ
            img_locator = page.locator(".modal-content img")
            expect(img_locator).to_be_visible(timeout=5000)
            modal_image_src = img_locator.get_attribute("src")
            assert modal_image_src is not None, f"Image source not found for 'Water's Edge' item {i+1}"
            modal_image_srcs.append(modal_image_src)
            print(f"Modal image src: {modal_image_src}")

            # モーダルを閉じる
            page.keyboard.press("Escape")
            expect(page.locator(".modal-content")).not_to_be_visible()
            print("Modal is closed.")

        # 全ての画像ソースURLがユニークであることを確認
        assert len(set(modal_image_srcs)) == count, \
            f"Expected {count} unique 'Water's Edge' items, but found {len(set(modal_image_srcs))} unique images."
        print(f"All {count} 'Water's Edge' items show unique content (image src).")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

# -----------------------------------------------------------------------------
# 3.5. フッターテスト
# -----------------------------------------------------------------------------

def test_tc_015_copyright_display(page: Page):
    """TC-015: 著作権表示の確認"""
    test_name = "tc_015_copyright_display"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # フッターに「© 2025 Asami K.」という著作権表示があることを確認
        expect(page.get_by_text(re.compile(r"© 2025 Asami K\.", re.IGNORECASE))).to_be_visible()
        print("Copyright notice '© 2025 Asami K.' is visible in the footer.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_016_about_link_navigation(page: Page):
    """TC-016: 「About」リンクの正常動作確認"""
    test_name = "tc_016_about_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # フッターの「About」リンクをクリックする
        # contentinfoロールの内部にあるlinkロールを絞り込む
        print("Clicking 'About' link in footer...")
        page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"About", re.IGNORECASE)).click()

        # 「About」ページへ遷移する。
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/about", re.IGNORECASE))
        print(f"Navigated to About page: {page.url}.")

        # 「About」ページの主要コンテンツが正しく表示される。（見出し「About」を想定）
        expect(page.get_by_role("heading", name=re.compile(r"About", re.IGNORECASE))).to_be_visible()
        print("About page main heading 'About' is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_017_contact_link_navigation(page: Page):
    """TC-017: 「contact」リンクの正常動作確認"""
    test_name = "tc_017_contact_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # フッターの「contact」リンクをクリックする
        print("Clicking 'contact' link in footer...")
        page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"contact", re.IGNORECASE)).click()

        # 「contact」ページへ遷移する。
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/contact", re.IGNORECASE))
        print(f"Navigated to Contact page: {page.url}.")

        # 「contact」ページの主要コンテンツが表示される。（見出し「Contact」を想定）
        expect(page.get_by_role("heading", name=re.compile(r"Contact", re.IGNORECASE))).to_be_visible()
        print("Contact page main heading 'Contact' is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")

def test_tc_018_law_link_navigation(page: Page):
    """TC-018: 「law」リンクの正常動作確認"""
    test_name = "tc_018_law_link_navigation"
    try:
        print(f"\n--- Running {test_name} ---")
        page.goto(BASE_URL)
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/camera", re.IGNORECASE))
        print(f"Navigated to {BASE_URL}.")

        # フッターの「law」リンクをクリックする
        print("Clicking 'law' link in footer...")
        page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"law", re.IGNORECASE)).click()

        # 「law」ページへ遷移する。
        expect(page).to_have_url(re.compile(r"asami\.tokyo\/law", re.IGNORECASE))
        print(f"Navigated to Law page: {page.url}.")

        # 「law」ページの主要コンテンツが表示される。（見出し「Law」を想定）
        expect(page.get_by_role("heading", name=re.compile(r"Law", re.IGNORECASE))).to_be_visible()
        print("Law page main heading 'Law' is visible.")

    except (Error, TimeoutError, AssertionError) as e:
        save_screenshot_on_failure(page, test_name)
        pytest.fail(f"{test_name} failed: {e}")