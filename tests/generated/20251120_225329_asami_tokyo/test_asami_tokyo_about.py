import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error, TimeoutError

# pytest-playwrightがインストールされていない環境でも動作するように、pageフィクスチャを定義
@pytest.fixture(scope="module")
def page():
    """
    PlaywrightのPageオブジェクトを提供するPytestフィクスチャ。
    テストモジュール全体で一度だけブラウザを起動し、ページを共有します。
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()  # Chromiumブラウザを起動
        page = browser.new_page()       # 新しいページを作成
        # デフォルトのビューポートサイズを設定
        page.set_viewport_size({"width": 1280, "height": 720})
        yield page                      # テストにページオブジェクトを渡す
        browser.close()                 # テスト完了後にブラウザを閉じる

# スクリーンショットを保存するディレクトリを定義 (テストファイルと同じディレクトリ)
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

def take_screenshot(page_obj: Page, name: str):
    """
    スクリーンショットを撮影し、指定されたファイル名で保存するヘルパー関数。
    """
    path = os.path.join(SAVE_DIR, name)
    try:
        page_obj.screenshot(path=path)
        print(f"Screenshot saved to: {path}")
    except Error as e:
        print(f"Failed to take screenshot {name}: {e}")

def test_01_about_page_content_display(page: Page):
    """
    Scenario 1: Aboutページの基本コンテンツ表示確認 (正常系)
    目的: Aboutページが正しくロードされ、主要なタイトル、セクション見出し、説明文が表示されることを確認する。
    """
    try:
        # 1. https://asami.tokyo/about にアクセスする。
        print(f"Navigating to {page.url} for test_01...")
        response = page.goto("https://asami.tokyo/about")

        # ページが正常にロードされたことを確認
        assert response.status == 200, f"Expected 200, got {response.status} for {page.url}"
        # URLが期待通りであることを確認
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        take_screenshot(page, "01_about_page_initial_load.png")

        # 2. ページのタイトルが "About" または関連するテキストを含むことを確認する。
        # タイトルはプリミティブ値なので標準のassertを使用
        assert "About" in page.title(), f"Page title should contain 'About', but was '{page.title()}'"

        # 3. h1/h2などの見出し「Art」と「Development」が存在し、表示されていることを確認する。
        # 'Art'見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("Art", re.IGNORECASE))).to_be_visible()
        # 'Development'見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("Development", re.IGNORECASE))).to_be_visible()

        # 4. 各セクションの主要な説明テキスト（例: "I create visuals...", "I am developing..."）が存在し、表示されていることを確認する。
        # 'Art'セクションの説明テキストが表示されていることを確認
        expect(page.get_by_text(re.compile("I create visuals and interactive experiences", re.IGNORECASE))).to_be_visible()
        # 'Development'セクションの説明テキストが表示されていることを確認
        expect(page.get_by_text(re.compile("I am developing web services", re.IGNORECASE))).to_be_visible()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_01_about_page_content_display: {e}")

def test_02_header_navigation_to_art_page(page: Page):
    """
    Scenario 2: ヘッダーナビゲーションリンク動作確認 (Artページへの遷移) (正常系)
    目的: ヘッダーのナビゲーションリンク（「Art」）が正しく機能し、対応するページへ遷移することを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_02...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. ヘッダーにある「Art」リンクをクリックする。
        # 'Art'リンクをクリックし、ナビゲーションが完了するのを待つ
        page.get_by_role("link", name=re.compile("Art", re.IGNORECASE)).click()

        # 3. URLが /art (または類似のArtページURL) に変更されることを確認する。
        # URLが'/art'を含むことを確認
        expect(page).to_have_url(re.compile(".*asami.tokyo/art.*"))

        take_screenshot(page, "02_navigated_to_art_page.png")

        # 4. Artページの主要なコンテンツ（例: 作品リストなど）が表示されることを確認する。
        # Artページの主要な見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("Art", re.IGNORECASE))).to_be_visible()
        # Artページの作品リストの存在を示すテキストが表示されていることを確認
        expect(page.get_by_text(re.compile("Generative Artworks", re.IGNORECASE))).to_be_visible()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_02_header_navigation_to_art_page: {e}")

