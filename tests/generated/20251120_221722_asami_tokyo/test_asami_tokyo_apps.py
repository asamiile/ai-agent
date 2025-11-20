import os
import pytest
import re
from playwright.sync_api import Page, expect, sync_playwright, Error

# Define the page fixture as per the requirements
@pytest.fixture(scope="module")
def page():
    """
    Playwright Page fixture for pytest.
    Launches a Chromium browser and provides a new page for each test module.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        # Set a default viewport size for consistency across tests
        page.set_viewport_size({"width": 1280, "height": 800})
        yield page
        browser.close()

# Directory to save screenshots, relative to the test file
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

# Base URL for the application
BASE_URL = "https://asami.tokyo"
APPS_URL = f"{BASE_URL}/apps"

def test_page_load_and_title_display(page: Page):
    """
    1.1. ページロードとタイトル表示
    目的: `https://asami.tokyo/apps` ページが正しくロードされ、適切なページタイトルが表示されることを確認する。
    """
    try:
        # Action: Navigate to the apps page
        response = page.goto(APPS_URL)

        # Assert: Page loaded successfully (HTTP status code 200)
        assert response.status == 200, f"Expected 200 status, got {response.status} for {APPS_URL}"

        # Assert: Page title contains "Apps" (case-insensitive partial match)
        # Comment: Verifying the page title for correctness.
        expect(page).to_have_title(re.compile("Apps", re.IGNORECASE))

        # Assert: Current URL is the expected apps URL
        # Comment: Verifying the final URL after navigation to ensure no redirects.
        expect(page).to_have_url(APPS_URL)

        # Take a screenshot for visual inspection
        page.screenshot(path=os.path.join(SAVE_DIR, "1_1_apps_page_load.png"))

    except Error as e:
        pytest.fail(f"Playwright error during page load and title display test: {e}")

def test_header_navigation_and_links(page: Page):
    """
    1.2. ヘッダーナビゲーションの表示とリンク検証
    目的: ヘッダー部分のナビゲーションメニューが正しく表示され、各リンクが適切なURLに遷移することを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        # Test "Top" link
        # Comment: Verifying "Top" link visibility and navigation.
        top_link = page.get_by_role("link", name=re.compile("Top", re.IGNORECASE))
        expect(top_link).to_be_visible()
        top_link.click()
        expect(page).to_have_url(BASE_URL + "/")
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        # Test "Art" link
        # Comment: Verifying "Art" link visibility and navigation.
        art_link = page.get_by_role("link", name=re.compile("Art", re.IGNORECASE))
        expect(art_link).to_be_visible()
        art_link.click()
        expect(page).to_have_url(BASE_URL + "/art")
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        # Test "Camera" link
        # Comment: Verifying "Camera" link visibility and navigation.
        camera_link = page.get_by_role("link", name=re.compile("Camera", re.IGNORECASE))
        expect(camera_link).to_be_visible()
        camera_link.click()
        expect(page).to_have_url(BASE_URL + "/camera")
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        # Test "Apps" link (current page)
        # Comment: Verifying "Apps" link visibility and ensuring no navigation occurs.
        apps_link = page.get_by_role("link", name=re.compile("Apps", re.IGNORECASE))
        expect(apps_link).to_be_visible()
        # Although it's the current page, click to ensure no unexpected navigation
        apps_link.click()
        expect(page).to_have_url(APPS_URL) # Assert URL remains Apps page

        # Take a screenshot for visual inspection
        page.screenshot(path=os.path.join(SAVE_DIR, "1_2_header_navigation.png"))

    except Error as e:
        pytest.fail(f"Playwright error during header navigation test: {e}")

