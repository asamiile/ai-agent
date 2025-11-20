import time
import os
import sys
from playwright.sync_api import sync_playwright
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.scrapers.yahoo import fetch_yahoo_links_playwright
from common.discord import send_discord_notification

API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def check_page_for_size(url: str) -> bool:
    prompt_template = """
    あなたはファッション選定AIです。
    以下のECサイトのページテキストを読み、この商品に「14Y」または「16Y」のサイズが
    利用可能かどうかを判断してください。
    
    「はい」（利用可能）か「いいえ」（利用不可）のみで回答してください。

    --- ページテキスト ---
    {page_text}
    ---
    回答: 
    """

    page_text = ""
    with sync_playwright() as p:
        # 安定動作のため headless=True 推奨
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page_text = page.locator("body").inner_text()
        except Exception as e:
            print(f"  [エラー] ページアクセス失敗: {url}")
            browser.close()
            return False
        finally:
            browser.close()

    if not page_text:
        return False

    try:
        prompt = prompt_template.format(page_text=page_text)
        response = model.generate_content(prompt)
        ai_answer = response.text.strip().lower()
        print(f"  [AI回答: {ai_answer}]")

        if "はい" in ai_answer:
            return True
        else:
            return False
    except Exception as e:
        print(f"  [エラー] API呼び出し失敗: {e}")
        return False

# --- メイン実行 ---
if __name__ == "__main__":
    
    BASE_SEARCH_URL = "https://shopping.yahoo.co.jp/search?p=%E3%83%87%E3%82%A3%E3%83%BC%E3%82%BC%E3%83%AB%E3%82%AD%E3%83%83%E3%82%BA+%E3%82%A2%E3%82%A6%E3%83%88%E3%83%AC%E3%83%83%E3%83%88"
    ITEMS_PER_PAGE = 30
    all_product_links = set()
    page_num = 1
    
    print("ステップ1：全商品リンクの収集を開始します...")
    
    while True: 
        start_index = (page_num - 1) * ITEMS_PER_PAGE + 1
        url_to_scrape = f"{BASE_SEARCH_URL}&b={start_index}"
        
        print(f"--- ページ {page_num} (b={start_index}) 収集 ---")
        links = fetch_yahoo_links_playwright(url_to_scrape)
        
        if not links:
            break
        
        print(f"  -> {len(links)}件発見")
        all_product_links.update(links)
        page_num += 1 
        time.sleep(1) 

    print(f"\nステップ1完了：合計 {len(all_product_links)} 件")
    
    print(f"\nステップ2：AIによるサイズ選定を開始します...")
    recommended_links = []

    for i, link in enumerate(all_product_links):
        print(f"\n--- チェック {i+1}/{len(all_product_links)} ---")
        print(f"  URL: {link}")
        
        if check_page_for_size(link):
            print(f"  ★ サイズあり！リストに追加")
            recommended_links.append(link)
        else:
            print(f"  - サイズなし")
        
        time.sleep(1)

    # --- ステップ3：通知 (★今回追加★) ---
    print("\n--- ステップ3：結果の通知 ---")
    if recommended_links:
        print(f"{len(recommended_links)}件のアイテムが見つかりました。Discordに送信します...")
        send_discord_notification(DISCORD_WEBHOOK_URL, recommended_links)
    else:
        print("通知対象のアイテムはありませんでした。")