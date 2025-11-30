import os
import re
import pytest
from datetime import datetime
from playwright.sync_api import Page, expect, sync_playwright, Error

# Base URL for the tests
BASE_URL = "https://asami.tokyo"
ABOUT_URL = f"{BASE_URL}/about"

@pytest.fixture(scope="module")
def page():
    """
    Provides a Playwright Page object for tests.
    This fixture ensures Playwright browser setup and teardown,
    and works even if pytest-playwright is not installed.
    """
    with sync_playwright() as p:
        # Launch Chromium browser
        browser = p.chromium.launch()
        # Create a new page
        page = browser.new_page()
        # Yield the page object to the tests
        yield page
        # Close the browser after all tests in the module are done
        browser.close()

# Helper function to save screenshots
def save_screenshot(page: Page, test_id: str, screenshot_name: str):
    """
    Saves a screenshot to the same directory as the test file.
    """
    save_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(save_dir, f"{test_id}_{screenshot_name}.png")
    page.screenshot(path=path)
    print(f"Screenshot saved to: {path}")

# --- Test Scenarios ---

# SCENARIO ID: DISP-001
def test_disp_001_page_and_content_display(page: Page):
    try:
        # Step 1: Access the About page
        response = page.goto(ABOUT_URL)

        # Assertion: Check if the initial page load was successful (HTTP status)
        assert response.status == 200, f"Expected 200, got {response.status} for {ABOUT_URL}"

        # Assertion: Verify the current URL is the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Assertion: Verify page title contains "About"
        expect(page).to_have_title(re.compile("About", re.IGNORECASE))

        # Assertion: Verify header navigation bar is displayed
        expect(page.get_by_role("banner")).to_be_visible()

        # Assertion: Verify "Art" heading is displayed
        expect(page.get_by_role("heading", name=re.compile("Art", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "Art" section text content is displayed
        expect(page.get_by_text(
            "I create visuals using TouchDesigner and Unreal Engine. I also write articles on Medium about generative AI prompts."
        )).to_be_visible()

        # Assertion: Verify "Development" heading is displayed
        expect(page.get_by_role("heading", name=re.compile("Development", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "Development" section text content is displayed
        expect(page.get_by_text(
            "I am developing the front-end of web applications using Vue.js and Nuxt.js. In addition, we are developing AI applications using LLM. Recently, I've been working on electronic projects using Arduino and other devices to help with my art."
        )).to_be_visible()

        # Assertion: Verify footer is displayed
        expect(page.get_by_role("contentinfo")).to_be_visible()

        # Save screenshot for successful page load
        save_screenshot(page, "DISP-001", "initial_load")

    except Error as e:
        pytest.fail(f"Playwright error in DISP-001: {e}")

# SCENARIO ID: DISP-002
def test_disp_002_all_links_displayed(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL is the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Assertion: Verify "View the Works." link is displayed
        expect(page.get_by_role("link", name=re.compile("View the Works", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "View the Video. ( Youtube / Vimeo )" link is displayed
        # Using a locator with filter as the name contains multiple keywords
        expect(page.locator("a").filter(has_text=re.compile("View the Video", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "View the Shop." link is displayed
        expect(page.get_by_role("link", name=re.compile("View the Shop", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "View the Touch Designer File." link is displayed
        expect(page.get_by_role("link", name=re.compile("View the Touch Designer File", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "View the AI Prompt." link is displayed
        expect(page.get_by_role("link", name=re.compile("View the AI Prompt", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "View the Code." link is displayed
        expect(page.get_by_role("link", name=re.compile("View the Code", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "View the DIY Electronics." link is displayed
        expect(page.get_by_role("link", name=re.compile("View the DIY Electronics", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify "View the Dify Application Files." link is displayed
        expect(page.get_by_role("link", name=re.compile("View the Dify Application Files", re.IGNORECASE))).to_be_visible()

        save_screenshot(page, "DISP-002", "all_links_displayed")

    except Error as e:
        pytest.fail(f"Playwright error in DISP-002: {e}")

# SCENARIO ID: DISP-003
def test_disp_003_copyright_display(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL is the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Check the copyright notice in the footer
        current_year = datetime.now().year

        # Assertion: Verify copyright information matches the current year and "Asami K."
        # Using locator and to_contain_text for robustness against surrounding whitespace.
        # Regex ensures flexibility for year if it's dynamic but still checks the pattern.
        expect(page.locator("footer")).to_contain_text(re.compile(rf"© {current_year} Asami K\.", re.IGNORECASE))

        save_screenshot(page, "DISP-003", "copyright_display")

    except Error as e:
        pytest.fail(f"Playwright error in DISP-003: {e}")

# SCENARIO ID: DISP-004
@pytest.mark.parametrize("width, height, device_name", [
    (375, 812, "smartphone"),  # iPhone X portrait
    (768, 1024, "tablet"),     # iPad portrait
    (1920, 1080, "desktop")    # Full HD desktop
])
def test_disp_004_responsive_design(page: Page, width: int, height: int, device_name: str):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL is the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2-4: Set viewport size and check layout
        page.set_viewport_size({"width": width, "height": height})

        # Assertion: Main content area should be visible
        expect(page.locator("main")).to_be_visible()

        # Assertion: Header should be visible
        expect(page.get_by_role("banner")).to_be_visible()

        # Assertion: Footer should be visible
        expect(page.get_by_role("contentinfo")).to_be_visible()

        # For smaller viewports, check for a potential hamburger menu
        if width <= 768: # Common breakpoint for mobile/tablet menus
            # Assertion: Check if a menu button (e.g., hamburger icon) is visible.
            # Use regex for common accessible names for menu buttons.
            menu_button = page.get_by_role("button", name=re.compile("menu|toggle navigation", re.IGNORECASE))
            if menu_button.count() > 0: # Check if a potential menu button exists
                expect(menu_button).to_be_visible()
                # Optional: If the site has a hamburger menu, expand and check navigation links
                # menu_button.click()
                # expect(page.get_by_role("navigation")).to_be_visible()
                # expect(page.get_by_role("link", name=re.compile("Top", re.IGNORECASE))).to_be_visible()
                # page.go_back() # Revert menu state if necessary

        # Assertion: Key headings should still be visible
        expect(page.get_by_role("heading", name=re.compile("Art", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("heading", name=re.compile("Development", re.IGNORECASE))).to_be_visible()

        # Save screenshot for each viewport size
        save_screenshot(page, "DISP-004", f"layout_{device_name}_{width}x{height}")

    except Error as e:
        pytest.fail(f"Playwright error in DISP-004 for {device_name} ({width}x{height}): {e}")

# SCENARIO ID: NAV-001
def test_nav_001_header_top_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click the "Top" link in the header
        # Using get_by_role with a regex name for case-insensitive matching of the accessible name
        page.get_by_role("link", name=re.compile("Top", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded") # Wait for navigation to complete

        # Assertion: Verify URL transitioned to the top page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/?$", re.IGNORECASE)) # Ends with / or /#...

        save_screenshot(page, "NAV-001", "top_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in NAV-001: {e}")

# SCENARIO ID: NAV-002
def test_nav_002_header_art_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click the "Art" link in the header
        page.get_by_role("link", name=re.compile("Art", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the Art page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/art", re.IGNORECASE))

        save_screenshot(page, "NAV-002", "art_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in NAV-002: {e}")

# SCENARIO ID: NAV-003
def test_nav_003_header_camera_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click the "Camera" link in the header
        page.get_by_role("link", name=re.compile("Camera", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the Camera page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/camera", re.IGNORECASE))

        save_screenshot(page, "NAV-003", "camera_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in NAV-003: {e}")

# SCENARIO ID: NAV-004
def test_nav_004_header_apps_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click the "Apps" link in the header
        page.get_by_role("link", name=re.compile("Apps", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the Apps page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/apps", re.IGNORECASE))

        save_screenshot(page, "NAV-004", "apps_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in NAV-004: {e}")

# SCENARIO ID: NAV-005
def test_nav_005_header_about_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click the "About" link in the header
        page.get_by_role("link", name=re.compile("About", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL remains the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        save_screenshot(page, "NAV-005", "about_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in NAV-005: {e}")

# SCENARIO ID: ART-001
def test_art_001_view_works_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "View the Works." link
        page.get_by_role("link", name=re.compile("View the Works", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the Works page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/works", re.IGNORECASE))

        save_screenshot(page, "ART-001", "works_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in ART-001: {e}")

# SCENARIO ID: ART-002
def test_art_002_view_video_youtube_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click the YouTube link within "View the Video."
        # Using a locator with filter to target a specific part of the link text
        with page.expect_popup() as popup_info:
            page.locator("a").filter(has_text=re.compile(r"Youtube", re.IGNORECASE)).click()
        
        popup = popup_info.value
        popup.wait_for_load_state("load") # Wait for the new tab to load

        # Assertion: New tab opened and its URL starts with youtube.com
        expect(popup).to_have_url(re.compile(r"youtube\.com", re.IGNORECASE))
        # Assertion: Original tab's URL remains the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        save_screenshot(popup, "ART-002", "youtube_popup_page")
        save_screenshot(page, "ART-002", "original_about_page")

    except Error as e:
        pytest.fail(f"Playwright error in ART-002: {e}")

# SCENARIO ID: ART-003
def test_art_003_view_video_vimeo_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click the Vimeo link within "View the Video."
        # Using a locator with filter to target a specific part of the link text
        with page.expect_popup() as popup_info:
            page.locator("a").filter(has_text=re.compile(r"Vimeo", re.IGNORECASE)).click()
        
        popup = popup_info.value
        popup.wait_for_load_state("load")

        # Assertion: New tab opened and its URL starts with vimeo.com
        expect(popup).to_have_url(re.compile(r"vimeo\.com", re.IGNORECASE))
        # Assertion: Original tab's URL remains the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        save_screenshot(popup, "ART-003", "vimeo_popup_page")
        save_screenshot(page, "ART-003", "original_about_page")

    except Error as e:
        pytest.fail(f"Playwright error in ART-003: {e}")

# SCENARIO ID: ART-004
def test_art_004_view_shop_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "View the Shop." link
        page.get_by_role("link", name=re.compile("View the Shop", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the Shop page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/shop", re.IGNORECASE))

        save_screenshot(page, "ART-004", "shop_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in ART-004: {e}")

# SCENARIO ID: ART-005
def test_art_005_view_touch_designer_file_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "View the Touch Designer File." link
        page.get_by_role("link", name=re.compile("View the Touch Designer File", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the TouchDesigner page (or a similar related page)
        # Note: Scenario allows for new tab with file, but assuming internal navigation for simplicity.
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/touchdesigner", re.IGNORECASE))

        save_screenshot(page, "ART-005", "touchdesigner_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in ART-005: {e}")

# SCENARIO ID: ART-006
def test_art_006_view_ai_prompt_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "View the AI Prompt." link
        page.get_by_role("link", name=re.compile("View the AI Prompt", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the AI Prompt page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/ai-prompt", re.IGNORECASE))

        save_screenshot(page, "ART-006", "ai_prompt_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in ART-006: {e}")

# SCENARIO ID: DEV-001
def test_dev_001_view_code_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "View the Code." link
        page.get_by_role("link", name=re.compile("View the Code", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the Code page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/code", re.IGNORECASE))

        save_screenshot(page, "DEV-001", "code_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in DEV-001: {e}")

# SCENARIO ID: DEV-002
def test_dev_002_view_diy_electronics_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "View the DIY Electronics." link
        page.get_by_role("link", name=re.compile("View the DIY Electronics", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the DIY Electronics page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/diy-electronics", re.IGNORECASE))

        save_screenshot(page, "DEV-002", "diy_electronics_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in DEV-002: {e}")

# SCENARIO ID: DEV-003
def test_dev_003_view_dify_application_files_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "View the Dify Application Files." link
        page.get_by_role("link", name=re.compile("View the Dify Application Files", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the Dify Applications page (or similar related page)
        # Similar to ART-005, assuming internal navigation.
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/dify-applications", re.IGNORECASE))

        save_screenshot(page, "DEV-003", "dify_applications_page_after_click")

    except Error as e:
        pytest.fail(f"Playwright error in DEV-003: {e}")

# SCENARIO ID: FOOT-001
def test_foot_001_footer_about_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "About" link in the footer
        # Using locator and get_by_role to narrowly target links within the footer
        page.locator("footer").get_by_role("link", name=re.compile("About", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL remains the About page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        save_screenshot(page, "FOOT-001", "about_page_after_footer_click")

    except Error as e:
        pytest.fail(f"Playwright error in FOOT-001: {e}")

# SCENARIO ID: FOOT-002
def test_foot_002_footer_law_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "law" link in the footer
        page.locator("footer").get_by_role("link", name=re.compile("law", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the law page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/law", re.IGNORECASE))

        save_screenshot(page, "FOOT-002", "law_page_after_footer_click")

    except Error as e:
        pytest.fail(f"Playwright error in FOOT-002: {e}")

# SCENARIO ID: FOOT-003
def test_foot_003_footer_contact_link(page: Page):
    try:
        # Step 1: Access the About page
        page.goto(ABOUT_URL)

        # Assertion: Verify the current URL before click
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/about", re.IGNORECASE))

        # Step 2: Click "contact" link in the footer
        page.locator("footer").get_by_role("link", name=re.compile("contact", re.IGNORECASE)).click()
        page.wait_for_load_state("domcontentloaded")

        # Assertion: Verify URL transitioned to the contact page
        expect(page).to_have_url(re.compile(rf"{BASE_URL}/contact", re.IGNORECASE))

        save_screenshot(page, "FOOT-003", "contact_page_after_footer_click")

    except Error as e:
        pytest.fail(f"Playwright error in FOOT-003: {e}")

# SCENARIO ID: ERR-001 (Abnormal case)
def test_err_001_non_existent_page(page: Page):
    try:
        # Create a unique non-existent URL to avoid caching issues
        non_existent_url = f"{BASE_URL}/non-existent-page-{datetime.now().timestamp()}"
        # Step 1: Access a non-existent URL
        # Use 'commit' to get status faster for 404 responses
        response = page.goto(non_existent_url, wait_until="commit")

        # Assertion: Verify HTTP status code is 404
        assert response.status == 404, f"Expected 404 status, but got {response.status} for {non_existent_url}"

        # Assertion: Verify a user-friendly error message is displayed
        # Look for common "page not found" texts in English or Japanese
        expect(page.get_by_text(re.compile(r"(ページが見つかりません|Page not found|404)", re.IGNORECASE))).to_be_visible()

        # Assertion: Verify site navigation (header) is still visible on the error page
        expect(page.get_by_role("banner")).to_be_visible()
        # Assertion: Verify footer is still visible on the error page
        expect(page.get_by_role("contentinfo")).to_be_visible()
        # Assertion: Verify a link to the top page (or home) exists
        expect(page.get_by_role("link", name=re.compile("Top|Home", re.IGNORECASE))).to_be_visible()

        save_screenshot(page, "ERR-001", "404_page")

    except Error as e:
        pytest.fail(f"Playwright error in ERR-001: {e}")

# SCENARIO ID: ERR-002 (Abnormal case for test code itself)
def test_err_002_invalid_selector_detection(page: Page):
    try:
        # Navigate to a known page to ensure Playwright context is active
        page.goto(ABOUT_URL)
        
        # Assertion: Attempt to locate a clearly non-existent element and assert its visibility.
        # This is designed to intentionally fail and raise a Playwright Error (e.g., TimeoutError)
        # because the element will not be found within the specified timeout.
        expect(page.locator("#definitely-not-an-existing-element-12345")).to_be_visible(timeout=1000)
        
        # If the above line passes (which it should not for a non-existent element),
        # then the test logic is flawed, and we explicitly fail the test.
        pytest.fail("Expected Playwright to raise an error for a non-existent selector, but it did not.")

    except Error as e:
        # Assertion: Verify that a Playwright Error (e.g., TimeoutError, or "locator resolved to no elements")
        # was caught. This confirms that the test script can detect issues with invalid selectors,
        # which is the purpose of this abnormal test scenario.
        error_message = str(e)
        assert "Timeout" in error_message or "locator resolved to no elements" in error_message, \
            f"Expected element not found or timeout error, but got: {error_message}"
        print(f"Successfully caught expected Playwright error for invalid selector: {e}")
        # The test passes because the expected error was caught.
    except Exception as e:
        # Catch any other unexpected exceptions and fail the test
        pytest.fail(f"Caught an unexpected exception type: {type(e).__name__} - {e}")