def test_footer_content_and_links(page: Page):
    """
    1.3. フッターコンテンツの表示とリンク検証
    目的: フッター部分に著作権表示とナビゲーションリンクが正しく表示され、各リンクが適切なURLに遷移することを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        # Assert: Footer is visible on the page
        # Comment: Verifying that the footer section is present.
        footer_locator = page.locator("footer")
        expect(footer_locator).to_be_visible()

        # Assert: Copyright text "© 2025 Asami K." is displayed (partial match is default for to_contain_text/get_by_text)
        # Comment: Checking for the presence of the copyright information.
        expect(footer_locator.get_by_text("© 2025 Asami K.")).to_be_visible()

        # Test "About" link
        # Comment: Verifying "About" link visibility and navigation within the footer.
        about_link = footer_locator.get_by_role("link", name=re.compile("About", re.IGNORECASE))
        expect(about_link).to_be_visible()
        about_link.click()
        expect(page).to_have_url(BASE_URL + "/about")
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        # Test "law" link
        # Comment: Verifying "law" link visibility and navigation within the footer.
        law_link = footer_locator.get_by_role("link", name=re.compile("law", re.IGNORECASE))
        expect(law_link).to_be_visible()
        law_link.click()
        expect(page).to_have_url(BASE_URL + "/law")
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        # Test "contact" link
        # Comment: Verifying "contact" link visibility and navigation within the footer.
        contact_link = footer_locator.get_by_role("link", name=re.compile("contact", re.IGNORECASE))
        expect(contact_link).to_be_visible()
        contact_link.click()
        expect(page).to_have_url(BASE_URL + "/contact")
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        # Take a screenshot for visual inspection
        page.screenshot(path=os.path.join(SAVE_DIR, "1_3_footer_content.png"))

    except Error as e:
        pytest.fail(f"Playwright error during footer content test: {e}")

def test_global_event_timeline_card(page: Page):
    """
    2.1. 「Global Event Timeline」カードの表示とコンテンツ検証
    目的: 「Global Event Timeline」アプリケーションの紹介カードが正しく表示され、タイトル、説明、技術スタック、GitHubリンクが正しいことを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        # Locate the card using its heading
        card_title = "Global Event Timeline"
        # Comment: Locating the specific application card using its heading.
        card_locator = page.locator("section").filter(has=page.get_by_role("heading", name=re.compile(card_title, re.IGNORECASE)))

        # Assert: Card is visible
        # Comment: Verifying the card itself is displayed.
        expect(card_locator).to_be_visible()
        # Assert: Title is correct
        # Comment: Checking the main title of the card.
        expect(card_locator.get_by_role("heading")).to_contain_text(card_title)
        # Assert: Description text is correct (using nth for multiple paragraphs)
        # Comment: Checking the first paragraph of the description.
        expect(card_locator.locator("p").nth(0)).to_contain_text(
            "A video visualization that maps extreme weather event CSV data onto a world map."
        )
        # Assert: Tech stack text is correct
        # Comment: Checking the second paragraph, expected to contain tech stack.
        expect(card_locator.locator("p").nth(1)).to_contain_text(
            "TypeScript, Express, Canvas API, HTML5 Video Recording"
        )

        # Assert: GitHub link is visible
        # Comment: Verifying the GitHub link for the card is visible.
        github_link = card_locator.get_by_role("link", name=re.compile("GitHub", re.IGNORECASE))
        expect(github_link).to_be_visible()
        
        # Click GitHub link and verify URL. Expect navigation to an external site.
        # Comment: Clicking the GitHub link and asserting navigation and HTTP status.
        with page.expect_navigation(url=re.compile(r"https://github\.com/", re.IGNORECASE), wait_until="load") as navigation_info:
            github_link.click()
        
        # Assert: URL navigates to GitHub
        expect(page).to_have_url(re.compile(r"https://github\.com/", re.IGNORECASE))
        # Assert: External site loaded successfully (status 200)
        assert navigation_info.value.status == 200, f"GitHub link returned status {navigation_info.value.status} for {page.url}"
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        page.screenshot(path=os.path.join(SAVE_DIR, "2_1_global_event_timeline_card.png"))

    except Error as e:
        pytest.fail(f"Playwright error during Global Event Timeline card test: {e}")

