import os
import pytest
import re
from playwright.sync_api import Page, expect, sync_playwright, Error

# Define the page fixture as required, even if pytest-playwright is installed
@pytest.fixture(scope="module")
def page():
    """Provides a Playwright Page object for tests within the module."""
    with sync_playwright() as p:
        # Launch a Chromium browser
        browser = p.chromium.launch()
        # Create a new page
        page = browser.new_page()
        # Set a default viewport for consistency across tests
        page.set_viewport_size({"width": 1280, "height": 720})
        yield page
        # Close the browser after all tests in the module are done
        browser.close()

# Directory for saving screenshots, relative to this test file
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

def test_1_basic_page_display_and_content(page: Page):
    """
    Test scenario 1: Basic page display and main content verification.
    Ensures the page loads correctly and basic elements (header, main content, footer) are visible.
    """
    try:
        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        # Assert HTTP status code
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."

        # Assert URL after navigation
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging purposes
        page.screenshot(path=os.path.join(SAVE_DIR, "test_1_basic_display_art_page.png"))

        # Verify header navigation links
        # Using get_by_role with regex for case-insensitivity in link names
        expect(page.get_by_role("link", name=re.compile("Top", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("Art", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("Camera", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("Apps", re.IGNORECASE))).to_be_visible()

        # Verify 'Tools' text content using get_by_text
        expect(page.get_by_text("Tools: TouchDesigner, Photoshop, Midjourney, Runway")).to_be_visible()

        # Verify at least the first artwork title and its corresponding image
        # Using get_by_text for the title
        expect(page.get_by_text("Smoke drifting over big cities")).to_be_visible()
        # Locate the first image within the main content, assuming it's an artwork image
        expect(page.locator("main img").nth(0)).to_be_visible()

        # Verify footer copyright and links
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("About", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("law", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("contact", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_1_basic_page_display_and_content: {e}")

def test_2_navigation_link_behavior(page: Page):
    """
    Test scenario 2: Navigation links behavior.
    Checks that the 'Art' link is active and 'Top' link navigates correctly.
    """
    try:
        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging on the Art page
        page.screenshot(path=os.path.join(SAVE_DIR, "test_2_nav_behavior_art_page_before_click.png"))

        # Verify 'Art' link is active. This checks for an 'active' CSS class or similar indicator.
        # Assuming the 'active' class is applied directly to the link or a parent element that contains the link's text.
        # We target the link and check if its class list contains 'active'.
        expect(page.get_by_role("link", name=re.compile("Art", re.IGNORECASE))).to_have_class(re.compile(r'.*\bactive\b.*'))
        
        # Click the 'Top' link in the navigation
        top_link = page.get_by_role("link", name=re.compile("Top", re.IGNORECASE))
        expect(top_link).to_be_visible() # Ensure the link is visible before clicking
        top_link.click()

        # Verify URL changed to the top page
        expect(page).to_have_url("https://asami.tokyo/")

        # Take a screenshot after navigating to the Top page
        page.screenshot(path=os.path.join(SAVE_DIR, "test_2_nav_behavior_top_page_after_click.png"))

        # Verify a key content of the top page to confirm successful navigation
        # Replace with actual text expected on the homepage
        expect(page.locator('body')).to_contain_text(re.compile("Welcome|Portfolio", re.IGNORECASE)) 

    except Error as e:
        pytest.fail(f"Playwright error in test_2_navigation_link_behavior: {e}")

def test_3_artwork_image_display_and_alt_attributes(page: Page):
    """
    Test scenario 3: Artwork image display and alt attribute presence.
    Ensures artwork images are visible and have non-empty alt attributes for accessibility.
    """
    try:
        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_3_artwork_images_and_alt.png"))

        # Get all artwork image elements (assuming they are within the <main> content area)
        artwork_images = page.locator("main img")
        
        # Verify that at least one image exists and is visible
        expect(artwork_images.nth(0)).to_be_visible()
        
        # Get the count of images found
        num_images = artwork_images.count()
        assert num_images > 0, "No artwork images found on the page to verify."

        # Iterate over a representative set of images (e.g., first 5) to check alt attributes
        for i in range(min(num_images, 5)):
            image_locator = artwork_images.nth(i)
            # Verify the image element is visible
            expect(image_locator).to_be_visible()
            # Verify alt attribute exists and is not an empty string
            alt_text = image_locator.get_attribute("alt")
            assert alt_text is not None and len(alt_text.strip()) > 0, \
                f"Image {i} ({image_locator.get_attribute('src')}) is missing a non-empty alt attribute."

    except Error as e:
        pytest.fail(f"Playwright error in test_3_artwork_image_display_and_alt_attributes: {e}")

def test_4_footer_link_behavior(page: Page):
    """
    Test scenario 4: Footer link behavior.
    Checks that the 'About' link in the footer navigates correctly.
    """
    try:
        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging on the Art page before clicking
        page.screenshot(path=os.path.join(SAVE_DIR, "test_4_footer_links_art_page_before_click.png"))

        # Click the 'About' link in the footer
        # Using get_by_role with regex for case-insensitivity
        about_link = page.get_by_role("link", name=re.compile("About", re.IGNORECASE))
        expect(about_link).to_be_visible() # Ensure the link is visible
        about_link.click()

        # Verify URL changed to the About page
        expect(page).to_have_url("https://asami.tokyo/about")

        # Take a screenshot after navigating to the About page
        page.screenshot(path=os.path.join(SAVE_DIR, "test_4_footer_links_about_page_after_click.png"))

        # Verify a key content of the About page to confirm successful navigation
        # Replace with actual text expected on the About page
        expect(page.locator('body')).to_contain_text(re.compile("About|profile", re.IGNORECASE)) 

    except Error as e:
        pytest.fail(f"Playwright error in test_4_footer_link_behavior: {e}")

def test_5_responsive_design_mobile_viewport(page: Page):
    """
    Test scenario 5: Responsive design check for mobile viewport.
    Verifies page layout on a smartphone-sized screen.
    """
    try:
        # Set viewport size to a common smartphone size (e.g., iPhone 6/7/8)
        page.set_viewport_size({"width": 375, "height": 667})

        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging in mobile viewport
        page.screenshot(path=os.path.join(SAVE_DIR, "test_5_mobile_viewport.png"))

        # Verify navigation menu is mobile-friendly (e.g., hamburger icon visible or main nav hidden)
        # This locator should target your site's specific mobile menu toggle button.
        # Example: a button with role "button" and name "menu" or "toggle navigation".
        mobile_menu_button = page.get_by_role("button", name=re.compile("menu|toggle navigation", re.IGNORECASE))
        if mobile_menu_button.count() > 0: # Check if a mobile menu button exists
            expect(mobile_menu_button).to_be_visible()
            # Optionally, assert that desktop navigation links are not visible
            expect(page.get_by_role("link", name=re.compile("Top", re.IGNORECASE))).not_to_be_visible()
        else:
            # Fallback if no explicit mobile menu button: assume main nav adapts or is hidden
            # This assertion might need adjustment based on the actual site's mobile behavior
            expect(page.locator("header nav")).to_be_visible() # Ensure header nav is still present
            # Further checks for layout adaptation if no hamburger menu

        # Verify main content (e.g., artwork images and text) are visible and not causing horizontal scroll.
        # Check for horizontal scroll by comparing document's scrollWidth with viewport width.
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        viewport_width = page.viewport_size["width"]
        # Allow a small margin of error for browser rendering inconsistencies
        assert scroll_width <= viewport_width + 5, f"Horizontal scroll detected. Scroll width: {scroll_width}, Viewport width: {viewport_width}"

        expect(page.locator("main img").nth(0)).to_be_visible() # At least one artwork image should still be visible
        expect(page.get_by_text("Tools:")).to_be_visible() # Tools section text should be visible

        # Verify footer is appropriately displayed
        expect(page.locator("footer")).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_5_responsive_design_mobile_viewport: {e}")

def test_6_copyright_notice_verification(page: Page):
    """
    Test scenario 6: Copyright notice verification.
    Ensures the correct copyright text and year are displayed in the footer.
    """
    try:
        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_6_copyright_notice.png"))

        # Verify the exact copyright text is contained within the footer
        # Using to_contain_text is more robust as it allows for surrounding text/elements.
        expect(page.locator("footer")).to_contain_text("© 2025 Asami K.")

    except Error as e:
        pytest.fail(f"Playwright error in test_6_copyright_notice_verification: {e}")

def test_7_tools_display_verification(page: Page):
    """
    Test scenario 7: Tools name display verification.
    Ensures all specified tool names are accurately displayed in the 'Tools' section.
    """
    try:
        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging
        page.screenshot(path=os.path.join(SAVE_DIR, "test_7_tools_display.png"))

        # Verify the full 'Tools' text content is visible
        # get_by_text is suitable here as we expect the full string to appear.
        expect(page.get_by_text("Tools: TouchDesigner, Photoshop, Midjourney, Runway")).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_7_tools_display_verification: {e}")

def test_8_non_existent_url_404_page(page: Page):
    """
    Test scenario 8 (Negative): Accessing a non-existent URL and checking for a 404 page.
    Verifies that a proper 404 error page is displayed.
    """
    try:
        # Navigate to a non-existent URL. Use wait_until="commit" to capture the initial response.
        response = page.goto("https://asami.tokyo/non-existent-page", wait_until="commit")
        
        # Verify HTTP status code is 404
        assert response.status == 404, f"Expected 404, got {response.status} for non-existent page."

        # Take a screenshot for debugging the 404 page
        page.screenshot(path=os.path.join(SAVE_DIR, "test_8_404_page.png"))

        # Verify a 404 error message or indicator in the page content or title
        # Using a regex to broadly match common 404 phrases
        expect(page.locator("body")).to_contain_text(re.compile("404|not found|ページが見つかりません", re.IGNORECASE))
        # Also check the page title if it reflects the 404 status
        expect(page).to_have_title(re.compile("404|not found", re.IGNORECASE))

    except Error as e:
        pytest.fail(f"Playwright error in test_8_non_existent_url_404_page: {e}")

def test_9_image_load_failure(page: Page):
    """
    Test scenario 9 (Negative): Image load failure.
    Verifies behavior when images fail to load (e.g., alt text or broken image icon).
    """
    try:
        # Route and intercept image requests to simulate failure (e.g., 404 Not Found)
        page.route("**/art/images/*", lambda route: route.fulfill(status=404))

        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Take a screenshot for debugging with failed image loads
        page.screenshot(path=os.path.join(SAVE_DIR, "test_9_image_load_failure.png"))

        # Verify that images are "broken" or their natural dimensions are 0/1
        # Get all artwork image elements
        artwork_images = page.locator("main img")
        num_images = artwork_images.count()
        assert num_images > 0, "No artwork images found on the page to test failure."

        # Check a representative set of images (e.g., first 3) for load failure
        for i in range(min(num_images, 3)):
            image_locator = artwork_images.nth(i)
            # Wait for the image element to be rendered and its properties to be accessible
            image_locator.wait_for() 
            # Evaluate JavaScript to get naturalWidth and naturalHeight, which are 0 or 1 for broken images
            natural_width = image_locator.evaluate("img => img.naturalWidth")
            natural_height = image_locator.evaluate("img => img.naturalHeight")

            # Assert that the image failed to load (natural dimensions are typically 0 or 1 for broken images)
            assert natural_width <= 1 or natural_height <= 1, \
                f"Image {i} ({image_locator.get_attribute('src')}) loaded successfully (naturalWidth: {natural_width}, naturalHeight: {natural_height}), but was expected to fail loading."
            
            # The alt attribute presence is checked in test_3. If alt text is visible, it's a manual verification via screenshot.

    except Error as e:
        pytest.fail(f"Playwright error in test_9_image_load_failure: {e}")

def test_10_text_size_change_display(page: Page):
    """
    Test scenario 10 (Boundary): Browser text size change display.
    Ensures page layout remains stable and text is readable when text size is larger.
    """
    try:
        # Navigate to the Art page
        response = page.goto("https://asami.tokyo/art")
        assert response.status == 200, f"Expected 200, got {response.status} for /art page."
        expect(page).to_have_url("https://asami.tokyo/art")

        # Set the browser's text size to 'larger'
        page.emulate_media(text_size='larger')

        # Take a screenshot for debugging with larger text
        page.screenshot(path=os.path.join(SAVE_DIR, "test_10_larger_text_size.png"))

        # Verify key elements are still visible and not severely overlapping or broken.
        # Direct assertion for "no overlap" is complex. We'll check visibility of major content blocks.
        
        # Verify header is still visible
        expect(page.locator("header")).to_be_visible()
        # Verify main navigation links are still visible (they might wrap to new lines, but shouldn't disappear)
        expect(page.get_by_role("link", name=re.compile("Top", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_role("link", name=re.compile("Art", re.IGNORECASE))).to_be_visible()

        # Verify artwork titles and tools section are visible
        expect(page.get_by_text("Smoke drifting over big cities")).to_be_visible()
        expect(page.get_by_text("Tools:")).to_be_visible()

        # Verify footer is visible
        expect(page.locator("footer")).to_be_visible()

        # For a thorough check, visual regression testing would be ideal here.
        # These assertions provide a basic functional check that critical elements are still present.
        # Manual review of the screenshot `test_10_larger_text_size.png` is highly recommended.

    except Error as e:
        pytest.fail(f"Playwright error in test_10_text_size_change_display: {e}")