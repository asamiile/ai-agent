import time
from playwright.sync_api import sync_playwright
import sys

# ---------------------------------------------------------------------------
# ▼▼▼ ステップ1：1ページ分のリンクを収集する「関数（部品）」▼▼▼
# ---------------------------------------------------------------------------
def fetch_yahoo_links_playwright(target_url: str) -> set[str]:
    """
    Playwright単独でYahoo!ショッピングにアクセスし,
    「正解のセレクタ」で商品リンクを直接収集する（1ページ分）。
    
    Args:
        target_url: Yahoo!ショッピングの検索結果ページのURL

    Returns:
        重複を除去した、商品詳細ページのURLのセット
    """
    
    product_links = set()
    
    # 待機目標のセレクタ
    TARGET_SELECTOR = 'a[class*="ItemImageLink_SearchResultItemImageLink__link__"]'

    with sync_playwright() as p:
        # headless=True にすると裏側で動きます
        browser = p.chromium.launch(headless=True) 
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print(f"ブラウザで {target_url} にアクセスしています...")
            
            page.goto(
                target_url, 
                timeout=60000, 
                wait_until="domcontentloaded"
            )
            
            print(f"商品リンク（{TARGET_SELECTOR}）の読み込みを待機します...")
            
            page.wait_for_selector(TARGET_SELECTOR, timeout=30000)
            
            print("商品リンクの読み込みを確認しました。")
            
            link_elements = page.locator(TARGET_SELECTOR).all()

            if not link_elements:
                print("エラー: 待機後も商品リンクの要素が見つかりませんでした。")
                browser.close()
                return set()

            for link_element in link_elements:
                href = link_element.get_attribute("href")
                if href:
                    product_links.add(href)
                    
        except Exception as e:
            # 30秒待っても TARGET_SELECTOR が見つからなかった場合（＝最終ページ）
            # ここでエラーをキャッチし、空のセットを返す
            print(f"情報: 30秒待機しましたが、{TARGET_SELECTOR} が見つかりませんでした。")
            print(f"詳細: {e}")
            
        finally:
            browser.close()

    return product_links

# ---------------------------------------------------------------------------
# ▼▼▼ ステップ2：メインの実行部分（whileループ）▼▼▼
# (この 'if' ブロックが、上記の 'fetch_yahoo_links_playwright' 関数を呼び出す)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    
    # 検索クエリの基本URL
    BASE_SEARCH_URL = "https://shopping.yahoo.co.jp/search?p=%E3%83%87%E3%82%A3%E3%83%BC%E3%82%BC%E3%83%AB%E3%82%AD%E3%83%83%E3%82%BA+%E3%82%A2%E3%82%A6%E3%83%88%E3%83%AC%E3%83%83%E3%83%88"
    
    ITEMS_PER_PAGE = 30  # 1ページあたりのアイテム数
    
    # 収集した全リンクを保存するセット
    all_product_links = set()

    page_num = 1 # 1ページ目からスタート
    
    print("存在するすべてのページのリンクを収集します...")

    # while True: 処理が「止まれ(break)」と言うまで永遠にループ
    while True: 
        
        start_index = (page_num - 1) * ITEMS_PER_PAGE + 1
        url_to_scrape = f"{BASE_SEARCH_URL}&b={start_index}"
        
        print(f"\n--- ページ {page_num} (b={start_index}) の収集を開始 ---")
        
        # ★エラーが発生した箇所★
        # 上で定義した 'fetch_yahoo_links_playwright' 関数をここで呼び出す
        links_from_page = fetch_yahoo_links_playwright(url_to_scrape)
        
        # --- 停止条件 ---
        if not links_from_page:
            print(f"ページ {page_num} でリンクが見つかりませんでした。収集を終了します。")
            break # while True ループを抜ける
        
        print(f"ページ {page_num} で {len(links_from_page)} 件のリンクを発見。")
        all_product_links.update(links_from_page)
        
        page_num += 1 
        time.sleep(1) 

    # --- ループ終了 ---

    if all_product_links:
        print(f"\n--- 収集完了 ---")
        print(f"合計 {len(all_product_links)} 件のユニークな商品リンクが見つかりました。")
    else:
        print("商品リンクの収集に失敗しました。")