def test_stat_dashboard_card(page: Page):
    """
    2.2. 「Stat Dashboard」カードの表示とコンテンツ検証
    目的: 「Stat Dashboard」アプリケーションの紹介カードが正しく表示され、タイトル、説明、技術スタック、Demoリンクが正しいことを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        card_title = "Stat Dashboard"
        # Comment: Locating the specific application card using its heading.
        card_locator = page.locator("section").filter(has=page.get_by_role("heading", name=re.compile(card_title, re.IGNORECASE)))

        # Assert: Card is visible
        expect(card_locator).to_be_visible()
        # Assert: Title is correct
        expect(card_locator.get_by_role("heading")).to_contain_text(card_title)
        # Assert: Description text is correct
        expect(card_locator.locator("p").nth(0)).to_contain_text(
            "This is a web dashboard app that allows you to upload CSV data from government statistics e-Stat and visualize it in graphs and summaries."
        )
        # Assert: Tech stack text is correct
        expect(card_locator.locator("p").nth(1)).to_contain_text(
            "Nuxt.js v3, shadcn/vue, Tailwind CSS, Fast API, Pandas, NumPy, Scikit-learn, Vercel"
        )

        # Assert: Demo link is visible
        # Comment: Verifying the Demo link for the card is visible.
        demo_link = card_locator.get_by_role("link", name=re.compile("Demo", re.IGNORECASE))
        expect(demo_link).to_be_visible()

        # Click Demo link and verify URL. Expect navigation to an external site.
        # Comment: Clicking the Demo link and asserting navigation and HTTP status.
        with page.expect_navigation(url=re.compile(r"https://stat-dashboard\.example\.com", re.IGNORECASE), wait_until="load") as navigation_info:
            demo_link.click()

        # Assert: URL navigates to the example demo URL
        expect(page).to_have_url(re.compile(r"https://stat-dashboard\.example\.com", re.IGNORECASE))
        # Assert: External site loaded successfully (status 200)
        assert navigation_info.value.status == 200, f"Demo link returned status {navigation_info.value.status} for {page.url}"
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        page.screenshot(path=os.path.join(SAVE_DIR, "2_2_stat_dashboard_card.png"))

    except Error as e:
        pytest.fail(f"Playwright error during Stat Dashboard card test: {e}")

def test_livesync_card(page: Page):
    """
    2.3. 「Livesync」カードの表示とコンテンツ検証
    目的: 「Livesync」アプリケーションの紹介カードが正しく表示され、タイトル、説明、技術スタック、Demoリンクが正しいことを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        card_title = "Livesync"
        # Comment: Locating the specific application card using its heading.
        card_locator = page.locator("section").filter(has=page.get_by_role("heading", name=re.compile(card_title, re.IGNORECASE)))

        # Assert: Card is visible
        expect(card_locator).to_be_visible()
        # Assert: Title is correct
        expect(card_locator.get_by_role("heading")).to_contain_text(card_title)
        # Assert: Description text is correct
        expect(card_locator.locator("p").nth(0)).to_contain_text(
            "Livesync is a live viewer app that synchronizes effects like color and animation in real time."
        )
        # Assert: Tech stack text is correct
        expect(card_locator.locator("p").nth(1)).to_contain_text(
            "Nuxt.js v3, shadcn/vue, Tailwind CSS, Storybook, Supabase, Vitest, Playwright, Vercel"
        )

        # Assert: Demo link is visible
        # Comment: Verifying the Demo link for the card is visible.
        demo_link = card_locator.get_by_role("link", name=re.compile("Demo", re.IGNORECASE))
        expect(demo_link).to_be_visible()

        # Click Demo link and verify URL. Expect navigation to an external site.
        # Comment: Clicking the Demo link and asserting navigation and HTTP status.
        with page.expect_navigation(url=re.compile(r"https://livesync\.example\.com", re.IGNORECASE), wait_until="load") as navigation_info:
            demo_link.click()

        # Assert: URL navigates to the example demo URL
        expect(page).to_have_url(re.compile(r"https://livesync\.example\.com", re.IGNORECASE))
        # Assert: External site loaded successfully (status 200)
        assert navigation_info.value.status == 200, f"Demo link returned status {navigation_info.value.status} for {page.url}"
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        page.screenshot(path=os.path.join(SAVE_DIR, "2_3_livesync_card.png"))

    except Error as e:
        pytest.fail(f"Playwright error during Livesync card test: {e}")

