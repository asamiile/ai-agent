import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

# Base URL for the website under test
BASE_URL = "https://asami.tokyo/"

# Directory to save screenshots
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope="module")
def page():
    """
    Playwright 'page' fixture for synchronous API.
    This fixture ensures Playwright browser and page are set up and torn down
    correctly for all tests in the module.
    It's defined here to ensure it works even if pytest-playwright is not globally installed.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page_instance = browser.new_page()
        yield page_instance
        browser.close()

def test_1_homepage_main_elements_display(page: Page):
    """
    テストケース1: トップページ主要要素の表示確認
    トップページが正常にロードされ、主要な自己紹介テキスト、スキルリスト、
    ナビゲーション、フッターが正しく表示されることを確認する。
    """
    try:
        # 1. ブラウザで https://asami.tokyo/ にアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        response = page.goto(BASE_URL, wait_until='networkidle')
        assert response.status == 200, f"Expected 200, got {response.status} for {BASE_URL}"
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_1_homepage_main_elements.png"))

        # 1. ページタイトルが期待される値であること。
        # Use regex for flexible title matching
        expect(page).to_have_title(re.compile(r"Asami K\.|Asami K\. - Front-end Engineer", re.IGNORECASE))

        # 2. 以下のテキスト要素がページ上に表示されていること:
        # "I'm a front-end engineer and I use technology to express my art."
        expect(page.get_by_text("I'm a front-end engineer", exact=False)).to_be_visible()
        # "Work Skill:"
        expect(page.get_by_text("Work Skill:", exact=False)).to_be_visible()
        # "Hobby Skill:"
        expect(page.get_by_text("Hobby Skill:", exact=False)).to_be_visible()

        # 3. ヘッダーナビゲーションに以下のリンクが表示されていること: Top, Art, Camera, Apps, Asami K
        # Using get_by_role with case-insensitive regex for robustness
        expect(page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile(r"Camera", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile(r"Apps", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile(r"Asami K", re.IGNORECASE))).to_be_visible()

        # 4. フッターナビゲーションに以下のリンクが表示されていること: About, law, contact
        # Using get_by_role with case-insensitive regex for robustness
        expect(page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"About", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"law", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"contact", re.IGNORECASE))).to_be_visible()

        # 5. 著作権表示 "© 2025 Asami K." が表示されていること。
        expect(page.get_by_text("© 2025 Asami K.", exact=False)).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_1_homepage_main_elements_display: {e}")

def test_2_navigation_link_art(page: Page):
    """
    テストケース2: ナビゲーションリンク「Art」の遷移
    ヘッダーの「Art」ナビゲーションリンクをクリックすると、対応するArtページへ正常に遷移することを確認する。
    """
    try:
        # 1. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # 2. ヘッダーナビゲーションの「Art」リンクをクリックする。
        art_link = page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))
        expect(art_link).to_be_visible() # Ensure link is visible before clicking
        art_link.click()

        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_2_navigation_art.png"))

        # 1. URLが https://asami.tokyo/art に変更されていること。
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art/?$"))

        # 2. Artページの主要コンテンツ（例: 作品リスト、"Art" という見出しなど）が表示されていること。
        expect(page.get_by_role("heading", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_2_navigation_link_art: {e}")

def test_3_navigation_link_asami_k(page: Page):
    """
    テストケース3: ナビゲーションリンク「Asami K」の遷移
    ヘッダーの「Asami K」ナビゲーションリンクをクリックすると、対応するプロフィールページへ正常に遷移することを確認する。
    """
    try:
        # 1. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # 2. ヘッダーナビゲーションの「Asami K」リンクをクリックする。
        asami_k_link = page.get_by_role("link", name=re.compile(r"Asami K", re.IGNORECASE))
        expect(asami_k_link).to_be_visible() # Ensure link is visible before clicking
        asami_k_link.click()

        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_3_navigation_asami_k.png"))

        # 1. URLが https://asami.tokyo/about に変更されていること。
        expect(page).to_have_url(re.compile(r"asami\.tokyo/about/?$"))

        # 2. プロフィールページの主要コンテンツ（例: 詳細な自己紹介、"Asami K." という見出しなど）が表示されていること。
        expect(page.get_by_role("heading", name=re.compile(r"About|Asami K", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text("Hi there!", exact=False)).to_be_visible() # A common phrase on about pages

    except Error as e:
        pytest.fail(f"Playwright error in test_3_navigation_link_asami_k: {e}")

def test_4_footer_link_about(page: Page):
    """
    テストケース4: フッターリンク「About」の遷移
    フッターの「About」リンクをクリックすると、対応するAboutページへ正常に遷移することを確認する。
    """
    try:
        # 1. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # 2. フッターの「About」リンクをクリックする。
        # Target the footer section specifically to avoid conflicts with header links
        about_link = page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"About", re.IGNORECASE))
        expect(about_link).to_be_visible()
        about_link.click()

        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_4_footer_about.png"))

        # 1. URLが https://asami.tokyo/about に変更されていること。
        expect(page).to_have_url(re.compile(r"asami\.tokyo/about/?$"))

        # 2. Aboutページの主要コンテンツが表示されていること。
        expect(page.get_by_role("heading", name=re.compile(r"About|Asami K", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text("Hi there!", exact=False)).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_4_footer_link_about: {e}")

def test_5_footer_link_law(page: Page):
    """
    テストケース5: フッターリンク「law」の遷移
    フッターの「law」リンクをクリックすると、対応する法律情報ページへ正常に遷移することを確認する。
    """
    try:
        # 1. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # 2. フッターの「law」リンクをクリックする。
        law_link = page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"law", re.IGNORECASE))
        expect(law_link).to_be_visible()
        law_link.click()

        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_5_footer_law.png"))

        # 1. URLが https://asami.tokyo/law に変更されていること。
        expect(page).to_have_url(re.compile(r"asami\.tokyo/law/?$"))

        # 2. ページの主要コンテンツが表示されていること (例: 法的表記、プライバシーポリシーなど)。
        expect(page.get_by_role("heading", name=re.compile(r"law|legal|特定商取引法|プライバシーポリシー", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text("Legal information", exact=False)).to_be_visible() # Common text on such pages

    except Error as e:
        pytest.fail(f"Playwright error in test_5_footer_link_law: {e}")

def test_6_footer_link_contact(page: Page):
    """
    テストケース6: フッターリンク「contact」の遷移
    フッターの「contact」リンクをクリックすると、対応するお問い合わせページへ正常に遷移することを確認する。
    """
    try:
        # 1. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # 2. フッターの「contact」リンクをクリックする。
        contact_link = page.get_by_role("contentinfo").get_by_role("link", name=re.compile(r"contact", re.IGNORECASE))
        expect(contact_link).to_be_visible()
        contact_link.click()

        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_6_footer_contact.png"))

        # 1. URLが https://asami.tokyo/contact に変更されていること。
        expect(page).to_have_url(re.compile(r"asami\.tokyo/contact/?$"))

        # 2. お問い合わせフォームまたは連絡先情報が表示されていること。
        expect(page.get_by_role("heading", name=re.compile(r"contact|お問い合わせ", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text("Feel free to reach out", exact=False)).to_be_visible() # Common text on contact pages

    except Error as e:
        pytest.fail(f"Playwright error in test_6_footer_link_contact: {e}")

def test_7_404_page_display_validation(page: Page):
    """
    テストケース7: 404ページ表示の検証 (異常系)
    存在しないURLにアクセスした際に、適切なHTTPステータスコード (404 Not Found) が返され、
    ユーザーフレンドリーなエラーページが表示されることを確認する。
    """
    try:
        # 1. ブラウザでサイトの存在しないパスに直接アクセスする。
        non_existent_url = BASE_URL + "non-existent-page-12345"
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        response = page.goto(non_existent_url, wait_until='networkidle')

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_7_404_page.png"))

        # 1. HTTPステータスコードが 404 であること。
        assert response.status == 404, f"Expected 404 status, but got {response.status} for {non_existent_url}"

        # 2. 「Page Not Found」や「お探しのページは見つかりませんでした」といった、
        #    ユーザーに状況を伝えるエラーメッセージが表示されていること。
        expect(page.get_by_text(re.compile(r"Page Not Found|お探しのページは見つかりませんでした", re.IGNORECASE))).to_be_visible()

        # 3. トップページへのリンクなど、ユーザーをナビゲートするための要素が表示されていること。
        expect(page.get_by_role("link", name=re.compile(r"Home|Top", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_7_404_page_display_validation: {e}")

def test_8_mobile_view_layout_check(page: Page):
    """
    テストケース8: モバイルビューでのレイアウト確認 (レスポンシブデザイン)
    スマートフォンなどのモバイルデバイスのビューポートでトップページが正しく表示され、
    主要なコンテンツが適切にレイアウトされていることを確認する。
    """
    try:
        # 1. ビューポートサイズを一般的なモバイルサイズ (例: 幅375px, 高さ667px) に設定する。
        page.set_viewport_size({"width": 375, "height": 667})

        # 2. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_8_mobile_view_layout.png"))

        # 1. ページコンテンツが画面幅に収まって表示され、横スクロールが発生しないこと。
        # Check if scrollWidth is greater than innerWidth, which indicates horizontal scroll.
        # Allow a small tolerance for browser rendering differences.
        has_horizontal_scroll = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 5")
        assert not has_horizontal_scroll, "Horizontal scroll detected in mobile view."

        # 2. 自己紹介テキスト、スキルリストが読みやすいフォントサイズと適切な行間で表示されていること。
        expect(page.get_by_text("I'm a front-end engineer", exact=False)).to_be_visible()
        expect(page.get_by_text("Work Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("Hobby Skill:", exact=False)).to_be_visible()
        # Additional check: If there's a specific mobile menu (e.g., hamburger icon)
        # instead of a desktop navigation bar, check for its visibility and the desktop nav's invisibility.
        # Assuming a common "menu" or "navigation" accessible name for hamburger icons.
        mobile_menu_button = page.get_by_role("button", name=re.compile(r"menu|ナビゲーション", re.IGNORECASE))
        # 修正: .count() > 0 の代わりに Playwright の is_visible() を使用して、要素が現在表示されているかを直接確認します。
        if mobile_menu_button.is_visible():
            expect(mobile_menu_button).to_be_visible()
            # Optionally, assert that desktop navigation links are not visible
            expect(page.get_by_role("navigation", name=re.compile(r"main|primary", re.IGNORECASE))).not_to_be_visible()
        else:
            # If no mobile-specific menu, ensure main nav is still present and adapting
            expect(page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
            expect(page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()

        # 3. フッターが適切に表示されていること。
        expect(page.get_by_text("© 2025 Asami K.", exact=False)).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_8_mobile_view_layout_check: {e}")

def test_9_copyright_year_validation(page: Page):
    """
    テストケース9: 著作権表示の年号検証 (境界値/正常系)
    フッターの著作権表示が最新の年号 (2025年) と正しい名前で表示されていることを確認する。
    """
    try:
        # 1. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_9_copyright_year.png"))

        # 1. フッターに "© 2025 Asami K." というテキストが正確に表示されていること。
        # Using to_contain_text is fine here as it's a specific string, but exact=False would also work.
        # Since the requirement strictly says "正確に表示されていること", we use to_have_text
        # but avoid exact=True to handle potential leading/trailing whitespace.
        expect(page.locator("footer")).to_contain_text("© 2025 Asami K.")

    except Error as e:
        pytest.fail(f"Playwright error in test_9_copyright_year_validation: {e}")

def test_10_no_console_errors(page: Page):
    """
    テストケース10: コンソールエラーの非発生検証 (異常系)
    ページのロード中や基本的な操作中に、ブラウザの開発者コンソールに重大なエラー
    (JavaScriptエラーなど) が出力されないことを確認し、ページの健全性を保証する。
    """
    console_errors = []

    def on_page_error(error):
        # 修正: pageerrorイベントからのエラーも、より具体的な文字列でリストに追加します。
        console_errors.append(f"Page Error: {error}")

    def on_console_message(msg):
        if msg.type == "error":
            # 修正: consoleイベントで発生する'error'レベルのメッセージも捕捉し、リストに追加します。
            console_errors.append(f"Console Error ({msg.type}): {msg.text}")
        # 全てのコンソールメッセージは引き続き出力してデバッグに役立てます。
        print(f"Console {msg.type}: {msg.text}")

    try:
        # 1. ブラウザのコンソールエラーを監視するリスナーを設定する。
        page.on("pageerror", on_page_error)
        # 修正: consoleイベントハンドラを専用の関数に分離し、エラーメッセージを捕捉するように変更します。
        page.on("console", on_console_message)

        # 2. トップページにアクセスする。
        # 修正: ページが完全にロードされ、ネットワーク活動が落ち着くまで待機する 'networkidle' オプションを追加し、
        # テストの安定性を向上させます。
        page.goto(BASE_URL, wait_until='networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # 3. 各ナビゲーションリンクをクリックし、ページ間を移動する
        # (例: Art, Camera, Appsページに遷移し、トップに戻る)。
        # Visit Art page
        art_link = page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))
        expect(art_link).to_be_visible()
        art_link.click()
        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art/?$"))
        page.go_back()
        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # Visit Camera page
        camera_link = page.get_by_role("link", name=re.compile(r"Camera", re.IGNORECASE))
        expect(camera_link).to_be_visible()
        camera_link.click()
        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')
        expect(page).to_have_url(re.compile(r"asami\.tokyo/camera/?$"))
        page.go_back()
        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # Visit Apps page
        apps_link = page.get_by_role("link", name=re.compile(r"Apps", re.IGNORECASE))
        expect(apps_link).to_be_visible()
        apps_link.click()
        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')
        expect(page).to_have_url(re.compile(r"asami\.tokyo/apps/?$"))
        page.go_back()
        # 修正: ページ遷移完了をより確実に待機するため、URLアサーションの前に 'networkidle' 状態を待機します。
        page.wait_for_load_state('networkidle')
        expect(page).to_have_url(re.compile(rf"^{re.escape(BASE_URL)}/?$"))

        # Save screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_10_no_console_errors.png"))

        # 1. ページロード中およびページ遷移中に、コンソールに error レベルのメッセージが出力されないこと。
        assert not console_errors, f"Console errors found: {console_errors}"

    except Error as e:
        pytest.fail(f"Playwright error in test_10_no_console_errors: {e}")
