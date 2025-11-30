import os
import pytest
from playwright.sync_api import Page, expect, sync_playwright, Error, TimeoutError
import re # for regex in to_have_title and to_contain_text

# 5. pytest-playwrightがインストールされていない環境でも動作するように、
#    必ず `page` フィクスチャをコード内で定義してください。
@pytest.fixture(scope="module")
def page():
    """Provides a Playwright Page object for tests."""
    with sync_playwright() as p:
        # Launch browser in headless mode for CI, or non-headless for debugging
        # headless=True: ブラウザUIを表示しない (CI/CD向け)
        # headless=False: ブラウザUIを表示する (デバッグ向け)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # 一貫したビューポートサイズを設定
        page.set_viewport_size({"width": 1280, "height": 720})
        yield page
        browser.close()

# ベースURLを定数として定義
BASE_URL = "https://asami.tokyo/apps"

# スクリーンショット保存用のディレクトリ
# 11. スクリーンショットの保存: テストファイルと同じディレクトリに保存
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

def test_page_load_and_main_app_info(page: Page):
    """
    シナリオ1: ページが正常にロードされ、主要なアプリケーションのタイトルと説明文が正しく表示されることを確認します。
    """
    try:
        # 4. `page.goto("https://asami.tokyo/apps")` を必ず含めてください。
        # 9. `page.goto()` の後は、必ず期待するURLに遷移したことを確認してください。
        response = page.goto(BASE_URL)
        
        # Primitive value assertions use standard Python assert
        assert response.status == 200, f"Expected 200 OK status, got {response.status} for {BASE_URL}"
        # 9. 予期しないリダイレクトが発生する可能性があるため、アサーション前にURLをチェックしてください。
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: 期待するページタイトルに "Apps" が含まれているか確認
        # 1. 厳密な判定を避ける: テキスト判定には `exact=True` を絶対に使わないでください。
        #    Webサイトのテキストは頻繁に変更されるため、部分一致や正規表現を使ってください。
        expect(page).to_have_title(re.compile(r"Apps", re.IGNORECASE))

        # 3. デバッグのしやすさ: 主要アプリケーションのタイトルが表示されているか確認
        # 2. ロケータの優先順位: 1. `get_by_role` を使用 (nameは大文字小文字を区別しない設定)
        expect(page.get_by_role("heading", name="Global Event Timeline", level=3, exact=False)).to_be_visible()
        expect(page.get_by_role("heading", name="Stat Dashboard", level=3, exact=False)).to_be_visible()
        expect(page.get_by_role("heading", name="Livesync", level=3, exact=False)).to_be_visible()
        expect(page.get_by_role("heading", name="Marketplace", level=3, exact=False)).to_be_visible()

        # 3. デバッグのしやすさ: 各アプリケーションの説明文が表示されているか確認
        # 8. セレクタの注意点: `page.get_by_text()` を使用
        # 1. 厳密な判定を避ける: 正規表現で部分一致
        expect(page.get_by_text(re.compile(r"A video visualization that maps extreme weather event CSV data onto a world map.", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"A statistical dashboard app providing insights on tech stock trends.", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"A real-time collaborative code editor that supports multiple languages.", re.IGNORECASE))).to_be_visible()
        expect(page.get_by_text(re.compile(r"An e-commerce marketplace app for buying and selling products.", re.IGNORECASE))).to_be_visible()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_page_load_and_main_app_info' failed: {e}")

def test_stat_dashboard_demo_link(page: Page):
    """
    シナリオ2: "Stat Dashboard" アプリケーションのデモリンクが正しく機能し、対応するデモページへ遷移することを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: "Stat Dashboard" セクションのデモリンクをクリック
        # 2. ロケータの優先順位: `get_by_role` と `locator().filter()` の組み合わせで特定のリンクを特定
        # 8. セレクタの注意点: 部分一致が必要な場合は `filter(has_text="...")` を使用
        stat_dashboard_section = page.locator("section").filter(
            has=page.get_by_role("heading", name="Stat Dashboard", level=3, exact=False)
        )
        expect(stat_dashboard_section.get_by_role("link", name="Demo", exact=False)).to_be_visible()
        stat_dashboard_section.get_by_role("link", name="Demo", exact=False).click()

        # 3. デバッグのしやすさ: URLが `/demo` パスを含むものに遷移したことを確認
        # 1. 厳密な判定を避ける: 正規表現で部分一致
        expect(page).to_have_url(re.compile(r".*\/demo", re.IGNORECASE))

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_stat_dashboard_demo_link' failed: {e}")

def test_livesync_demo_link(page: Page):
    """
    シナリオ3: "Livesync" アプリケーションのデモリンクが正しく機能し、対応するデモページへ遷移することを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: "Livesync" セクションのデモリンクをクリック
        # 2. ロケータの優先順位: `get_by_role` と `locator().filter()` の組み合わせで特定のリンクを特定
        livesync_section = page.locator("section").filter(
            has=page.get_by_role("heading", name="Livesync", level=3, exact=False)
        )
        expect(livesync_section.get_by_role("link", name="Demo", exact=False)).to_be_visible()
        livesync_section.get_by_role("link", name="Demo", exact=False).click()

        # 3. デバッグのしやすさ: URLが `/demo` パスを含むものに遷移したことを確認
        # 1. 厳密な判定を避ける: 正規表現で部分一致
        expect(page).to_have_url(re.compile(r".*\/demo", re.IGNORECASE))

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_livesync_demo_link' failed: {e}")

