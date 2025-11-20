# Access Deniedになるため、ZOZOにアクセスすることは困難

import time
# playwright_stealth はもう使いません
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_product_links_playwright(target_url: str) -> set[str]:
    base_url = "https://zozo.jp"
    product_links = set()

    with sync_playwright() as p:
        
        # 目視確認のためFalseのまま
        browser = p.chromium.launch(headless=False) 
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # --- ▼▼▼ ここを修正 ▼▼▼ ---
            # 'playwright_stealth' を削除し、
            # 'page.goto' の *前* に、自動化検知を回避するJavaScriptを挿入します。
            print("自動化検知（webdriver）を無効化しています...")
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            # --- ▲▲▲ ここまで修正 ▲▲▲ ---

            print(f"ブラウザで {target_url} にアクセスしています...")
            
            page.goto(
                target_url, 
                timeout=60000, 
                wait_until="domcontentloaded" 
            )
            
            page.wait_for_timeout(5000) # 5秒待機

            html_content = page.content()
            
            soup = BeautifulSoup(html_content, "html.parser")
            
            item_cards = soup.find_all("div", class_="c-items_item")
            
            if not item_cards:
                # Access Denied ページに来た場合も、商品カードは見つからない
                page_text = soup.get_text()
                if "Access Denied" in page_text:
                    print("エラー: 'Access Denied' が検出されました。ステルスが失敗しました。")
                else:
                    print("エラー: 商品カードが見つかりませんでした。サイトの構造が変わったか、読み込みに失敗した可能性があります。")
                browser.close()
                return set()

            for card in item_cards:
                link_tag = card.find("a", href=True)
                if link_tag:
                    relative_path = link_tag["href"]
                    full_url = urljoin(base_url, relative_path)
                    product_links.add(full_url)
                    
        except Exception as e:
            print(f"エラー: Playwrightでの処理中にエラーが発生しました。 {e}")
            
        finally:
            browser.close()

    return product_links

# --- メインの実行部分 ---
if __name__ == "__main__":
    
    TARGET_BRAND_URL = "https://zozo.jp/brand/dieselkids/"
    
    print(f"{TARGET_BRAND_URL} から商品リンクを収集します (Playwright + 手動ステルス使用)...")
    
    links = fetch_product_links_playwright(TARGET_BRAND_URL)
    
    if links:
        print(f"\n合計 {len(links)} 件のユニークな商品リンクが見つかりました：")
        for i, link in enumerate(links):
            print(f"{i+1}: {link}")
    else:
        print("商品リンクの収集に失敗しました。")