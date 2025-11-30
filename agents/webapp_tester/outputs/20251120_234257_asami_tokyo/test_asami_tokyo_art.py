import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

@pytest.fixture(scope="module")
def page():
    """
    pytest-playwrightがインストールされていない環境でも動作するように、
    pageフィクスチャをコード内で定義します。
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page_instance = browser.new_page()
        # 修正1: Playwrightのデフォルトアクションタイムアウトを延長
        # デフォルトは5秒。要素の出現待ちなどでタイムアウトが発生しやすいため、15秒に延長します。
        page_instance.set_default_timeout(15000) # 15秒
        # 修正2: Playwrightのデフォルトナビゲーションタイムアウトを延長（任意）
        # page.goto()のデフォルトは30秒ですが、明示的に設定することで安定性を高めます。
        page_instance.set_default_navigation_timeout(30000) # 30秒
        yield page_instance
        browser.close()

# テストファイルと同じディレクトリにスクリーンショットを保存するためのパスを設定
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

def take_screenshot(page: Page, name: str):
    """スクリーンショットを撮影し、指定されたディレクトリに保存するヘルパー関数"""
    path = os.path.join(SAVE_DIR, name)
    try:
        page.screenshot(path=path)
        print(f"Screenshot saved to: {path}")
    except Error as e:
        print(f"Failed to take screenshot {name}: {e}")

def test_01_main_content_display(page: Page):
    """
    テストケース1: ページ主要コンテンツの表示確認
    ページロード時に、主要なテキストコンテンツが期待通りに表示されることを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        # ページ全体のタイムアウトを回避するため、goto操作の安定性を確保
        response = page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        # URLが期待通りであることを確認
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        # HTTPステータスコードが200であることを確認
        assert response.status == 200, f"Expected status 200, got {response.status}"
        take_screenshot(page, "01_main_content_display.png")

        # 2. ページタイトル「Art」が表示されていることを確認する。
        # get_by_role('heading') を使用し、nameは大文字小文字を区別しない正規表現で部分一致
        print("Asserting 'Art' heading is visible.")
        expect(page.get_by_role("heading", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()
        # ページ全体のタイトルも確認
        print("Asserting page title contains 'Art'.")
        expect(page).to_have_title(re.compile(r"Art", re.IGNORECASE))

        # 3. 「Tools: TouchDesigner, Photoshop, Midjourney, Runway」のテキストが表示されていることを確認する。
        # get_by_text を使用し、部分一致
        print("Asserting 'Tools' text is visible.")
        expect(page.get_by_text("Tools: TouchDesigner, Photoshop, Midjourney, Runway")).to_be_visible()

        # 4. 「Smoke drifting over big cities」と「Resort Pool」などの作品名がリスト表示されていることを確認する。
        # get_by_text を使用し、部分一致
        print("Asserting work title 'Smoke drifting over big cities' is visible.")
        expect(page.get_by_text("Smoke drifting over big cities")).to_be_visible()
        print("Asserting work title 'Resort Pool' is visible.")
        expect(page.get_by_text("Resort Pool")).to_be_visible()

        # 5. フッターに「© 2025 Asami K.」が表示されていることを確認する。
        # get_by_text を使用し、部分一致
        print("Asserting footer copyright is visible.")
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()

    except Error as e:
        take_screenshot(page, "FAIL_01_main_content_display.png")
        pytest.fail(f"Playwright error in test_01_main_content_display: {e}")

def test_02_global_navigation_links(page: Page):
    """
    テストケース2: グローバルナビゲーションリンクの動作確認
    グローバルナビゲーション内の各リンクが正しく機能し、対応するページへ遷移することを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "02_global_navigation_start.png")

        # 2. ナビゲーションメニューの「Top」リンクをクリックする。
        print("Clicking 'Top' navigation link.")
        # get_by_role("link", name=re.compile(r"Top", re.IGNORECASE)) で大文字小文字を区別しないリンク名を探す
        page.get_by_role("link", name=re.compile(r"Top", re.IGNORECASE)).click()
        # 修正: クリック後のページ遷移が完了し、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        # 3. ページがトップページ（https://asami.tokyo/ など）に遷移することを確認する。
        print("Asserting URL is the top page.")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/$"))
        take_screenshot(page, "02_global_navigation_top.png")

        # 元のArtページに戻る
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))

        # 4. 「Camera」リンクをクリックし、対応するURLに遷移することを確認する。
        print("Clicking 'Camera' navigation link.")
        page.get_by_role("link", name=re.compile(r"Camera", re.IGNORECASE)).click()
        # 修正: クリック後のページ遷移が完了し、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        print("Asserting URL is the camera page.")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/camera"))
        take_screenshot(page, "02_global_navigation_camera.png")

        # 元のArtページに戻る
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))

        # 5. 「Apps」リンクをクリックし、対応するURLに遷移することを確認する。
        print("Clicking 'Apps' navigation link.")
        page.get_by_role("link", name=re.compile(r"Apps", re.IGNORECASE)).click()
        # 修正: クリック後のページ遷移が完了し、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        print("Asserting URL is the apps page.")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/apps"))
        take_screenshot(page, "02_global_navigation_apps.png")

    except Error as e:
        take_screenshot(page, "FAIL_02_global_navigation_links.png")
        pytest.fail(f"Playwright error in test_02_global_navigation_links: {e}")

def test_03_works_list_display(page: Page):
    """
    テストケース3: 作品リストの表示確認
    複数のアート作品がリストとして表示されることを確認する。
    (作品名自体はリンクではないため、クリック動作の確認は行わない)
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "03_works_list_display.png")

        # 2. 複数の作品名（例：「Smoke drifting over big cities」、「Resort Pool」）が表示されていることを確認する。
        # 複数の要素が存在することを確認するために、locator().all() や expect().to_have_count() を使用
        # または、個々の要素の表示を確認する
        print("Asserting multiple work titles are visible.")
        expect(page.get_by_text("Smoke drifting over big cities")).to_be_visible()
        expect(page.get_by_text("Resort Pool")).to_be_visible()
        expect(page.get_by_text("Cyber City")).to_be_visible()
        expect(page.get_by_text("Floating Future")).to_be_visible()

        # より一般的な方法として、全ての作品タイトルがh2タグとして表示されていると仮定し、その数を検証
        # locator("h2").filter(has_text=re.compile(r".+")) で全ての非空のh2を対象にできる
        print("Asserting there are multiple work titles (h2 elements).")
        work_titles_count = page.locator("h2").filter(has_text=re.compile(r"[a-zA-Z0-9]+")).count()
        assert work_titles_count >= 4, f"Expected at least 4 work titles, found {work_titles_count}"

    except Error as e:
        take_screenshot(page, "FAIL_03_works_list_display.png")
        pytest.fail(f"Playwright error in test_03_works_list_display: {e}")

def test_04_footer_links(page: Page):
    """
    テストケース4: フッターリンクの動作確認
    フッターに表示されている「About」および「contact」リンクが正しく機能し、対応するページへ遷移することを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "04_footer_links_start.png")

        # 2. フッターの「About」リンクをクリックする。
        print("Clicking 'About' footer link.")
        # get_by_role("link", name=re.compile(r"About", re.IGNORECASE)) で大文字小文字を区別しないリンク名を探す
        page.get_by_role("link", name=re.compile(r"About", re.IGNORECASE)).click()
        # 修正: クリック後のページ遷移が完了し、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        # 3. ページが「About」ページ（https://asami.tokyo/about など）に遷移することを確認する。
        print("Asserting URL is the about page.")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/about"))
        take_screenshot(page, "04_footer_links_about.png")

        # 4. 元のページに戻り、「contact」リンクをクリックする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        print("Clicking 'contact' footer link.")
        page.get_by_role("link", name=re.compile(r"contact", re.IGNORECASE)).click()
        # 修正: クリック後のページ遷移が完了し、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        # 5. ページが「Contact」ページ（https://asami.tokyo/contact など）に遷移することを確認する。
        print("Asserting URL is the contact page.")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/contact"))
        take_screenshot(page, "04_footer_links_contact.png")

    except Error as e:
        take_screenshot(page, "FAIL_04_footer_links.png")
        pytest.fail(f"Playwright error in test_04_footer_links: {e}")

def test_05_image_content_loading(page: Page):
    """
    テストケース5: 画像コンテンツのロード確認
    ページ内の作品画像が正しくロードされ、壊れていないことを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "05_image_loading_check.png")

        # 2. ページ内のすべての`<img>`要素が存在することを確認する。
        print("Finding all image elements.")
        images = page.locator("img").all()
        assert len(images) > 0, "No image elements found on the page."

        # 3. 各`<img>`要素がロードされ、`naturalWidth`が0より大きいことを確認する。
        # (画像が正しく表示されていることの簡易チェック)
        print("Asserting all images are loaded correctly (naturalWidth > 0).")
        for i, img_locator in enumerate(images):
            try:
                # `is_visible()`で要素がDOM上にあり、表示されている可能性のある状態かを確認
                expect(img_locator).to_be_visible()
                # naturalWidthは要素がDOMにあり、レイアウト計算されている必要があるため、evaluateを使用
                natural_width = img_locator.evaluate("img => img.naturalWidth")
                assert natural_width > 0, f"Image {i+1} has naturalWidth of 0, indicating it might not be loaded or is broken."
            except Error as e:
                pytest.fail(f"Playwright error while checking image {i+1}: {e}")
            except AssertionError as ae:
                pytest.fail(f"Image loading assertion failed for image {i+1}: {ae}")

    except Error as e:
        take_screenshot(page, "FAIL_05_image_content_loading.png")
        pytest.fail(f"Playwright error in test_05_image_content_loading: {e}")

