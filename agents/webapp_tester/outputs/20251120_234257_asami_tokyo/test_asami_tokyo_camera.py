import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

# Base URL for the tests
BASE_URL = "https://asami.tokyo/camera"

# 修正箇所: `page`フィクスチャを分割し、より堅牢にする

@pytest.fixture(scope="module")
def browser_fixture():
    """
    Playwrightブラウザインスタンスをモジュールスコープで起動します。
    これにより、複数のページを開いてもブラウザの起動は一度で済みます。
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser_fixture):
    """
    各テスト関数に対して新しいページインスタンスを提供します。
    これにより、テスト間の状態の漏洩を防ぎ、独立性を保証します。
    デフォルトのデスクトップサイズにviewportを設定します。
    """
    page = browser_fixture.new_page(viewport={"width": 1280, "height": 720})
    yield page
    page.close() # 各テスト後にページを閉じ、次のテストのためにクリーンな状態を保証


def get_save_dir():
    """テストファイルと同じディレクトリを取得するヘルパー関数"""
    return os.path.dirname(os.path.abspath(__file__))

# --- テストケース ---

def test_01_page_load_and_main_elements_exist(page: Page):
    """
    目的: Webページが正しくロードされ、主要なナビゲーション、コンテンツ要素、
          フッターが表示されることを確認する。
    """
    try:
        # 1. ブラウザでURLにアクセス
        response = page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")
        assert response.status == 200, f"ページロードに失敗しました。ステータスコード: {response.status}"

        # スクリーンショットを保存（デバッグ用）
        save_dir = get_save_dir()
        page.screenshot(path=os.path.join(save_dir, "01_initial_load.png"))

        # 2. ページのタイトルが期待通りであることを確認
        # デバッグ: ページのタイトルを確認
        expect(page).to_have_title(re.compile("Camera|asami.tokyo", re.IGNORECASE))

        # 3. ヘッダーナビゲーションに「Camera」というテキストが表示されていることを確認
        # デバッグ: ヘッダーナビゲーションの'Camera'リンクの可視性を確認
        expect(page.get_by_role("link", name=re.compile("Camera", re.IGNORECASE))).to_be_visible()

        # 4. 「Tools」という見出しとその下に「DJI Osmo Pocket 3」などのツール名が表示されていることを確認
        # デバッグ: 'Tools'見出しの可視性を確認
        expect(page.get_by_role("heading", name=re.compile("Tools", re.IGNORECASE))).to_be_visible()
        # デバッグ: 'DJI Osmo Pocket 3'テキストの可視性を確認
        expect(page.get_by_text("DJI Osmo Pocket 3")).to_be_visible()

        # 5. コンテンツエリアに「Water's Edge」などのキャプションテキストが表示されていることを確認
        # デバッグ: 'Water\'s Edge'キャプションの可視性を確認
        expect(page.get_by_text("Water's Edge")).to_be_visible()

        # 6. フッターに「© 2025 Asami K.」という著作権表示と「About」リンクが表示されていることを確認
        # デバッグ: 著作権表示の可視性を確認
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()
        # デバッグ: 'About'リンクの可視性を確認
        expect(page.get_by_role("link", name=re.compile("About", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"テスト 'test_01_page_load_and_main_elements_exist' でPlaywrightエラーが発生しました: {e}")

def test_02_header_navigation_links_work(page: Page):
    """
    目的: ヘッダーナビゲーションの他のページへのリンクが正しく機能し、
          対応するページへ遷移することを確認する。
    """
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")

        links_to_test = {
            "Top": {"path": "/", "title_re": "Home|Top|asami.tokyo"},
            "Art": {"path": "/art", "title_re": "Art|作品"},
            "Apps": {"path": "/apps", "title_re": "Apps|アプリケーション"},
        }

        for link_name, expected in links_to_test.items():
            # デバッグ: ナビゲーションリンク '{link_name}' をクリック
            link_locator = page.get_by_role("link", name=re.compile(link_name, re.IGNORECASE))
            expect(link_locator).to_be_visible() # リンクが可視であることを確認
            link_locator.click()

            # デバッグ: URLが '{expected["path"]}' に遷移したことを確認
            expect(page).to_have_url(re.compile(f"asami.tokyo{expected['path']}", re.IGNORECASE))
            # デバッグ: ページタイトルが '{expected["title_re"]}' を含むことを確認
            expect(page).to_have_title(re.compile(expected['title_re'], re.IGNORECASE))

            # 次のテストのために元のページに戻る
            page.goto(BASE_URL, wait_until="domcontentloaded")
            # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
            # page.wait_for_load_state("networkidle")

    except Error as e:
        pytest.fail(f"テスト 'test_02_header_navigation_links_work' でPlaywrightエラーが発生しました: {e}")

def test_03_footer_navigation_links_work(page: Page):
    """
    目的: フッターの「About」、「law」、「contact」リンクが正しく機能し、
          対応するページへ遷移することを確認する。
    """
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")

        links_to_test = {
            "About": {"path": "/about", "title_re": "About|について"},
            "law": {"path": "/law", "title_re": "特定商取引|law"},
            "contact": {"path": "/contact", "title_re": "Contact|お問い合わせ"},
        }

        for link_name, expected in links_to_test.items():
            # デバッグ: フッターリンク '{link_name}' をクリック
            # フッターのリンクを探すため、より具体的なセレクタを使用
            link_locator = page.locator("footer").get_by_role("link", name=re.compile(link_name, re.IGNORECASE))
            expect(link_locator).to_be_visible() # リンクが可視であることを確認
            link_locator.click()

            # デバッグ: URLが '{expected["path"]}' に遷移したことを確認
            expect(page).to_have_url(re.compile(f"asami.tokyo{expected['path']}", re.IGNORECASE))
            # デバッグ: ページタイトルが '{expected["title_re"]}' を含むことを確認
            expect(page).to_have_title(re.compile(expected['title_re'], re.IGNORECASE))

            # 次のテストのために元のページに戻る
            page.goto(BASE_URL, wait_until="domcontentloaded")
            # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
            # page.wait_for_load_state("networkidle")

    except Error as e:
        pytest.fail(f"テスト 'test_03_footer_navigation_links_work' でPlaywrightエラーが発生しました: {e}")

def test_04_current_page_navigation_link_behavior(page: Page):
    """
    目的: 現在表示されているページへのナビゲーションリンク（例: 「Camera」）を
          クリックした際の挙動が期待通りであることを確認する。
    """
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")
        initial_url = page.url

        # デバッグ: 'Camera'ナビゲーションリンクをクリック
        camera_link_locator = page.get_by_role("link", name=re.compile("Camera", re.IGNORECASE))
        expect(camera_link_locator).to_be_visible()
        camera_link_locator.click()

        # デバッグ: URLが変更されていないことを確認
        expect(page).to_have_url(initial_url)
        # ページがリロードされていないことを確認するためのより高度なチェックも可能だが、
        # URLが変わらないことの確認で十分な場合が多い。

    except Error as e:
        pytest.fail(f"テスト 'test_04_current_page_navigation_link_behavior' でPlaywrightエラーが発生しました: {e}")

def test_05_image_content_display_and_visibility(page: Page):
    """
    目的: ページの主要コンテンツである画像が正しくロードされ、破損していないことを確認する。
    """
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")

        # デバッグ: ページ内のすべての画像要素が可視であることを確認
        image_locators = page.locator("img").all()
        assert len(image_locators) > 0, "ページに画像が見つかりません。"

        for i, img_locator in enumerate(image_locators):
            # デバッグ: {i+1}番目の画像が可視であることを確認
            expect(img_locator).to_be_visible(timeout=5000) # 画像ロード待ちのため少し長めのタイムアウト

    except Error as e:
        pytest.fail(f"テスト 'test_05_image_content_display_and_visibility' でPlaywrightエラーが発生しました: {e}")

def test_06_all_content_captions_exist(page: Page):
    """
    目的: 提供されたコンテンツ抜粋にある全ての画像キャプションが
          実際にページに表示されていることを確認する。
    """
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")

        captions_to_check = [
            "Water's Edge",
            "stream",
            "walk in sunset",
            "sunset coast",
            "Port Tower",
            "Palm Tree",
            "ship enters the port",
            "Sunset with bird",
        ]

        for caption in captions_to_check:
            # デバッグ: キャプション '{caption}' がページに存在し、可視であることを確認
            expect(page.get_by_text(caption)).to_be_visible()

    except Error as e:
        pytest.fail(f"テスト 'test_06_all_content_captions_exist' でPlaywrightエラーが発生しました: {e}")

def test_07_tools_section_text_accuracy(page: Page):
    """
    目的: 「Tools」セクションに記載されている情報が正確に表示されていることを確認する。
    """
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")

        # デバッグ: 'Tools'見出しが可視であることを確認
        tools_heading = page.get_by_role("heading", name=re.compile("Tools", re.IGNORECASE))
        expect(tools_heading).to_be_visible()

        tools_list_items = [
            "DJI Osmo Pocket 3",
            "DJI Action 2",
            "Google Pixel 8 Pro",
            "Davinci Resolve",
        ]

        # 見出しに続くテキストコンテンツの存在を確認
        for tool_name in tools_list_items:
            # デバッグ: ツール名 '{tool_name}' がページに存在し、可視であることを確認
            expect(page.get_by_text(tool_name)).to_be_visible()

    except Error as e:
        pytest.fail(f"テスト 'test_07_tools_section_text_accuracy' でPlaywrightエラーが発生しました: {e}")

def test_08_copyright_notice_accuracy(page: Page):
    """
    目的: フッターの著作権表示が正確に表示されていることを確認する。
    """
    try:
        page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")

        # デバッグ: 著作権表示テキストがページに存在し、可視であることを確認
        # to_contain_textを使用し、前後の空白や他の要素との結合を許容
        expect(page.locator("footer")).to_contain_text("© 2025 Asami K.")

    except Error as e:
        pytest.fail(f"テスト 'test_08_copyright_notice_accuracy' でPlaywrightエラーが発生しました: {e}")

def test_09_responsive_design_mobile_view(page: Page):
    """
    目的: ページがモバイルデバイスのビューポートでも正しく表示され、
          レイアウトが崩れていないことを確認する。
    """
    # 修正箇所: `page`フィクスチャが各テストで新しいページインスタンスを提供するようになったため、
    # ビューポートサイズを保存し、テスト終了後に元に戻す処理は不要になりました。
    # 各テストは常にデフォルトのviewportで開始されます。

    try:
        # デバッグ: ビューポートサイズをモバイル相当に設定
        page.set_viewport_size({"width": 375, "height": 667})
        response = page.goto(BASE_URL, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")
        assert response.status == 200, f"モバイルビューでのページロードに失敗しました。ステータスコード: {response.status}"

        # デバッグ: モバイルビューのスクリーンショットを保存
        save_dir = get_save_dir()
        page.screenshot(path=os.path.join(save_dir, "09_mobile_camera_page.png"))

        # モバイルビューでの主要要素の可視性を確認 (例: ヘッダーやフッターのコンテンツ)
        # ハンバーガーメニューなど、モバイル専用のナビゲーション要素があればその存在を確認
        # 今回のサイトではハンバーガーメニューはなさそうなので、基本的なヘッダー/フッターを確認
        # デバッグ: ヘッダー内のサイトタイトルまたはロゴが可視であることを確認
        expect(page.get_by_role("link", name=re.compile("Asami.tokyo", re.IGNORECASE))).to_be_visible()
        # デバッグ: フッターの著作権表示が可視であることを確認
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()

        # コンテンツが重なったり切れたりしていないことの自動確認は複雑なため、
        # スクリーンショットを保存し、手動または画像比較ツールで検証することを推奨。
        # ここでは基本的な要素の存在確認とスクリーンショットで代替。

    except Error as e:
        pytest.fail(f"テスト 'test_09_responsive_design_mobile_view' でPlaywrightエラーが発生しました: {e}")
    # finallyブロックは不要になったため削除
    # finally:
    #     page.set_viewport_size(initial_viewport_size)


def test_10_access_non_existent_url_path(page: Page):
    """
    目的: 存在しないURLパスにアクセスした場合に、
          適切なエラーページ（例: 404ページ）が表示されることを確認する。
    """
    try:
        non_existent_url = "https://asami.tokyo/camera/non-existent-page-12345"
        # デバッグ: 存在しないURL '{non_existent_url}' にアクセス
        response = page.goto(non_existent_url, wait_until="domcontentloaded")
        # サイトの特性によっては、より安定したロードを待つために以下の行を追加することも検討できます。
        # page.wait_for_load_state("networkidle")

        # デバッグ: HTTPステータスコードが404であることを確認
        assert response.status == 404, \
            f"Expected 404 status code, but got {response.status} for {non_existent_url}"

        # デバッグ: エラーメッセージがページに存在し、可視であることを確認
        # サイト固有のエラーメッセージを考慮して正規表現で部分一致
        expect(page.get_by_text(re.compile("Not Found|ページが見つかりません|エラー", re.IGNORECASE))).to_be_visible()

        # スクリーンショットを保存（デバッグ用）
        save_dir = get_save_dir()
        page.screenshot(path=os.path.join(save_dir, "10_404_page.png"))

    except Error as e:
        pytest.fail(f"テスト 'test_10_access_non_existent_url_path' でPlaywrightエラーが発生しました: {e}")