def test_03_footer_navigation_to_contact_page(page: Page):
    """
    Scenario 3: フッター内部リンク動作確認 (Contactページへの遷移) (正常系)
    目的: フッターにある「contact」リンクが正しく機能し、対応するページへ遷移することを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_03...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. フッターにある「contact」リンクをクリックする。
        # フッター内の'Contact'リンクをクリックし、ナビゲーションが完了するのを待つ
        # locatorでfooterを指定することで、より堅牢にする
        page.locator("footer").get_by_role("link", name=re.compile("contact", re.IGNORECASE)).click()

        # 3. URLが /contact (または類似のContactページURL) に変更されることを確認する。
        # URLが'/contact'を含むことを確認
        expect(page).to_have_url(re.compile(".*asami.tokyo/contact.*"))

        take_screenshot(page, "03_navigated_to_contact_page.png")

        # 4. Contactページの主要なコンテンツが表示されていることを確認する。
        # Contactページの主要な見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("Contact", re.IGNORECASE))).to_be_visible()
        # Contactフォームの存在を示すテキストが表示されていることを確認
        expect(page.get_by_text(re.compile("Feel free to contact me", re.IGNORECASE))).to_be_visible()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_03_footer_navigation_to_contact_page: {e}")

def test_04_view_the_works_link(page: Page):
    """
    Scenario 4: 「View the Works.」リンクの動作確認 (外部サイトへの遷移) (正常系)
    目的: 「Art」セクションの「View the Works.」リンクが正しく外部サイトへ遷移することを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_04...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. 「View the Works.」リンクをクリックする。
        # 新しいページが開かれるイベントを待つ
        with page.context.wait_for_event("page") as page_info:
            page.get_by_role("link", name=re.compile("View the Works", re.IGNORECASE)).click()
        new_page = page_info.value

        # 3. 新しいタブ/ウィンドウが開かれることを確認する。
        # 新しいページがロードされるのを待つ (最大30秒)
        new_page.wait_for_load_state(timeout=30000)
        assert new_page is not None, "A new page should have opened."

        # 4. 新しいタブ/ウィンドウのURLが期待される外部サイトのURLと一致することを確認する。
        # URLが外部サイトのドメインを含むことを確認
        expect(new_page).to_have_url(re.compile(".*art.asami.tokyo.*"))
        
        take_screenshot(new_page, "04_view_the_works_external.png")
        new_page.close() # 新しいタブを閉じる

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_04_view_the_works_link: {e}")

def test_05_view_the_video_link(page: Page):
    """
    Scenario 5: 「View the Video. ( Youtube / Vimeo )」リンクの動作確認 (外部サイトへの遷移) (正常系)
    目的: 「Art」セクションの「View the Video. ( Youtube / Vimeo )」リンクが正しくYoutubeまたはVimeoのいずれかの動画サイトへ遷移することを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_05...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. 「View the Video. ( Youtube / Vimeo )」リンクをクリックする。
        # 新しいページが開かれるイベントを待つ
        with page.context.wait_for_event("page") as page_info:
            page.get_by_role("link", name=re.compile("View the Video", re.IGNORECASE)).click()
        new_page = page_info.value

        # 3. 新しいタブ/ウィンドウが開かれることを確認する。
        new_page.wait_for_load_state(timeout=30000)
        assert new_page is not None, "A new page should have opened."

        # 4. 新しいタブ/ウィンドウのURLがYoutubeまたはVimeoのいずれかのドメインを含むことを確認する。
        # URLがYoutubeまたはVimeoのドメインを含むことを確認
        assert re.search(r".*(youtube\.com|vimeo\.com).*", new_page.url()), \
            f"Expected URL to contain youtube.com or vimeo.com, got {new_page.url()}"

        take_screenshot(new_page, "05_view_the_video_external.png")
        new_page.close()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_05_view_the_video_link: {e}")

def test_06_view_the_ai_prompt_link(page: Page):
    """
    Scenario 6: 「View the AI Prompt.」リンクの動作確認 (外部サイトへの遷移) (正常系)
    目的: 「Art」セクションの「View the AI Prompt.」リンクがMediumなどのブログ記事サイトへ正しく遷移することを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_06...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. 「View the AI Prompt.」リンクをクリックする。
        with page.context.wait_for_event("page") as page_info:
            page.get_by_role("link", name=re.compile("View the AI Prompt", re.IGNORECASE)).click()
        new_page = page_info.value

        # 3. 新しいタブ/ウィンドウが開かれることを確認する。
        new_page.wait_for_load_state(timeout=30000)
        assert new_page is not None, "A new page should have opened."

        # 4. 新しいタブ/ウィンドウのURLがMediumまたは関連するブログサイトのURLを含むことを確認する。
        # 実際のサイトはnote.comのようです
        expect(new_page).to_have_url(re.compile(".*note.com.*"))

        take_screenshot(new_page, "06_view_the_ai_prompt_external.png")
        new_page.close()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_06_view_the_ai_prompt_link: {e}")