def test_06_responsive_design_basic_check(page: Page):
    """
    テストケース6: レスポンシブデザインの基本確認 (モバイルサイズ)
    異なるビューポートサイズでページレイアウトが崩れず、主要なコンテンツが適切に表示されることを確認する。
    """
    try:
        # 1. Playwrightのset_viewport_sizeを使ってビューポートを一般的なモバイルサイズに設定する。
        mobile_viewport = {"width": 375, "height": 667}
        page.set_viewport_size(mobile_viewport)
        print(f"Set viewport size to {mobile_viewport['width']}x{mobile_viewport['height']}.")

        # 2. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "06_responsive_mobile.png")

        # 3. ページタイトル、ナビゲーションメニュー、作品リスト、フッターなど、主要なコンテンツ要素が
        # 画面内に収まり、オーバーラップやレイアウトの崩れがないことを確認する。
        # (例: toBeVisible()で要素の存在確認)
        print("Asserting main elements are visible in mobile viewport.")
        expect(page.get_by_role("heading", name=re.compile(r"Art", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text("Tools: TouchDesigner")).to_be_visible() # 部分一致で存在確認
        expect(page.get_by_text("Smoke drifting over big cities")).to_be_visible()
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()

        # モバイル表示時にハンバーガーメニューが表示される場合があるため、ナビゲーションリンクの直接的な可視性ではなく、
        # サイト名やメインコンテンツが適切に表示されることを確認
        expect(page.get_by_role("link", name=re.compile(r"Asami K\.", re.IGNORECASE))).to_be_visible()

    except Error as e:
        take_screenshot(page, "FAIL_06_responsive_design_basic_check.png")
        pytest.fail(f"Playwright error in test_06_responsive_design_basic_check: {e}")

def test_07_page_title_and_meta_info(page: Page):
    """
    テストケース7: ページのタイトルとメタ情報の確認
    ページのタイトルタグが正しく設定されており、ブラウザタブや検索結果表示に適切な情報が提供されていることを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "07_page_title_check.png")

        # 2. ブラウザのページタイトル（<title>タグの内容）が「Art - Asami K.」など、
        # コンテンツに即した適切なものであることを確認する。
        print("Asserting page title contains 'Art - Asami K.'.")
        # to_have_title で正規表現を使って部分一致または厳密な一致を確認
        expect(page).to_have_title(re.compile(r"Art - Asami K\."))

    except Error as e:
        take_screenshot(page, "FAIL_07_page_title_and_meta_info.png")
        pytest.fail(f"Playwright error in test_07_page_title_and_meta_info: {e}")

def test_08_non_existent_url_behavior(page: Page):
    """
    テストケース8: 存在しないURLへのアクセス時の挙動
    サイトの存在しないURLにアクセスした場合に、適切なエラーページが表示されることを確認する。
    """
    try:
        # 1. https://asami.tokyo/non-existent-page のような、意図的に存在しないURLに直接アクセスする。
        print("Navigating to a non-existent URL.")
        response = page.goto("https://asami.tokyo/non-existent-page")
        # このテストケースでは意図的にエラーページを検証するため、
        # ページのロード状態が完全に"networkidle"にならない可能性があるため、wait_for_load_stateは追加しない。
        take_screenshot(page, "08_non_existent_url.png")

        # 2. HTTPステータスコードが404であることを確認する。
        print(f"Asserting HTTP status code is 404, got {response.status}.")
        assert response.status == 404, f"Expected status 404 for non-existent page, got {response.status}"

        # 3. ページに「404 Not Found」や「ページが見つかりません」といったエラーメッセージ、
        # またはカスタムエラーページが表示されることを確認する。
        print("Asserting '404' or 'Page Not Found' message is visible.")
        # `get_by_text`で部分一致または正規表現でエラーメッセージを探す
        expect(page.get_by_text(re.compile(r"404|Page Not Found|ページが見つかりません", re.IGNORECASE))).to_be_visible()
        # また、タイトルも確認できる
        expect(page).to_have_title(re.compile(r"404|Page Not Found|ページが見つかりません", re.IGNORECASE))

    except Error as e:
        take_screenshot(page, "FAIL_08_non_existent_url_behavior.png")
        pytest.fail(f"Playwright error in test_08_non_existent_url_behavior: {e}")

def test_09_no_console_errors(page: Page):
    """
    テストケース9: コンソールエラーの有無
    ページロード時や基本的な操作中に、開発者コンソールに重大なJavaScriptエラーやネットワークエラーが出力されないことを確認する。
    """
    console_errors = []

    def handle_console_message(msg):
        if msg.type == "error":
            console_errors.append(msg.text)
            print(f"Console error detected: {msg.text}")

    try:
        # 1. Playwrightのpage.on('console')イベントを購読し、エラーメッセージを監視するように設定する。
        page.on("console", handle_console_message)
        print("Console error listener set up.")

        # 2. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "09_no_console_errors.png")

        # 3. ページが完全にロードされるのを待つ。(goto()が完了すれば十分なことが多い)
        # 必要であれば additional networkidle または load state
        # 修正: 明示的にネットワークアイドル状態になるまで待機。
        page.wait_for_load_state("networkidle")

        # 期待される結果: ページロード中にコンソールにエラーレベルのメッセージが出力されないこと。
        print("Asserting no console errors were found.")
        assert not console_errors, f"Console errors found during page load: {'; '.join(console_errors)}"

    except Error as e:
        take_screenshot(page, "FAIL_09_no_console_errors.png")
        pytest.fail(f"Playwright error in test_09_no_console_errors: {e}")
    finally:
        # クリーンアップ: イベントリスナーを削除する
        page.remove_listener("console", handle_console_message)


def test_10_copyright_accuracy(page: Page):
    """
    テストケース10: Copyright情報の正確性
    フッターに表示されている著作権情報が正しく、特に年号が意図通りに「2025」と表示されていることを確認する。
    """
    try:
        # 1. https://asami.tokyo/art にアクセスする。
        page.goto("https://asami.tokyo/art")
        # 修正: ページが完全にロードされ、ネットワークアイドル状態になるまで待機
        page.wait_for_load_state("networkidle")
        expect(page).to_have_url(re.compile(r"asami\.tokyo/art"))
        take_screenshot(page, "10_copyright_accuracy.png")

        # 2. フッターの著作権表示テキストが「© 2025 Asami K.」と完全に一致することを確認する。
        # 厳密な判定を避ける制約があるため、get_by_textで特定のテキストを含む要素を探し、
        # to_contain_textでその内容を検証します。
        # この場合、完全な文字列が期待されるため、to_contain_textの引数に完全な文字列を渡します。
        print("Asserting footer copyright text is '© 2025 Asami K.'.")
        # get_by_text は部分一致をデフォルトとするため、"© 2025 Asami K." はそのテキストを含む要素を返す。
        # その要素に対して to_contain_text() を使い、実際のテキストが期待通りかを確認
        expect(page.get_by_text("© 2025 Asami K.")).to_contain_text("© 2025 Asami K.")

    except Error as e:
        take_screenshot(page, "FAIL_10_copyright_accuracy.png")
        pytest.fail(f"Playwright error in test_10_copyright_accuracy: {e}")