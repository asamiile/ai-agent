import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

@pytest.fixture(scope="module")
def page():
    """
    Playwright Page fixture for pytest.
    This fixture ensures that a Playwright browser and page are available for tests,
    even if pytest-playwright is not globally installed.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Set a common viewport size for consistency, can be overridden per test if needed.
        page.set_viewport_size({"width": 1280, "height": 720})
        yield page
        browser.close()

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
        expect(page).to_have_title(re.compile(r"Asami K", re.IGNORECASE))

        # Assert: Main introduction text is visible
        expect(page.get_by_text("I'm a front-end engineer and I use technology to express my art.")).to_be_visible()

        # Assert: Work Skill and Hobby Skill headers are visible
        expect(page.get_by_role("heading", name=re.compile(r"Work Skill", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("heading", name=re.compile(r"Hobby Skill", re.IGNORECASE))).to_be_visible()

        # Assert: Footer copyright notice is visible
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error during test_homepage_content_display: {e}")

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
            expect(nav_locator).to_be_visible() # Ensure link is visible before clicking
            nav_locator.click()

            # Assert: URL matches the expected path
            expect(page).to_have_url(re.compile(rf"https://asami\.tokyo{expected_path}/?"))
            # Assert: A unique element/heading on the target page is visible (e.g., page title or a main heading)
            expect(page.get_by_role("heading", name=re.compile(link_name, re.IGNORECASE)).first).to_be_visible()

            # Assert: Navigate back to Top from the current page
            top_link_locator = page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE)).first
            expect(top_link_locator).to_be_visible() # Ensure Top link is visible
            top_link_locator.click()
            expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))

    except Error as e:
        pytest.fail(f"Playwright error during test_global_navigation_links: {e}")

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
            expect(page.get_by_role("heading", name=re.compile(link_name, re.IGNORECASE)).first).to_be_visible()
            # Navigate back to the homepage for the next link click
            page.goto("https://asami.tokyo/")
            expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))

    except Error as e:
        pytest.fail(f"Playwright error during test_footer_navigation_links: {e}")

def test_homepage_internal_links_status(page: Page):
    """
    Scenario 4: トップページ内の内部リンクのリンク切れチェック
    目的: トップページからアクセス可能な内部リンクが有効であり、ユーザーがリンク切れのページに遭遇しないことを確認する。
    (このテストはトップページ上のリンクのみを対象とします。サイト全体のクロールは単一テストの責務を超えます。)
    """
    try:
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))

        # Get all anchor tags on the page
        all_links = page.locator("a").all()
        internal_links = set()

        # Filter for internal links
        for link_element in all_links:
            href = link_element.get_attribute("href")
            if href and (href.startswith("/") or href.startswith("https://asami.tokyo")):
                # Normalize URL to avoid duplicates (e.g., /art and /art/)
                full_url = page.url.split('://')[0] + '://' + page.url.split('://')[1].split('/')[0] + href
                internal_links.add(full_url.rstrip('/'))

        if not internal_links:
            pytest.fail("No internal links found on the homepage to test.")

        # Visit each internal link and check its status
        for link_url in internal_links:
            # Assert: Navigate to the internal link
            response = page.goto(link_url)
            # Assert: HTTP status code is 200 OK
            assert response.status == 200, f"Link broken: {link_url} returned status {response.status}"
            # Navigate back to homepage for next link check (prevents complex history management)
            page.goto("https://asami.tokyo/")

    except Error as e:
        pytest.fail(f"Playwright error during test_homepage_internal_links_status: {e}")

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
                expect(page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE))).to_be_visible()
                expect(page.get_by_role("link", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()

            # Assert: Footer copyright is visible and not cut off (simple visibility check)
            expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()

            # Optional: Take a screenshot for visual debugging
            page.screenshot(path=os.path.join(save_dir, f"homepage_{name.lower()}.png"))

    except Error as e:
        pytest.fail(f"Playwright error during test_responsive_design_viewports: {e}")

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
        expect(page.get_by_text(re.compile(r"404 Not Found|ページが見つかりません", re.IGNORECASE))).to_be_visible()
        # Assert: Link to homepage or a prominent "back to site" link exists
        expect(page.get_by_role("link", name=re.compile(r"Top|Home", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error during test_nonexistent_url_error_page: {e}")

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
            assert is_loaded, f"Image failed to load: {img_locator.get_attribute('src')}"
            # Assert: Image has an alt attribute (important for accessibility)
            alt_text = img_locator.get_attribute("alt")
            assert alt_text is not None and len(alt_text.strip()) > 0, \
                f"Image missing or empty alt text: {img_locator.get_attribute('src')}"

    except Error as e:
        pytest.fail(f"Playwright error during test_art_page_image_content_display: {e}")

def test_footer_copyright_year(page: Page):
    """
    Scenario 8: フッターの著作権表示年号の確認テスト
    目的: フッターに表示されている著作権年号が「2025」と正しく表示されていることを確認する。
    """
    try:
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))

        # Assert: Footer contains the exact copyright text including the year "2025"
        # Using get_by_text with partial match is fine here, as the scenario specified 'contains "2025"'
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()
        expect(page.locator("footer")).to_contain_text("2025 Asami K.")

    except Error as e:
        pytest.fail(f"Playwright error during test_footer_copyright_year: {e}")

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
        pytest.fail(f"Playwright error during test_no_javascript_errors_on_console: {e}")

def test_contact_page_form_existence(page: Page):
    """
    Scenario 10: 連絡先（Contact）ページへのアクセスとフォームの存在確認
    目的: フッターからアクセスできる「Contact」ページが存在し、連絡フォームがある場合はその基本的な表示を確認する。
    """
    try:
        page.goto("https://asami.tokyo/")
        expect(page).to_have_url(re.compile(r"https://asami\.tokyo/?"))

        # Click the "contact" link in the footer
        contact_link = page.locator("footer").get_by_role("link", name=re.compile(r"contact", re.IGNORECASE)).first
        expect(contact_link).to_be_visible() # Ensure link is visible
        contact_link.click()

        # Assert: URL matches the expected contact path
        expect(page).to_have_url(re.compile(r"https://asami\.tokyo/contact/?"))
        # Assert: Page title or a main heading contains "Contact"
        expect(page.get_by_role("heading", name=re.compile(r"Contact", re.IGNORECASE))).to_be_visible()

        # Check for the existence of basic form elements
        # These locators are general and assume standard HTML form elements
        # Assert: At least one input field is visible
        expect(page.locator("input").first).to_be_visible()
        # Assert: At least one textarea field is visible
        expect(page.locator("textarea").first).to_be_visible()
        # Assert: A submit button is visible
        expect(page.locator("button[type='submit']").first).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error during test_contact_page_form_existence: {e}")