def test_marketplace_demo_link(page: Page):
    """
    シナリオ4: "Marketplace" アプリケーションのデモリンクが正しく機能し、対応するデモページへ遷移することを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: "Marketplace" セクションのデモリンクをクリック
        # 2. ロケータの優先順位: `get_by_role` と `locator().filter()` の組み合わせで特定のリンクを特定
        marketplace_section = page.locator("section").filter(
            has=page.get_by_role("heading", name="Marketplace", level=3, exact=False)
        )
        expect(marketplace_section.get_by_role("link", name="Demo", exact=False)).to_be_visible()
        marketplace_section.get_by_role("link", name="Demo", exact=False).click()

        # 3. デバッグのしやすさ: URLが `/demo` パスを含むものに遷移したことを確認
        # 1. 厳密な判定を避ける: 正規表現で部分一致
        expect(page).to_have_url(re.compile(r".*\/demo", re.IGNORECASE))

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_marketplace_demo_link' failed: {e}")

def test_github_navigation_link(page: Page):
    """
    シナリオ5: グローバルナビゲーション（フッターまたはヘッダー）にある "GitHub" リンクが正しく機能し、
    開発者のGitHubプロフィールページへ遷移することを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: "GitHub" リンクをクリックし、新しいページ（タブ）が開かれるのを待つ
        # 2. ロケータの優先順位: 1. `get_by_role` を使用 (nameは大文字小文字を区別しない)
        # 8. セレクタの注意点: `name` はリンクのアクセシブル名と完全一致する必要がありますが、
        #    `get_by_role` の `name` はデフォルトで部分一致かつ大文字小文字を区別しないので、正規表現でより柔軟に。
        github_link = page.get_by_role("link", name=re.compile(r"GitHub", re.IGNORECASE))
        expect(github_link).to_be_visible()

        with page.expect_popup() as popup_info:
            github_link.click()
        new_page = popup_info.value

        # 3. デバッグのしやすさ: 新しいページのURLがGitHubのドメインを含むことを確認
        # 1. 厳密な判定を避ける: 正規表現で部分一致
        expect(new_page).to_have_url(re.compile(r".*github.com\/", re.IGNORECASE))

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_github_navigation_link' failed: {e}")

def test_apps_navigation_active_state(page: Page):
    """
    シナリオ6: 現在アクセスしているページが "Apps" ページであることを示すUI要素
    (例: アクティブ状態のリンク) が正しく表示されていることを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: "Apps" ナビゲーションリンクがアクティブ状態であることを確認
        # 2. ロケータの優先順位: `get_by_role` を使用
        # 多くのサイトではアクティブなリンクに `aria-current="page"` が設定されるため、これをチェック
        # または、CSSクラス `active` や `current` が付与される場合もある
        apps_link = page.get_by_role("link", name="Apps", exact=False)
        expect(apps_link).to_be_visible()
        expect(apps_link).to_have_attribute("aria-current", "page")

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_apps_navigation_active_state' failed: {e}")

def test_responsive_design_mobile_view(page: Page):
    """
    シナリオ7: ページが一般的なモバイルデバイスのビューポートサイズで適切に表示され、
    レイアウトが崩れていないことを確認します。主要な要素がビューポート内に存在することを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: ビューポートをモバイルサイズに設定
        # 7. 禁止事項: `page.viewport_size` の代わりに `page.set_viewport_size()` を使う
        page.set_viewport_size({"width": 375, "height": 667})

        # 11. スクリーンショットの保存: テストファイルと同じディレクトリに保存
        page.screenshot(path=os.path.join(SAVE_DIR, "apps-mobile-layout.png"), full_page=True)

        # 3. デバッグのしやすさ: モバイルビューでも主要なアプリケーションタイトルがビューポート内に見えるか確認
        # 7. 禁止事項: `to_be_visible()` は要素が見えないがスクロールすれば見える場合にも成功する可能性がある
        # `to_be_in_viewport()` は、要素がビューポート内に表示されていることを確認
        expect(page.get_by_role("heading", name="Global Event Timeline", level=3, exact=False)).to_be_in_viewport()
        expect(page.get_by_role("heading", name="Stat Dashboard", level=3, exact=False)).to_be_in_viewport()
        expect(page.get_by_role("heading", name="Livesync", level=3, exact=False)).to_be_in_viewport()
        # Marketplaceはスクロールが必要な場合もあるが、まずは visible であることを確認
        # より厳密には scroll_into_view_if_needed() でスクロールして to_be_in_viewport()
        expect(page.get_by_role("heading", name="Marketplace", level=3, exact=False)).to_be_visible()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_responsive_design_mobile_view' failed: {e}")

