import os
import re
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error

# ベースURLを定数として定義
BASE_URL = "https://asami.tokyo/law"
TOP_URL = "https://asami.tokyo/"
CONTACT_PATH_REGEX = r"/contact" # contact リンクのパス (正規表現で部分一致を許容)

# pytest-playwrightがインストールされていない環境でも動作するように、pageフィクスチャを定義
@pytest.fixture(scope="module")
def page():
    """
    PlaywrightのPageオブジェクトを提供するpytestフィクスチャ。
    テストモジュール全体で一度だけブラウザを起動し、ページインスタンスを作成・提供します。
    """
    with sync_playwright() as p:
        # headless=Trueでヘッドレスモードで実行 (デフォルト)
        # GUIを表示したい場合は headless=False に設定
        browser = p.chromium.launch()
        page = browser.new_page()
        # オプションでviewportサイズを設定することも可能だが、今回は不要な制約があるためスキップ
        # page.set_viewport_size({"width": 1280, "height": 720})
        yield page
        browser.close()

def test_1_basic_page_info(page: Page):
    """
    ページの基本情報（URL、タイトル、主要見出し）を確認するテスト。
    """
    try:
        # 1. ブラウザでURLにアクセス
        response = page.goto(BASE_URL)

        # デバッグ: HTTPレスポンスステータスを確認
        assert response.status == 200, f"Expected 200, got {response.status} for {BASE_URL}"

        # デバッグ: ページのURLが期待通りであることを確認
        assert page.url == BASE_URL, f"Expected URL {BASE_URL}, but got {page.url}"

        # デバッグ: ページのタイトルに「特定商取引法に基づく表記」が含まれていることを確認
        expect(page).to_have_title(re.compile("特定商取引法に基づく表記"))

        # デバッグ: メインの見出し「特定商取引法に基づく表記」が表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("特定商取引法に基づく表記", re.IGNORECASE))).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_1_basic_page_info: {e}")

def test_2_fixed_company_info(page: Page):
    """
    販売業者名および運営統括責任者名が正確に表示されていることを確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: 「販売業社の名称」の項目に「Asami Kakuishi」が表示されていることを確認
        # ロケータの優先順位を考慮し、CSSセレクタとhas_textを組み合わせる
        expect(page.locator("dt:has-text('販売業社の名称') + dd")).to_contain_text("Asami Kakuishi")

        # デバッグ: 「運営統括責任者」の項目に「Asami Kakuishi」が表示されていることを確認
        expect(page.locator("dt:has-text('運営統括責任者') + dd")).to_contain_text("Asami Kakuishi")

    except Error as e:
        pytest.fail(f"Playwright error in test_2_fixed_company_info: {e}")

def test_3_disclosure_request_info(page: Page):
    """
    所在地および電話番号に関する開示請求の旨が正確に表示されていることを確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: 「所在地」の項目に「請求があった場合は遅滞なく開示します」が表示されていることを確認
        expect(page.locator("dt:has-text('所在地') + dd")).to_contain_text("請求があった場合は遅滞なく開示します")

        # デバッグ: 「電話番号」の項目に「請求があった場合は遅滞なく開示します」が表示されていることを確認
        expect(page.locator("dt:has-text('電話番号') + dd")).to_contain_text("請求があった場合は遅滞なく開示します")

    except Error as e:
        pytest.fail(f"Playwright error in test_3_disclosure_request_info: {e}")

def test_4_email_address_and_mailto_link(page: Page):
    """
    連絡先メールアドレスが正しく表示され、mailtoリンクが設定されていることを確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: 「info@asami.tokyo」のテキストが表示され、その要素がmailtoリンクであることを確認
        # get_by_role('link', name='...') はアクセシブル名と完全一致するため、この場合はそのまま使用
        expect(page.get_by_role("link", name="info@asami.tokyo")).to_have_attribute("href", "mailto:info@asami.tokyo")

    except Error as e:
        pytest.fail(f"Playwright error in test_4_email_address_and_mailto_link: {e}")

def test_5_exchange_and_return_policy(page: Page):
    """
    交換および返品に関するポリシー情報が正しく表示されていることを確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: 「交換および返品（返金ポリシー）」の見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("交換および返品（返金ポリシー）", re.IGNORECASE))).to_be_visible()

        # デバッグ: 「Mediumの場合：Medium membershipに基づきます」のテキストが表示されていることを確認
        expect(page.get_by_text("Mediumの場合：Medium membershipに基づきます")).to_be_visible()

        # デバッグ: 「Behanceの場合：Adobeのポリシーに基づきます」のテキストが表示されていることを確認
        expect(page.get_by_text("Behanceの場合：Adobeのポリシーに基づきます")).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_5_exchange_and_return_policy: {e}")