def test_marketplace_card(page: Page):
    """
    2.4. 「Marketplace」カードの表示とコンテンツ検証
    目的: 「Marketplace」アプリケーションの紹介カードが正しく表示され、タイトル、説明、技術スタック、Demoリンクが正しいことを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        card_title = "Marketplace"
        # Comment: Locating the specific application card using its heading.
        card_locator = page.locator("section").filter(has=page.get_by_role("heading", name=re.compile(card_title, re.IGNORECASE)))

        # Assert: Card is visible
        expect(card_locator).to_be_visible()
        # Assert: Title is correct
        expect(card_locator.get_by_role("heading")).to_contain_text(card_title)
        # Assert: Description text is correct
        expect(card_locator.locator("p").nth(0)).to_contain_text(
            "Nuxt Marketplace is a marketplace app for buying, selling, and managing digital assets."
        )
        # Assert: Tech stack text is correct
        expect(card_locator.locator("p").nth(1)).to_contain_text(
            "Nuxt.js v3, shadcn/vue, Tailwind CSS, Storybook, Supabase, Resend, Vitest, Playwright, Vercel"
        )

        # Assert: Demo link is visible
        # Comment: Verifying the Demo link for the card is visible.
        demo_link = card_locator.get_by_role("link", name=re.compile("Demo", re.IGNORECASE))
        expect(demo_link).to_be_visible()

        # Click Demo link and verify URL. Expect navigation to an external site.
        # Comment: Clicking the Demo link and asserting navigation and HTTP status.
        with page.expect_navigation(url=re.compile(r"https://marketplace\.example\.com", re.IGNORECASE), wait_until="load") as navigation_info:
            demo_link.click()

        # Assert: URL navigates to the example demo URL
        expect(page).to_have_url(re.compile(r"https://marketplace\.example\.com", re.IGNORECASE))
        # Assert: External site loaded successfully (status 200)
        assert navigation_info.value.status == 200, f"Demo link returned status {navigation_info.value.status} for {page.url}"
        page.go_back() # Go back to Apps page
        expect(page).to_have_url(APPS_URL) # Confirm returned

        page.screenshot(path=os.path.join(SAVE_DIR, "2_4_marketplace_card.png"))

    except Error as e:
        pytest.fail(f"Playwright error during Marketplace card test: {e}")

def test_application_card_lens_icons(page: Page):
    """
    2.5. アプリケーションカード内の"lens"アイコンの表示
    目的: 各アプリケーションカードに表示されている"lens"アイコン（画像）が正しく表示されていることを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        # Locate all images with alt text "lens"
        # Comment: Finding all image elements expected to be "lens" icons.
        lens_icons = page.locator('img[alt="lens"]')

        # Assert: At least one lens icon exists and is visible
        # Comment: Ensuring there's at least one such icon and it renders.
        expect(lens_icons.first()).to_be_visible()
        
        # Assert: All found lens icons are visible
        # This implicitly checks for broken images that typically would not render or be 'visible'
        # Comment: Iterating through all found icons to confirm individual visibility.
        for i in range(lens_icons.count()):
            expect(lens_icons.nth(i)).to_be_visible()

        page.screenshot(path=os.path.join(SAVE_DIR, "2_5_lens_icons.png"))

    except Error as e:
        pytest.fail(f"Playwright error during lens icon test: {e}")

def test_smartphone_viewport_layout(page: Page):
    """
    3.1. スマートフォンビューポートでのレイアウト検証
    目的: スマートフォンサイズのビューポートでページレイアウトが崩れず、コンテンツが適切に表示されることを確認する。
    """
    try:
        # Action: Set viewport to smartphone size
        # Comment: Adjusting browser viewport to simulate a smartphone.
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(APPS_URL)

        # Assert: Header is visible in the new viewport
        # Comment: Basic check for header visibility on mobile.
        expect(page.locator("header")).to_be_visible()
        # Assert: Footer is visible in the new viewport
        # Comment: Basic check for footer visibility on mobile.
        expect(page.locator("footer")).to_be_visible()

        # Take a full page screenshot for visual comparison
        # Comment: Saving a screenshot for manual or automated visual regression comparison.
        page.screenshot(path=os.path.join(SAVE_DIR, "3_1_smartphone_layout.png"), full_page=True)

    except Error as e:
        pytest.fail(f"Playwright error during smartphone layout test: {e}")
    finally:
        # Restore default viewport size for subsequent tests
        page.set_viewport_size({"width": 1280, "height": 800})


def test_tablet_viewport_layout(page: Page):
    """
    3.2. タブレットビューポートでのレイアウト検証
    目的: タブレットサイズのビューポートでページレイアウトが崩れず、コンテンツが適切に表示されることを確認する。
    """
    try:
        # Action: Set viewport to tablet size
        # Comment: Adjusting browser viewport to simulate a tablet.
        page.set_viewport_size({"width": 768, "height": 1024})
        page.goto(APPS_URL)

        # Assert: Header is visible in the new viewport
        # Comment: Basic check for header visibility on tablet.
        expect(page.locator("header")).to_be_visible()
        # Assert: Footer is visible in the new viewport
        # Comment: Basic check for footer visibility on tablet.
        expect(page.locator("footer")).to_be_visible()

        # Take a full page screenshot for visual comparison
        # Comment: Saving a screenshot for manual or automated visual regression comparison.
        page.screenshot(path=os.path.join(SAVE_DIR, "3_2_tablet_layout.png"), full_page=True)

    except Error as e:
        pytest.fail(f"Playwright error during tablet layout test: {e}")
    finally:
        # Restore default viewport size for subsequent tests
        page.set_viewport_size({"width": 1280, "height": 800})