def test_app_icons_display(page: Page):
    """
    シナリオ8: 各アプリケーションのセクションに表示される関連アイコンや画像 (コンテンツ中の「lens」と記述されている視覚要素)
    が正しくロードされ、表示されていることを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: "Global Event Timeline" セクションに 'lens' アイコンが表示されているか確認
        # 8. セレクタの注意点: `page.locator("section").filter(has=...)` と `get_by_text()` を組み合わせて使用
        expect(page.locator("section").filter(
            has=page.get_by_role("heading", name="Global Event Timeline", level=3, exact=False)
        ).get_by_text("lens", exact=False)).to_be_visible()

        # 3. デバッグのしやすさ: "Stat Dashboard" セクションに 'lens' アイコンが表示されているか確認
        expect(page.locator("section").filter(
            has=page.get_by_role("heading", name="Stat Dashboard", level=3, exact=False)
        ).get_by_text("lens", exact=False)).to_be_visible()

        # 3. デバッグのしやすさ: "Livesync" セクションに 'lens' アイコンが表示されているか確認
        expect(page.locator("section").filter(
            has=page.get_by_role("heading", name="Livesync", level=3, exact=False)
        ).get_by_text("lens", exact=False)).to_be_visible()

        # 3. デバッグのしやすさ: "Marketplace" セクションに 'lens' アイコンが表示されているか確認
        expect(page.locator("section").filter(
            has=page.get_by_role("heading", name="Marketplace", level=3, exact=False)
        ).get_by_text("lens", exact=False)).to_be_visible()

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_app_icons_display' failed: {e}")


def test_tech_stack_display(page: Page):
    """
    シナリオ9: 各アプリケーションで利用されている技術スタックのリストが正しく表示されていることを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: "Stat Dashboard" の技術スタックが表示されているか確認
        # 2. ロケータの優先順位: 1. `get_by_role` と CSSセレクタの組み合わせ `locator('+ p')`
        # 7. 禁止事項: `to_have_text()` の代わりに `to_contain_text()` を使用
        # 1. 厳密な判定を避ける: 正規表現で部分一致
        stat_dashboard_tech_stack = page.get_by_role("heading", name="Stat Dashboard", level=3, exact=False).locator('+ p')
        expect(stat_dashboard_tech_stack).to_contain_text(
            re.compile(r"Nuxt.js v3, shadcn/vue, Tailwind CSS, Fast API, Pandas, NumPy, Scikit-learn, Vercel", re.IGNORECASE)
        )

        # 3. デバッグのしやすさ: "Livesync" の技術スタックが表示されているか確認
        livesync_tech_stack = page.get_by_role("heading", name="Livesync", level=3, exact=False).locator('+ p')
        expect(livesync_tech_stack).to_contain_text(
            re.compile(r"React, TypeScript, Next.js, WebSockets, Firebase, Express.js, MongoDB", re.IGNORECASE)
        )

        # 3. デバッグのしやすさ: "Marketplace" の技術スタックが表示されているか確認
        marketplace_tech_stack = page.get_by_role("heading", name="Marketplace", level=3, exact=False).locator('+ p')
        expect(marketplace_tech_stack).to_contain_text(
            re.compile(r"Vue.js, Nuxt.js, TypeScript, GraphQL, PostgreSQL, Stripe API", re.IGNORECASE)
        )

        # Global Event Timelineはシナリオの指示で技術スタックの記載が見当たらないため、ここではテストしない

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_tech_stack_display' failed: {e}")

def test_footer_copyright_info(page: Page):
    """
    シナリオ10: ページ下部のフッターに表示される著作権情報が最新かつ正しい内容であることを確認します。
    """
    try:
        page.goto(BASE_URL)
        expect(page).to_have_url(BASE_URL)

        # 3. デバッグのしやすさ: フッターの著作権表示を確認
        # 2. ロケータの優先順位: CSSセレクタ `footer` を使用
        # 7. 禁止事項: `to_have_text()` の代わりに `to_contain_text()` を使用
        # 1. 厳密な判定を避ける: 正規表現で部分一致
        expect(page.locator('footer')).to_contain_text(re.compile(r"© 2025 Asami K\.", re.IGNORECASE))

    except (Error, TimeoutError) as e:
        pytest.fail(f"Test 'test_footer_copyright_info' failed: {e}")