def test_6_accepted_payment_methods(page: Page):
    """
    受け付け可能な決済手段に関する情報が正しく表示されていることを確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: 「受け付け可能な決済手段」の見出しが表示されていることを確認
        expect(page.get_by_role("heading", name=re.compile("受け付け可能な決済手段", re.IGNORECASE))).to_be_visible()

        # デバッグ: 「Mediumの場合：Mediumに基づきます」のテキストが表示されていることを確認
        expect(page.get_by_text("Mediumの場合：Mediumに基づきます")).to_be_visible()

        # デバッグ: 「Behanceの場合：Adobeに基づきます」のテキストが表示されていることを確認
        expect(page.get_by_text("Behanceの場合：Adobeに基づきます")).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_6_accepted_payment_methods: {e}")

def test_7_footer_navigation_links(page: Page):
    """
    フッターの主要なナビゲーションリンクの存在と代表的なリンクの遷移を確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: フッター内の全ての指定されたリンクが表示されていることを確認
        link_names = ["Top", "Art", "Camera", "Apps", "About", "law", "contact"]
        for name in link_names:
            expect(page.get_by_role("link", name=re.compile(name, re.IGNORECASE))).to_be_visible(
                f"Link '{name}' should be visible in the footer."
            )

        # デバッグ: 「Top」リンクをクリック後、URLがトップページに遷移することを確認
        top_link = page.get_by_role("link", name=re.compile("Top", re.IGNORECASE))
        top_link.click()
        expect(page).to_have_url(TOP_URL)

        # 元のページに戻る（次のアサーションのため）
        page.goto(BASE_URL)

        # デバッグ: 「contact」リンクのhref属性が期待されるパスと一致することを確認
        expect(page.get_by_role("link", name=re.compile("contact", re.IGNORECASE))).to_have_attribute("href", re.compile(CONTACT_PATH_REGEX))

    except Error as e:
        pytest.fail(f"Playwright error in test_7_footer_navigation_links: {e}")

def test_8_footer_copyright_notice(page: Page):
    """
    著作権表示が正しく表示されていることを確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: 「© 2025 Asami K.」のテキストがフッターに表示されていることを確認
        expect(page.get_by_text("© 2025 Asami K.")).to_be_visible()

    except Error as e:
        pytest.fail(f"Playwright error in test_8_footer_copyright_notice: {e}")

def test_9_footer_law_link_current_page(page: Page):
    """
    現在閲覧中の「law」ページにおいて、フッターの「law」リンクの挙動を確認するテスト。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: 「law」リンクのhref属性が現在のURLパスと一致することを確認
        law_link = page.get_by_role("link", name=re.compile("law", re.IGNORECASE))
        expect(law_link).to_have_attribute("href", re.compile(r"/law"))

        # デバッグ: 「law」リンクをクリック後もページのURLが現在のURLのままであることを確認
        law_link.click()
        expect(page).to_have_url(BASE_URL) # リロードされる可能性はあるが、他のページには遷移しない

    except Error as e:
        pytest.fail(f"Playwright error in test_9_footer_law_link_current_page: {e}")

def test_10_visual_integrity_screenshot(page: Page):
    """
    ページ全体の視覚的な整合性を確認するため、スクリーンショットを保存するテスト。
    これはビジュアルリグレッションテストの第一歩として、基準画像を手動で確認するために使用できます。
    """
    try:
        page.goto(BASE_URL)

        # デバッグ: ページ全体のスクリーンショットを保存
        # 指示に従い、テストファイルと同じディレクトリに保存します
        save_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_path = os.path.join(save_dir, "law_page_full_screenshot.png")
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to: {screenshot_path}")

        # Note: Playwrightの `expect(page).to_have_screenshot()` は
        # 自動的なビジュアルリグレッションテストフレームワークの一部であり、
        # 通常は `__snapshots__` ディレクトリに画像を保存します。
        # 今回の指示「必ずテストファイルと同じディレクトリ」に従うため、
        # `page.screenshot()` を使用し、テストの目的を「スクリーンショット保存」と解釈します。
        # 実際のビジュアルリグレッションテストでは、ベースライン画像との比較ロジックが必要です。

    except Error as e:
        pytest.fail(f"Playwright error in test_10_visual_integrity_screenshot: {e}")