def test_nonexistent_url_access(page: Page):
    """
    4.1. 存在しないURLへのアクセス
    目的: 存在しないURLにアクセスした場合に、適切なエラーページが表示されることを確認する。
    """
    try:
        non_existent_url = f"{APPS_URL}/nonexistent-page-12345" # Using a more unique non-existent path
        # Action: Navigate to a non-existent URL, wait for 'domcontentloaded' to ensure error page content loads
        # Comment: Attempting to access an invalid URL.
        response = page.goto(non_existent_url, wait_until="domcontentloaded")

        # Assert: HTTP status code is 404
        # Comment: Confirming the server responds with a 404 status.
        assert response.status == 404, f"Expected 404 status for {non_existent_url}, got {response.status}"

        # Assert: Error message (e.g., "Not Found" or "ページが見つかりません") is visible on the page
        # Comment: Checking for user-friendly error messages on the 404 page.
        expect(page.locator("body")).to_contain_text(re.compile("Not Found|ページが見つかりません|404", re.IGNORECASE))
        
        page.screenshot(path=os.path.join(SAVE_DIR, "4_1_nonexistent_url.png"))

    except Error as e:
        pytest.fail(f"Playwright error during nonexistent URL access test: {e}")

def test_external_link_check(page: Page):
    """
    4.2. 外部サイトへのリンク切れチェック (簡易版)
    目的: アプリケーション紹介カードの「Demo」や「GitHub」リンクがリンク切れを起こしていないか、遷移後のHTTPステータスコードが正常であることを確認する。
    """
    try:
        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        # Define all external links to check
        external_links = [
            {"card_title": "Global Event Timeline", "link_name": "GitHub", "expected_url_regex": r"https://github\.com/"},
            {"card_title": "Stat Dashboard", "link_name": "Demo", "expected_url_regex": r"https://stat-dashboard\.example\.com"},
            {"card_title": "Livesync", "link_name": "Demo", "expected_url_regex": r"https://livesync\.example\.com"},
            {"card_title": "Marketplace", "link_name": "Demo", "expected_url_regex": r"https://marketplace\.example\.com"},
        ]

        for link_info in external_links:
            card_title = link_info["card_title"]
            link_name = link_info["link_name"]
            expected_url_regex = link_info["expected_url_regex"]

            # Locate the specific link within its card
            # Comment: Finding the target link for each external destination.
            card_locator = page.locator("section").filter(has=page.get_by_role("heading", name=re.compile(card_title, re.IGNORECASE)))
            target_link = card_locator.get_by_role("link", name=re.compile(link_name, re.IGNORECASE))

            # Assert: Link is visible before clicking
            # Comment: Ensuring the link is interactable.
            expect(target_link).to_be_visible()

            # Action: Click the link and wait for navigation to the external URL
            # Use 'load' event to ensure the external page has fully loaded
            # Comment: Clicking the link and waiting for the new page to load.
            with page.expect_navigation(url=re.compile(expected_url_regex, re.IGNORECASE), wait_until="load") as navigation_info:
                target_link.click()

            # Assert: URL has navigated to the expected external site
            # Comment: Verifying the browser is on the correct external URL.
            expect(page).to_have_url(re.compile(expected_url_regex, re.IGNORECASE))
            
            # Assert: The response status is 200 (success)
            # Comment: Checking that the external page loaded without an HTTP error.
            assert navigation_info.value.status == 200, \
                f"Link '{link_name}' for '{card_title}' returned status {navigation_info.value.status} " \
                f"at {page.url} instead of 200."
            
            # Action: Go back to the apps page to test the next link
            page.go_back()
            # Comment: Confirming return to the original page before checking the next link.
            expect(page).to_have_url(APPS_URL)

        page.screenshot(path=os.path.join(SAVE_DIR, "4_2_external_links_check.png"))

    except Error as e:
        pytest.fail(f"Playwright error during external link check test: {e}")


def test_image_loading_error(page: Page):
    """
    4.3. 画像読み込みエラー
    目的: ページ内の画像がすべて正常に読み込まれていることを確認する。
    """
    try:
        # Comment: Setting up a listener to capture failed image requests.
        failed_image_requests = []
        page.on("requestfailed", lambda request: failed_image_requests.append(request.url) if request.resource_type == "image" else None)

        # Action: Navigate to the apps page
        page.goto(APPS_URL)

        # Assert: No image requests failed during page load
        # Comment: Checking if the `requestfailed` listener caught any image loading errors.
        assert not failed_image_requests, f"Some image requests failed to load: {failed_image_requests}"

        # Additionally, take a full page screenshot for visual inspection
        # This allows for manual verification of rendered images (e.g., no broken image icons).
        # Comment: Saving a full page screenshot for visual confirmation of image rendering.
        page.screenshot(path=os.path.join(SAVE_DIR, "4_3_image_loading.png"), full_page=True)

    except Error as e:
        pytest.fail(f"Playwright error during image loading test: {e}")
