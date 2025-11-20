import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

# --- Global/Fixture setup for console errors ---
# A list to store console messages (errors and warnings) across tests
console_messages = []

def handle_console_message(msg):
    """
    Playwright console event handler to capture messages.
    Stores error and warning messages in the global console_messages list.
    """
    if msg.type == "error":
        console_messages.append(f"Console Error: {msg.text}")
    elif msg.type == "warning":
        console_messages.append(f"Console Warning: {msg.text}")
    # print(f"CONSOLE [{msg.type}]: {msg.text}") # Uncomment for verbose console logging

@pytest.fixture(scope="module")
def browser_page():
    """
    Provides a Playwright Page instance with console message handling for tests within the module.
    This fixture ensures 'page' is available even without 'pytest-playwright' plugin.
    """
    with sync_playwright() as p:
        # Launch browser in headless mode by default for CI environments.
        # Set headless=False for local debugging with a visible browser.
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Attach the console message handler to the page
        page.on("console", handle_console_message)
        yield page
        browser.close()

@pytest.fixture(scope="module")
def visual_regression_page():
    """
    Provides a separate Playwright Page instance for visual regression tests
    to ensure consistent viewport size and avoid interference from other tests.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Set a standard viewport size for visual comparison
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        yield page
        browser.close()

@pytest.fixture(scope="function", autouse=True)
def setup_teardown_each_test():
    """
    Resets the global console_messages list before each test function
    to ensure isolation of console logs between tests.
    """
    global console_messages
    console_messages = []  # Clear messages before each test
    yield
    # No specific teardown action needed after each test other than clearing messages

# Determine save directory for screenshots.
# Screenshots will be saved in the same directory as this test file.
save_dir = os.path.dirname(os.path.abspath(__file__))

# Base URL for the application
BASE_URL = "https://asami.tokyo"
ART_PAGE_URL = f"{BASE_URL}/art"

# --- Test Cases ---

def test_art_tc_001_page_load_and_basic_display(browser_page: Page):
    """
    ART-TC-001: ページが正しくロードされ、主要なUI要素が表示されることを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        response = browser_page.goto(ART_PAGE_URL)

        # アサーション: HTTPステータスコードが200であること。
        assert response.status == 200, f"Expected 200, got {response.status} for {ART_PAGE_URL}"

        # アサーション: ページのタイトルが「Art | Asami K.」または関連するテキストであること。
        # 部分一致と大文字小文字を区別しない正規表現を使用
        expect(browser_page).to_have_title(re.compile(r"Art \| Asami K\.", re.IGNORECASE))

        # アサーション: メインコンテンツエリアが表示されていることを確認する。
        # ロケータ優先順位: get_by_role
        expect(browser_page.get_by_role("main")).to_be_visible()

        # アサーション: ヘッダーナビゲーションリンク（Top, Art, Camera, Apps）が表示されていることを確認する。
        # ロケータ優先順位: get_by_role (nameは大文字小文字を区別しない設定)
        expect(browser_page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
        expect(browser_page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()
        expect(browser_page.get_by_role("link", name=re.compile(r"Camera", re.IGNORECASE))).to_be_visible()
        expect(browser_page.get_by_role("link", name=re.compile(r"Apps", re.IGNORECASE))).to_be_visible()

        # アサーション: フッターナビゲーションリンク（About, law, contact）が表示されていることを確認する。
        expect(browser_page.get_by_role("link", name=re.compile(r"About", re.IGNORECASE))).to_be_visible()
        expect(browser_page.get_by_role("link", name=re.compile(r"law", re.IGNORECASE))).to_be_visible()
        expect(browser_page.get_by_role("link", name=re.compile(r"contact", re.IGNORECASE))).to_be_visible()

        # アサーション: 著作権表示 (© 2025 Asami K.) が表示されていることを確認する。
        # ロケータ優先順位: get_by_text (部分一致)
        expect(browser_page.get_by_text(re.compile(r"© 2025 Asami K\.", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-001: {e}")

def test_art_tc_002_art_link_is_active(browser_page: Page):
    """
    ART-TC-002: `Art` リンクがアクティブ状態であることを確認する。（境界値）
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # アサーション: 「Art」リンクがアクティブ状態を示す 'aria-current="page"' 属性を持っていることを確認。
        # ロケータ優先順位: get_by_role (nameは大文字小文字を区別しない)
        art_link_locator = browser_page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))
        
        # まずリンク自体が可視であることを確認
        expect(art_link_locator).to_be_visible()
        
        # 'aria-current="page"' 属性が存在し、その値が 'page' であることを期待する。
        # Webサイトによってはactiveクラスや異なるスタイルでアクティブ状態を示すため、
        # 実際のサイトの実装に合わせてこのアサーションを調整してください。
        expect(art_link_locator).to_have_attribute("aria-current", "page", timeout=5000)

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-002: {e}")

def test_art_tc_003_navigation_links_function_correctly(browser_page: Page):
    """
    ART-TC-003: 各ナビゲーションリンクが正しく機能することを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # 定義されたナビゲーションリンクと期待されるURLのペア
        # "Art" リンクは現在のページなので、ここでは遷移テストから除外
        nav_links = {
            "Top": f"{BASE_URL}/",
            "Camera": f"{BASE_URL}/camera",
            "Apps": f"{BASE_URL}/apps",
            "About": f"{BASE_URL}/about",
            "law": f"{BASE_URL}/law",
            "contact": f"{BASE_URL}/contact",
        }

        for link_name, expected_url in nav_links.items():
            # アサーション: ナビゲーションリンクがクリック可能であることを確認。
            # ロケータ優先順位: get_by_role (nameは大文字小文字を区別しない)
            link_locator = browser_page.get_by_role("link", name=re.compile(link_name, re.IGNORECASE))
            expect(link_locator).to_be_enabled()

            # リンクをクリック
            link_locator.click()

            # アサーション: URLが期待するページに遷移したことを確認。末尾のスラッシュは許容。
            # `re.escape()` を使用してURL文字列内の特殊文字をエスケープ
            expect(browser_page).to_have_url(re.compile(f"^{re.escape(expected_url)}/?$", re.IGNORECASE))

            # ブラウザの「戻る」ボタンで元の「Art」ページに戻る
            browser_page.go_back()

            # アサーション: 元の「Art」ページに戻ったことを確認。末尾のスラッシュは許容。
            expect(browser_page).to_have_url(re.compile(f"^{re.escape(ART_PAGE_URL)}/?$", re.IGNORECASE))

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-003 for link '{link_name}': {e}")

def test_art_tc_004_tool_info_displayed_accurately(browser_page: Page):
    """
    ART-TC-004: ツール情報が正確に表示されることを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # アサーション: 「Tools: TouchDesigner, Photoshop, Midjourney, Runway」というテキストが正確に表示されること。
        # ロケータ優先順位: get_by_text (部分一致、正規表現で空白や句読点の揺れを吸収)
        expect(browser_page.get_by_text(re.compile(
            r"Tools:\s*TouchDesigner,\s*Photoshop,\s*Midjourney,\s*Runway", re.IGNORECASE
        ))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-004: {e}")

def test_art_tc_005_smoke_drifting_title_displayed(browser_page: Page):
    """
    ART-TC-005: 作品タイトル「Smoke drifting over big cities」が表示されることを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # アサーション: 「Smoke drifting over big cities」という作品タイトルが表示されていること。
        # ロケータ優先順位: get_by_text (部分一致)
        expect(browser_page.get_by_text(re.compile(r"Smoke drifting over big cities", re.IGNORECASE))).to_be_visible()

        # 関連画像がある場合、その画像が正常にロードされていることを確認する（オプション、ページの構造による）
        # 例: expect(browser_page.locator('article:has-text("Smoke drifting over big cities") img')).to_be_visible()
        # ここでは具体的なセレクタがないため、テキストの表示確認に集中する。

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-005: {e}")

def test_art_tc_006_resort_pool_title_displayed_multiple_times(browser_page: Page):
    """
    ART-TC-006: 作品タイトル「Resort Pool」が複数回表示されることを確認する。（境界値）
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # アサーション: 「Resort Pool」という作品タイトルが3回以上表示されていること。
        # ロケータ優先順位: get_by_text (部分一致)
        resort_pool_locators = browser_page.get_by_text(re.compile(r"Resort Pool", re.IGNORECASE))

        # アサーション: 少なくとも3つの要素が見つかること
        count = resort_pool_locators.count()
        assert count >= 3, f"Expected 'Resort Pool' to appear at least 3 times, but found {count} times."

        # 各要素が可視であることを確認 (オプション)
        for i in range(count):
            expect(resort_pool_locators.nth(i)).to_be_visible()

        # 関連画像がある場合、その画像が正常にロードされていることを確認する（オプション）
        # ここでは具体的なセレクタがないため、テキストの表示確認に集中する。

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-006: {e}")

def test_art_tc_007_copyright_year_is_correct(browser_page: Page):
    """
    ART-TC-007: 著作権表示の年号が正しいことを確認する。（将来の日付の確認）
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # アサーション: 著作権表示が「© 2025 Asami K.」と正確に表示されていること。
        # ロケータ優先順位: get_by_text (部分一致)
        expect(browser_page.get_by_text(re.compile(r"© 2025 Asami K\.", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-007: {e}")

def test_art_tc_008_responsive_design_mobile(browser_page: Page):
    """
    ART-TC-008: モバイルビューポートでのレイアウトと機能を確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # 2. Playwrightでビューポートサイズをモバイルデバイスの一般的な幅（例: 375x667）に設定する。
        browser_page.set_viewport_size({"width": 375, "height": 667})

        # 3. ページ全体のスクリーンショットを取得する。
        # スクリーンショットをテストファイルと同じディレクトリに保存
        screenshot_path = os.path.join(save_dir, "ART-TC-008_mobile_screenshot.png")
        browser_page.screenshot(path=screenshot_path, full_page=True)
        print(f"Mobile screenshot saved to: {screenshot_path}")

        # アサーション: ヘッダーナビゲーションがハンバーガーメニューに変化している場合、
        # それが表示され、クリックするとメニューが開閉することを確認する。
        # ロケータ優先順位: get_by_role("button") で name が "menu" や "navigation" のものを探す
        hamburger_menu_locator = browser_page.get_by_role("button", name=re.compile(r"menu|navigation", re.IGNORECASE)).first
        
        # モバイルビューポートでハンバーガーメニューが表示されていることを確認
        expect(hamburger_menu_locator).to_be_visible()

        # メニューをクリックして開く
        hamburger_menu_locator.click()
        # アサーション: メニューが開いたことを示す要素（例: トップリンク）が可視になることを確認
        # これはサイトの具体的な実装に依存するため、適切なロケータを選んでください。
        expect(browser_page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()

        # メニューを再度クリックして閉じる
        hamburger_menu_locator.click()
        # アサーション: メニューが閉じたことを確認（例: トップリンクが不可視になる）
        expect(browser_page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).not_to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-008: {e}")

def test_art_tc_009_responsive_design_tablet(browser_page: Page):
    """
    ART-TC-009: タブレットビューポートでのレイアウトと機能を確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # 2. Playwrightでビューポートサイズをタブレットデバイスの一般的な幅（例: 768x1024）に設定する。
        browser_page.set_viewport_size({"width": 768, "height": 1024})

        # 3. ページ全体のスクリーンショットを取得する。
        # スクリーンショットをテストファイルと同じディレクトリに保存
        screenshot_path = os.path.join(save_dir, "ART-TC-009_tablet_screenshot.png")
        browser_page.screenshot(path=screenshot_path, full_page=True)
        print(f"Tablet screenshot saved to: {screenshot_path}")

        # アサーション: コンテンツがタブレット向けに適切に再配置されていることを確認する。
        expect(browser_page.get_by_role("main")).to_be_visible()
        
        # アサーション: ナビゲーションがデスクトップとモバイルのどちらの形式になっているか確認し、
        # その形式が適切に機能することを確認する。
        # タブレットのブレークポイントによってはハンバーガーメニューが表示される場合と、
        # 通常のナビゲーションが表示される場合がある。
        hamburger_menu_locator = browser_page.get_by_role("button", name=re.compile(r"menu|navigation", re.IGNORECASE)).first
        if hamburger_menu_locator.is_visible():
            # タブレットでもハンバーガーメニューの場合
            expect(hamburger_menu_locator).to_be_visible()
            # メニューが開閉することを確認（詳細はART-TC-008を参照）
        else:
            # 通常のナビゲーションリンクが表示されている場合
            expect(browser_page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
            expect(browser_page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-009: {e}")

def test_art_tc_010_responsive_design_desktop(browser_page: Page):
    """
    ART-TC-010: デスクトップビューポートでのレイアウトと機能を確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        browser_page.goto(ART_PAGE_URL)

        # 2. Playwrightでビューポートサイズをデスクトップデバイスの一般的な幅（例: 1920x1080）に設定する。
        browser_page.set_viewport_size({"width": 1920, "height": 1080})

        # 3. ページ全体のスクリーンショットを取得する。
        # スクリーンショットをテストファイルと同じディレクトリに保存
        screenshot_path = os.path.join(save_dir, "ART-TC-010_desktop_screenshot.png")
        browser_page.screenshot(path=screenshot_path, full_page=True)
        print(f"Desktop screenshot saved to: {screenshot_path}")

        # アサーション: コンテンツがデスクトップ向けに適切に配置されていることを確認する。
        expect(browser_page.get_by_role("main")).to_be_visible()
        
        # アサーション: ハンバーガーメニューは表示されないことを期待
        hamburger_menu_locator = browser_page.get_by_role("button", name=re.compile(r"menu|navigation", re.IGNORECASE)).first
        expect(hamburger_menu_locator).not_to_be_visible()
        
        # アサーション: 通常のナビゲーションリンクが表示されていることを確認
        expect(browser_page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
        expect(browser_page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-010: {e}")

def test_art_tc_011_visual_regression_snapshot(visual_regression_page: Page):
    """
    ART-TC-011: スナップショットベースのUIリグレッションを検出する。（正常系・異常系）
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        visual_regression_page.goto(ART_PAGE_URL)

        # 2. ページ全体のスクリーンショットを取得し、事前に承認されたベースラインスクリーンショットと比較する。
        # expect(page).to_have_screenshot() は、Playwrightのビジュアルリグレッションテスト機能です。
        # 初回実行時: 指定された名前で参照画像が '__snapshots__' ディレクトリに保存されます。
        # 2回目以降: 新しく取得したスクリーンショットと参照画像を比較します。
        # 差分が `threshold` を超える場合、テストは失敗し、差分画像が生成されます。
        expect(visual_regression_page).to_have_screenshot(
            name="ART-TC-011_full_page_art.png",
            full_page=True,
            threshold=0.2  # 0.2% のピクセル差分を許容
        )
        print(f"Visual regression snapshot for ART-TC-011 completed. Check 'ART-TC-011_full_page_art.png' in {save_dir}/__snapshots__ directory.")

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-011 (Visual Regression): {e}")

def test_art_tc_012_no_console_errors(browser_page: Page):
    """
    ART-TC-012: ページロード中にコンソールエラーが発生しないことを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        # `browser_page` フィクスチャは既に console handler をアタッチしています。
        browser_page.goto(ART_PAGE_URL)

        # 2. ページのコンソールログは `handle_console_message` 関数によって監視され、
        #    エラーや警告は `console_messages` リストに格納されます。
        # 3. ページが完全にロードされるのを待ちます (goto が完了するのを待つ)。

        # アサーション: `console_messages` リストが空であることを確認。
        # つまり、ページロード中にコンソールエラーや警告が発生しなかったこと。
        assert not console_messages, \
            f"Expected no console errors or warnings, but found: \n" + \
            "\n".join(console_messages)

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-012: {e}")

def test_art_tc_013_404_page_for_invalid_url(browser_page: Page):
    """
    ART-TC-013: 無効なURLにアクセスした際に、404ページが表示されることを確認する。
    """
    # 毎回異なるランダムなURLを生成し、キャッシュや過去のリダイレクトの影響を避ける
    invalid_url = f"{BASE_URL}/non-existent-page-{os.urandom(4).hex()}" 
    try:
        # 1. 存在しないURLに直接アクセスする。
        # `wait_until="domcontentloaded"` は、DOMが構築された時点で処理を続けるため、
        # 404ページのようなシンプルなエラーページのチェックに適しています。
        response = browser_page.goto(invalid_url, wait_until="domcontentloaded")

        # アサーション: HTTPステータスコードが404であること。
        assert response.status == 404, \
            f"Expected 404 status for {invalid_url}, but got {response.status}"

        # アサーション: ページに「404 Not Found」や「ページが見つかりません」といったエラーメッセージが表示されていることを確認する。
        # ロケータ優先順位: get_by_text (部分一致、正規表現で複数の表現を許容)
        expect(browser_page.get_by_text(re.compile(r"404|not found|ページが見つかりません", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in ART-TC-013: {e}")
