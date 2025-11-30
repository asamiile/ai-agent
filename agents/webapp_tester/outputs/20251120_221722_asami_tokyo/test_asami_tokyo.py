import os
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

@pytest.fixture(scope="module")
def page():
    """
    Playwright の Page オブジェクトを Pytest フィクスチャとして提供します。
    pytest-playwright がインストールされていない環境でも動作するように、
    コード内で直接ブラウザを起動・終了します。
    """
    with sync_playwright() as p:
        # headless=False を指定すると、GUIのあるブラウザでテストを実行できます (デバッグ用)
        # CI/CD 環境では headless=True (デフォルト) を推奨
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({'width': 1920, 'height': 1080}) # デフォルトのビューポートサイズを設定
        yield page
        browser.close()

# スクリーンショット保存用のディレクトリパスを定義
# テストファイルと同じディレクトリに保存されます
SCREENSHOT_SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

def take_screenshot(page: Page, name: str):
    """指定された名前でスクリーンショットを保存するヘルパー関数"""
    path = os.path.join(SCREENSHOT_SAVE_DIR, name)
    page.screenshot(path=path)
    print(f"Screenshot saved to: {path}")

# A. ページのロードと基本表示テスト (正常系)
def test_A001_homepage_loads_successfully(page: Page):
    """A-001: トップページが正常にロードされること。"""
    try:
        # 1. Playwrightブラウザを起動し、指定されたURL https://asami.tokyo/ にアクセスする。
        print("Navigating to https://asami.tokyo/")
        response = page.goto("https://asami.tokyo/")

        # 1. ページのロードが完了し、HTTPステータスコードが200 OKであること。
        print(f"Checking HTTP status code. Expected 200, Got {response.status}")
        assert response.status == 200, f"Expected 200 OK, but received {response.status}"

        # 2. ページのタイトルがサイト名（例: "Asami K" や "Asami.Tokyo" など）を含む適切な文字列であること。
        print("Checking page title.")
        expect(page).to_have_title(/Asami K|Asami\.Tokyo/i) # 正規表現で部分一致、大文字小文字を区別しない

        # 3. faviconが表示されていること。
        # faviconは直接to_be_visible()で検証するのが難しい場合があるため、headタグ内にlink要素があることを確認
        print("Checking for favicon link in head.")
        expect(page.locator("head > link[rel*='icon']")).to_be_visible()

        take_screenshot(page, "A001_homepage_loaded.png")

    except Error as e:
        pytest.fail(f"Playwright error during test A-001: {e}")