def test_07_view_the_code_link(page: Page):
    """
    Scenario 7: 「View the Code.」リンクの動作確認 (外部サイトへの遷移) (正常系)
    目的: 「Development」セクションの「View the Code.」リンクがGitHubなどのコードリポジトリサイトへ正しく遷移することを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_07...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. 「View the Code.」リンクをクリックする。
        with page.context.wait_for_event("page") as page_info:
            page.get_by_role("link", name=re.compile("View the Code", re.IGNORECASE)).click()
        new_page = page_info.value

        # 3. 新しいタブ/ウィンドウが開かれることを確認する。
        new_page.wait_for_load_state(timeout=30000)
        assert new_page is not None, "A new page should have opened."

        # 4. 新しいタブ/ウィンドウのURLがGitHubまたは関連するコードリポジトリサイトのURLを含むことを確認する。
        expect(new_page).to_have_url(re.compile(".*github.com.*"))

        take_screenshot(new_page, "07_view_the_code_external.png")
        new_page.close()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_07_view_the_code_link: {e}")

def test_08_all_external_links_status(page: Page):
    """
    Scenario 8: 全ての外部リンクのリンク切れチェック (異常系)
    目的: ページ内のすべての外部リンクが有効であり、リンク切れが発生していないことを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_08...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. ページ内のすべての<a>タグでhref属性がhttp://またはhttps://で始まるリンクを特定する。
        # 外部リンクのhref属性を全て取得
        external_links = page.locator("a[href^='http'], a[href^='https']").all()
        hrefs = []
        for link in external_links:
            href = link.get_attribute("href")
            # 既にテスト済みの内部リンクや、同じドメインへのリンクは除外
            if href and "asami.tokyo" not in href and "localhost" not in href: # 自身へのリンクは除外
                hrefs.append(href)
        
        # 重複するURLを避けるためsetに変換し、リストに戻す
        unique_hrefs = list(set(hrefs))
        
        print(f"Checking {len(unique_hrefs)} unique external links for status 200-399.")

        failed_links_info = []
        # 3. 各リンクのhref属性のURLに対し、HTTPリクエストを送信する。
        for href in unique_hrefs:
            try:
                # page.request (APIRequestContext) を使用して、ページ遷移なしでHTTPリクエストを送信
                # タイムアウトは10秒に設定
                response = page.request.get(href, timeout=10000)
                # 4. 各リクエストのHTTPステータスコードが200（OK）または3xx（リダイレクト）であることを確認する。
                if not (200 <= response.status <= 399):
                    failed_links_info.append(f"Link: {href}, Status: {response.status}")
                else:
                    print(f"  Link: {href}, Status: {response.status} (OK)")
            except TimeoutError:
                failed_links_info.append(f"Link: {href}, Error: Timeout after 10s")
            except Error as link_error:
                failed_links_info.append(f"Link: {href}, Error: {link_error}")

        # 全てのリンクが正常であることを確認
        assert not failed_links_info, \
            f"Some external links failed (total {len(failed_links_info)}):\n" + "\n".join(failed_links_info)

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_08_all_external_links_status: {e}")

def test_09_copyright_display(page: Page):
    """
    Scenario 9: コピーライト表示の確認 (正常系)
    目的: フッターに正しい著作権情報と現在の年号（または翌年の年号）が表示されていることを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_09...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        take_screenshot(page, "09_copyright_check.png")

        # 2. フッターエリアに「© 2025 Asami K.」というテキストが存在し、表示されていることを確認する。
        # 著作権表示のテキストがフッターに表示されていることを確認
        # to_contain_textを使用し、部分一致を許容
        expect(page.locator("footer")).to_contain_text("© 2025 Asami K.")
        
    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_09_copyright_display: {e}")

def test_10_responsive_design_mobile_viewport(page: Page):
    """
    Scenario 10: レスポンシブデザインの基本的な確認 (モバイルビューポート) (境界値/非機能)
    目的: スマートフォン相当のビューポートサイズで、Aboutページが適切に表示され、コンテンツの崩れがないことを確認する。
    """
    try:
        # 1. Aboutページにアクセスする。
        print(f"Navigating to {page.url} for test_10...")
        page.goto("https://asami.tokyo/about")
        expect(page).to_have_url(re.compile(".*asami.tokyo/about.*"))

        # 2. ブラウザのビューポートサイズをスマートフォン相当（例: 幅375px、高さ667px）に設定する。
        page.set_viewport_size({"width": 375, "height": 667})

        take_screenshot(page, "10_mobile_viewport_about_page.png")

        # 3. 主要なコンテンツ（例: Art/Developmentセクションの見出し、テキスト）が画面からはみ出さずに表示されていることを確認する。
        # Art見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("Art", re.IGNORECASE))).to_be_visible()
        # Development見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("Development", re.IGNORECASE))).to_be_visible()
        # 主要な説明テキストが表示されていることを確認
        expect(page.get_by_text(re.compile("I create visuals and interactive experiences", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile("I am developing web services", re.IGNORECASE))).to_be_visible()
        
        # モバイル環境でヘッダーメニューが折りたたまれている場合、メニューボタンが表示されているかを確認 (もしあれば)
        # 例: expect(page.get_by_role("button", name=re.compile("Menu", re.IGNORECASE))).to_be_visible()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Playwright error in test_10_responsive_design_mobile_viewport: {e}")