def test_A002_main_navigation_and_footer_displayed(page: Page):
    """A-002: 主要なナビゲーションメニューとフッターが表示されること。"""
    try:
        # 1. トップページにアクセスする。
        print("Navigating to https://asami.tokyo/")
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url("https://asami.tokyo/") # URL確認

        # 1. ヘッダーナビゲーションメニュー (Top, Art, Camera, Apps, Asami K) がすべて表示され、クリック可能であること。
        print("Checking header navigation links.")
        # nameは大文字小文字を区別しない
        expect(page.get_by_role("link", name="Top", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Art", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Camera", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Apps", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Asami K", exact=False)).to_be_visible()

        # 2. フッターナビゲーションリンク (About, law, contact) がすべて表示され、クリック可能であること。
        print("Checking footer navigation links.")
        expect(page.get_by_role("link", name="About", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Law", exact=False)).to_be_visible() # lawはLawと表示される可能性を考慮
        expect(page.get_by_role("link", name="Contact", exact=False)).to_be_visible()

        # 3. 著作権表示 (© 2025 Asami K.) が表示されること。
        print("Checking copyright text.")
        expect(page.get_by_text("© 2025 Asami K", exact=False)).to_be_visible()
        expect(page.get_by_text("© 2025 Asami K", exact=False)).to_contain_text("2025 Asami K")

        take_screenshot(page, "A002_nav_and_footer.png")

    except Error as e:
        pytest.fail(f"Playwright error during test A-002: {e}")

def test_A003_no_console_errors(page: Page):
    """A-003: ページ内にコンソールエラーがないこと。"""
    try:
        console_errors = []
        # 2. Playwright の page.on('console') イベントを監視し、エラーや警告がログされないことを確認する。
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # 1. トップページにアクセスする。
        print("Navigating to https://asami.tokyo/ and checking for console errors.")
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url("https://asami.tokyo/") # URL確認

        # 1. ブラウザのコンソールにJavaScriptエラー、警告、または例外がログされないこと。
        # ページロード完了後、少し待ってからコンソールエラーを確認する
        page.wait_for_load_state("networkidle")
        print(f"Found {len(console_errors)} console errors.")
        assert not console_errors, f"Console errors found: {console_errors}"

        take_screenshot(page, "A003_no_console_errors.png")

    except Error as e:
        pytest.fail(f"Playwright error during test A-003: {e}")

def test_A004_main_text_content_displayed(page: Page):
    """A-004: 主要なテキストコンテンツが正しく表示されること。"""
    try:
        # 1. トップページにアクセスする。
        print("Navigating to https://asami.tokyo/")
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url("https://asami.tokyo/") # URL確認

        # 1. 自己紹介文 "I'm a front-end engineer and I use technology to express my art." が表示されること。
        print("Checking for introduction text.")
        expect(page.get_by_text("I'm a front-end engineer and I use technology to express my art", exact=False)).to_be_visible()
        expect(page.get_by_text("I'm a front-end engineer and I use technology to express my art", exact=False)).to_contain_text("front-end engineer")

        # 2. "Work Skill: TypeScript, JavaScript, Vue.js, Nuxt.js, Git, Figma, Photoshop." が表示されること。
        print("Checking for Work Skill text.")
        expect(page.get_by_text("Work Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("Work Skill: TypeScript, JavaScript, Vue.js, Nuxt.js, Git, Figma, Photoshop", exact=False)).to_contain_text("TypeScript")

        # 3. "Hobby Skill: Python, C++, Arduino, Unreal Engine, Blender, TouchDesigner, DaVinci Resolve." が表示されること。
        print("Checking for Hobby Skill text.")
        expect(page.get_by_text("Hobby Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("Hobby Skill: Python, C++, Arduino, Unreal Engine, Blender, TouchDesigner, DaVinci Resolve", exact=False)).to_contain_text("Python")

        take_screenshot(page, "A004_main_text_content.png")

    except Error as e:
        pytest.fail(f"Playwright error during test A-004: {e}")

# B. ナビゲーションリンクテスト (正常系)

def test_B001_header_top_link_navigates_to_homepage(page: Page):
    """B-001: ヘッダーの「Top」リンクがトップページへ遷移すること。"""
    try:
        # 1. トップページ以外のページ (例: Artページ) にアクセスする。
        print("Navigating to Art page first.")
        page.goto("https://asami.tokyo/art") # artページがない場合、gotoで404になる可能性もある
        # 実際に/artページが存在するか不明なため、一旦このgotoは成功すると仮定する。
        # ページが存在しない場合はtest_A001でURLチェックを追加する。

        # 2. ヘッダーの「Top」リンクをクリックする。
        print("Clicking 'Top' link in header.")
        top_link = page.get_by_role("link", name="Top", exact=False)
        expect(top_link).to_be_visible()
        top_link.click()

        # 1. URLが https://asami.tokyo/ に戻る。
        print("Checking URL after clicking 'Top'.")
        expect(page).to_have_url("https://asami.tokyo/")

        # 2. トップページの主要コンテンツ (自己紹介文など) が表示される。
        print("Checking for introduction text on homepage.")
        expect(page.get_by_text("I'm a front-end engineer", exact=False)).to_be_visible()

        take_screenshot(page, "B001_header_top_link.png")

    except Error as e:
        pytest.fail(f"Playwright error during test B-001: {e}")

# ナビゲーションリンクテストのヘルパー関数
def _test_navigation_link(page: Page, link_name: str, expected_url_regex: str, expected_title_regex: str, expected_content_text: str):
    """汎用ナビゲーションリンクテストヘルパー"""
    print(f"Testing navigation link: {link_name}")
    page.goto("https://asami.tokyo/")
    expect(page).to_have_url("https://asami.tokyo/") # トップページにいることを確認

    # ヘッダーかフッターのリンクを取得（どちらにあるか不明なため両方試す）
    # get_by_role("link", ...) はアクセシブル名で検索するため、信頼性が高い
    link_locator = page.get_by_role("link", name=link_name, exact=False)
    expect(link_locator).to_be_visible() # リンクが見えることを確認

    # リンクをクリック
    print(f"Clicking link: {link_name}")
    link_locator.click()

    # 1. URLが期待されるURLに遷移すること。
    print(f"Checking URL. Expected regex: {expected_url_regex}")
    expect(page).to_have_url(expected_url_regex)

    # 2. ページのタイトルが期待される文字列を含むこと。
    print(f"Checking page title. Expected regex: {expected_title_regex}")
    expect(page).to_have_title(expected_title_regex)

    # 3. 遷移先のページコンテンツが表示されること。
    print(f"Checking for expected content text: '{expected_content_text}'")
    expect(page.get_by_text(expected_content_text, exact=False)).to_be_visible()
    expect(page.get_by_text(expected_content_text, exact=False)).to_contain_text(expected_content_text)


def test_B002_header_art_link_navigates_correctly(page: Page):
    """B-002: ヘッダーの「Art」リンクがArtページへ遷移し、コンテンツが表示されること。"""
    try:
        _test_navigation_link(page, "Art", r"https://asami\.tokyo/art", r"Art", "Art Gallery" if "Art Gallery" else "Works") # 実際のコンテンツに合わせて調整
        take_screenshot(page, "B002_header_art_link.png")
    except Error as e:
        pytest.fail(f"Playwright error during test B-002: {e}")

def test_B003_header_camera_link_navigates_correctly(page: Page):
    """B-003: ヘッダーの「Camera」リンクがCameraページへ遷移し、コンテンツが表示されること。"""
    try:
        _test_navigation_link(page, "Camera", r"https://asami\.tokyo/camera", r"Camera", "Photography" if "Photography" else "Camera Works") # 実際のコンテンツに合わせて調整
        take_screenshot(page, "B003_header_camera_link.png")
    except Error as e:
        pytest.fail(f"Playwright error during test B-003: {e}")

def test_B004_header_apps_link_navigates_correctly(page: Page):
    """B-004: ヘッダーの「Apps」リンクがAppsページへ遷移し、コンテンツが表示されること。"""
    try:
        _test_navigation_link(page, "Apps", r"https://asami\.tokyo/apps", r"Apps", "Applications" if "Applications" else "Projects") # 実際のコンテンツに合わせて調整
        take_screenshot(page, "B004_header_apps_link.png")
    except Error as e:
        pytest.fail(f"Playwright error during test B-004: {e}")

def test_B005_header_asami_k_link_navigates_correctly(page: Page):
    """B-005: ヘッダーの「Asami K」リンクが適切なページへ遷移し、コンテンツが表示されること。"""
    try:
        # Asami K はプロフィールページまたはトップページへのリンクと推測される
        # 複数の可能性を考慮してOR条件で正規表現を記述
        _test_navigation_link(page, "Asami K", r"https://asami\.tokyo/(about)?", r"Asami K|About", "I'm a front-end engineer" if "I'm a front-end engineer" else "Profile")
        take_screenshot(page, "B005_header_asami_k_link.png")
    except Error as e:
        pytest.fail(f"Playwright error during test B-005: {e}")

def test_B006_footer_about_link_navigates_correctly(page: Page):
    """B-006: フッターの「About」リンクがAboutページへ遷移し、コンテンツが表示されること。"""
    try:
        _test_navigation_link(page, "About", r"https://asami\.tokyo/about", r"About", "About Me" if "About Me" else "I'm a front-end engineer") # 実際のコンテンツに合わせて調整
        take_screenshot(page, "B006_footer_about_link.png")
    except Error as e:
        pytest.fail(f"Playwright error during test B-006: {e}")

def test_B007_footer_law_link_navigates_correctly(page: Page):
    """B-007: フッターの「law」リンクがlawページへ遷移し、コンテンツが表示されること。"""
    try:
        _test_navigation_link(page, "Law", r"https://asami\.tokyo/law", r"Law|特定商取引法", "特定商取引法に基づく表記" if "特定商取引法に基づく表記" else "Legal Information") # 実際のコンテンツに合わせて調整
        take_screenshot(page, "B007_footer_law_link.png")
    except Error as e:
        pytest.fail(f"Playwright error during test B-007: {e}")

def test_B008_footer_contact_link_navigates_correctly(page: Page):
    """B-008: フッターの「contact」リンクがcontactページへ遷移し、コンテンツが表示されること。"""
    try:
        _test_navigation_link(page, "Contact", r"https://asami\.tokyo/contact", r"Contact|お問い合わせ", "お問い合わせフォーム" if "お問い合わせフォーム" else "Contact Us") # 実際のコンテンツに合わせて調整
        take_screenshot(page, "B008_footer_contact_link.png")
    except Error as e:
        pytest.fail(f"Playwright error during test B-008: {e}")

def test_B009_links_open_in_same_tab(page: Page):
    """B-009: リンクが同じタブ内で開くこと。"""
    try:
        # 1. トップページにアクセスする。
        print("Navigating to https://asami.tokyo/ to check link behavior.")
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url("https://asami.tokyo/") # URL確認

        # 2. ヘッダーまたはフッターのリンクをクリックする。
        # 例として「Art」リンクをクリックして検証
        print("Clicking 'Art' link and expecting no new popup.")
        art_link = page.get_by_role("link", name="Art", exact=False)
        expect(art_link).to_be_visible()

        # `with page.expect_popup() as popup_info:` を使用してポップアップが発生しないことを確認する
        # ポップアップが発生しないことを期待するため、例外が発生しないことをアサートする
        try:
            with page.expect_popup(timeout=1000) as popup_info: # 短いタイムアウトでポップアップを待機
                art_link.click()
            # ポップアップが発生した場合、ここに到達する
            pytest.fail("A new tab or window unexpectedly opened after clicking 'Art' link.")
        except Error:
            # timeout により expect_popup が失敗した場合、ポップアップは開かなかったと判断
            print("No popup detected, as expected.")
            pass

        # リンククリック後、URLが変わっていることを確認して、同じタブで遷移したことを補強
        print("Checking URL after clicking 'Art' link.")
        expect(page).to_have_url(r"https://asami\.tokyo/art")

        take_screenshot(page, "B009_links_same_tab.png")

    except Error as e:
        pytest.fail(f"Playwright error during test B-009: {e}")

# C. コンテンツの視覚的整合性テスト (正常系 / 境界値 - Visual Regression)
# Visual Regression Testing は、Playwright の expect().to_have_screenshot() や
# 外部ライブラリ (e.g., pytest-playwright-visual) を使うのが一般的ですが、
# 今回は指示に基づき、シンプルなスクリーンショット保存と手動確認を想定します。
# 厳密な比較は to_have_screenshot() の `threshold` オプションを使うことになります。

def test_C001_C005_C006_visual_consistency_desktop(page: Page):
    """
    C-001: トップページの主要要素が指定された画面サイズ (デスクトップ) で正しく表示されること。
    C-005: テキストコンテンツのフォントや配置が意図通りであること (スクリーンショットで確認)。
    C-006: 画像やアイコンが正しく表示されること。
    """
    try:
        # 1. トップページにアクセスする。
        print("Navigating to https://asami.tokyo/ for visual consistency test (desktop).")
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url("https://asami.tokyo/") # URL確認

        # 2. 画面サイズをデスクトップサイズに設定する（フィクスチャで設定済みだが念のため）
        print("Setting viewport size to 1920x1080.")
        page.set_viewport_size({'width': 1920, 'height': 1080})

        # 3. ページ全体のスクリーンショットを撮影し、基準画像と手動で比較する。
        # to_have_screenshot() を使用する場合は以下のように記述します
        # expect(page).to_have_screenshot("desktop_homepage.png", full_page=True, threshold=0.2)
        take_screenshot(page, "C_desktop_homepage_full.png")

        # 4. 主要なテキストコンテンツが視認可能であること (A-004の再確認)
        print("Verifying key text content visibility.")
        expect(page.get_by_text("I'm a front-end engineer", exact=False)).to_be_visible()
        expect(page.get_by_text("Work Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("Hobby Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("© 2025 Asami K", exact=False)).to_be_visible()

        # C-006: 画像やアイコンが正しく表示されること。
        # ページ内のすべてのimgタグを見つけ、表示されていることとalt属性があることを確認
        print("Checking for image visibility and alt attributes.")
        img_locators = page.locator("img")
        assert img_locators.count() > 0, "No image elements found on the page."

        for i in range(img_locators.count()):
            img = img_locators.nth(i)
            print(f"Checking image {i+1}/{img_locators.count()} (src: {img.get_attribute('src')}).")
            expect(img).to_be_visible()
            # alt属性の存在チェック。空でないことを確認
            alt_attr = img.get_attribute("alt")
            assert alt_attr is not None and alt_attr.strip() != "", \
                f"Image with src='{img.get_attribute('src')}' has missing or empty alt attribute."

        take_screenshot(page, "C_desktop_visual_consistency.png")

    except Error as e:
        pytest.fail(f"Playwright error during test C-001/C-005/C-006: {e}")


# D. レスポンシブデザインテスト (境界値)

def test_D001_D002_D003_responsive_mobile_layout(page: Page):
    """
    D-001: モバイルサイズ (例: 375x667) でレイアウトが崩れず、コンテンツが適切に表示されること。
    D-002: モバイルサイズでハンバーガーメニューが表示されること。
    D-003: ハンバーガーメニューがクリック可能で、ナビゲーションが展開されること。
    """
    try:
        # 1. トップページにアクセスする。
        print("Navigating to https://asami.tokyo/ for responsive mobile layout test.")
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url("https://asami.tokyo/") # URL確認

        # 2. 画面サイズをモバイルサイズに設定する (例: iPhone X)
        print("Setting viewport size to 375x667 (mobile).")
        page.set_viewport_size({'width': 375, 'height': 667})

        # D-001: モバイルサイズでレイアウトが崩れず、コンテンツが適切に表示されること。
        # 主要コンテンツが依然として表示されていることを確認
        print("Verifying key text content visibility in mobile view.")
        expect(page.get_by_text("I'm a front-end engineer", exact=False)).to_be_visible()
        expect(page.get_by_text("Work Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("Hobby Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("© 2025 Asami K", exact=False)).to_be_visible()

        take_screenshot(page, "D_mobile_homepage_initial.png")

        # D-002: モバイルサイズでハンバーガーメニューが表示されること。
        # 通常のナビゲーションリンクが非表示になり、ハンバーガーメニューが表示されることを確認
        print("Checking for hamburger menu visibility.")
        # ハンバーガーメニューのセレクタはサイトによって異なるため、一般的なものを仮定
        # aria-label="Open navigation" や role="button" で見つけることが多い
        hamburger_menu = page.locator("button[aria-label*='navigation'], button[role='button'].hamburger, .menu-icon")
        expect(hamburger_menu).to_be_visible()

        # デスクトップ用ナビゲーションが非表示になっていることを確認 (例: "Top"リンクが非表示)
        print("Checking if desktop navigation links are hidden.")
        expect(page.get_by_role("link", name="Top", exact=False)).not_to_be_visible()

        # D-003: ハンバーガーメニューがクリック可能で、ナビゲーションが展開されること。
        print("Clicking hamburger menu and checking for expanded navigation.")
        hamburger_menu.click()

        # 展開されたナビゲーションメニューが表示されることを確認
        # 展開されたメニュー内のリンク (例: "Art") が表示されることを確認
        expect(page.get_by_role("link", name="Art", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Camera", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Apps", exact=False)).to_be_visible()
        expect(page.get_by_role("link", name="Asami K", exact=False)).to_be_visible()

        take_screenshot(page, "D_mobile_hamburger_menu_opened.png")

    except Error as e:
        pytest.fail(f"Playwright error during test D-001/D-002/D-003: {e}")

def test_D004_responsive_tablet_layout(page: Page):
    """
    D-004: タブレットサイズ (例: 768x1024) でレイアウトが崩れず、コンテンツが適切に表示されること。
    """
    try:
        # 1. トップページにアクセスする。
        print("Navigating to https://asami.tokyo/ for responsive tablet layout test.")
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url("https://asami.tokyo/") # URL確認

        # 2. 画面サイズをタブレットサイズに設定する (例: iPad)
        print("Setting viewport size to 768x1024 (tablet).")
        page.set_viewport_size({'width': 768, 'height': 1024})

        # 3. ページ全体のスクリーンショットを撮影し、基準画像と手動で比較する。
        # expect(page).to_have_screenshot("tablet_homepage.png", full_page=True, threshold=0.2)
        take_screenshot(page, "D_tablet_homepage_full.png")

        # 4. 主要なテキストコンテンツが視認可能であること (A-004の再確認)
        print("Verifying key text content visibility in tablet view.")
        expect(page.get_by_text("I'm a front-end engineer", exact=False)).to_be_visible()
        expect(page.get_by_text("Work Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("Hobby Skill:", exact=False)).to_be_visible()
        expect(page.get_by_text("© 2025 Asami K", exact=False)).to_be_visible()

        # タブレットサイズではハンバーガーメニューが表示されるか、
        # あるいはデスクトップに近いナビゲーションが表示されるかを確認
        # ここではデスクトップナビゲーションが表示されると仮定
        print("Checking if desktop navigation links are visible in tablet view.")
        expect(page.get_by_role("link", name="Top", exact=False)).to_be_visible()
        # ハンバーガーメニューは非表示になっていると仮定
        hamburger_menu = page.locator("button[aria-label*='navigation'], button[role='button'].hamburger, .menu-icon")
        expect(hamburger_menu).not_to_be_visible()

        take_screenshot(page, "D_tablet_layout.png")

    except Error as e:
        pytest.fail(f"Playwright error during test D-004: {e}")