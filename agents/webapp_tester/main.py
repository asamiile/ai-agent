import os
import sys
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# パス設定（commonモジュールなどが使えるように）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# プロンプトの読み込み
from agents.webapp_tester.prompts import PLANNING_PROMPT, CODING_PROMPT

# APIキー設定
API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
if not API_KEY:
    print("エラー: GOOGLE_AI_STUDIO_API_KEY が設定されていません。")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def fetch_page_content(url: str):
    """Playwrightでページにアクセスし、HTML構造を簡易化して取得する"""
    print(f"🌐 ページにアクセス中: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            # ページの読み込みを待つ（必要に応じて）
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                print("⚠️ networkidle timeout, proceeding with domcontentloaded...")
                page.wait_for_load_state("domcontentloaded")

            # テキストコンテンツを取得 (for AI prompt)
            text = page.evaluate("document.body.innerText")

            # リンクを取得 (for crawling)
            links = page.evaluate("""
                Array.from(document.querySelectorAll('a')).map(a => a.href)
            """)

            browser.close()
            return text, links
        except Exception as e:
            print(f"❌ ページ取得エラー: {e}")
            return "", []

def generate_test_code(url: str, page_content: str):
    """Geminiにテスト計画とコードを生成させる"""

    # 1. テスト計画の作成
    print("🤔 AIがテストシナリオを考案中...")
    plan_prompt = PLANNING_PROMPT.format(url=url) + f"\n\n## ページコンテンツ(抜粋)\n{page_content[:10000]}" # 文字数制限対策

    plan_response = model.generate_content(plan_prompt)
    test_plan = plan_response.text
    print(f"\n--- 📝 テスト計画 ---\n{test_plan}\n--------------------")

    # 2. テストコードの生成
    print("💻 AIがテストコードを実装中...")
    code_prompt = CODING_PROMPT.format(url=url, test_plan=test_plan)

    code_response = model.generate_content(code_prompt)
    code_text = code_response.text

    # MarkdownのコードブロックからPythonコードだけを抽出
    match = re.search(r"```python\n(.*?)\n```", code_text, re.DOTALL)
    if match:
        code = match.group(1)
    else:
        # ブロックがない場合はそのまま返す（またはエラー処理）
        code = code_text.replace("```python", "").replace("```", "")

    return code, test_plan

def save_test_file(code: str, url: str):
    """生成されたコードをファイルに保存する"""
    # URLからファイル名を生成（例: google.com -> test_google_com.py）
    domain = re.sub(r'^https?://', '', url).split('/')[0].replace('.', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 実行ごとのディレクトリを作成: tests/generated/{timestamp}_{domain}/
    save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests", "generated", f"{timestamp}_{domain}")
    os.makedirs(save_dir, exist_ok=True)

    filename = f"test_{domain}.py"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"✅ テストコードを保存しました: {filepath}")
    return filepath, save_dir

def run_test(filepath: str):
    """生成されたテストコードをpytestで実行する"""
    print(f"🚀 テストを実行中: {filepath}")
    import subprocess

    try:
        # pytestを実行 (タイムアウト120秒)
        result = subprocess.run(
            ["pytest", filepath],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as e:
        print(f"⏰ テスト実行がタイムアウトしました (120秒): {filepath}")
        return 124, e.stdout or "", (e.stderr or "") + "\nTimeoutExpired: Test execution exceeded 120 seconds."
    except Exception as e:
        print(f"❌ テスト実行中にエラーが発生しました: {e}")
        return 1, "", str(e)

def generate_report(url: str, plan: str, retcode: int, stdout: str, stderr: str, save_dir: str, filename: str = "report.md"):
    """テスト結果のレポート(Markdown)を作成する"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ PASS" if retcode == 0 else "❌ FAIL"

    # スクリーンショットファイルを検索
    screenshots = []
    try:
        all_files = os.listdir(save_dir)
        screenshots = sorted([f for f in all_files if f.endswith('.png')])
    except Exception as e:
        print(f"⚠️ スクリーンショットの検索中にエラー: {e}")

    # スクリーンショットセクションを生成
    screenshot_section = ""
    if screenshots:
        screenshot_section = "\n## 3. Screenshots\n\n"
        screenshot_section += f"**Total Screenshots:** {len(screenshots)}\n\n"
        for img in screenshots:
            # ファイル名をタイトルとして使用（拡張子を除く）
            title = img.replace('.png', '').replace('_', ' ').title()
            screenshot_section += f"### {title}\n"
            screenshot_section += f"![{title}](./{img})\n\n"

    report_content = f"""# Webapp Test Report

**Target URL:** {url}
**Date:** {timestamp}
**Status:** {status}

## 1. Test Plan
{plan}

## 2. Execution Result
**Return Code:** {retcode}

### Stdout
```text
{stdout}
```

### Stderr
```text
{stderr}
```
{screenshot_section}"""
    report_path = os.path.join(save_dir, filename)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"📝 レポートを作成しました: {report_path}")
    return report_path

def filter_links(base_url: str, links: list[str]) -> list[str]:
    """リンクをフィルタリングして、同一ドメインの有効なURLのみを返す（順序保持）"""
    unique_links = []
    seen = set()
    base_domain = re.sub(r'^https?://', '', base_url).split('/')[0]

    for link in links:
        # URLを正規化
        link = link.split('#')[0].rstrip('/')

        # 無効なリンクを除外
        if not link or link.startswith(('mailto:', 'tel:', 'javascript:')):
            continue

        # 同一ドメインかチェック
        if base_domain not in link:
            continue

        # 自分自身を除外
        if link == base_url.rstrip('/'):
            continue

        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    return unique_links

if __name__ == "__main__":
    # テストしたいURLを指定（引数でも可）
    start_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"

    # 実行ID（タイムスタンプ）を生成
    domain = re.sub(r'^https?://', '', start_url).split('/')[0].replace('.', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"{timestamp}_{domain}"

    # 保存先ディレクトリを作成
    base_save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests", "generated", run_id)
    os.makedirs(base_save_dir, exist_ok=True)

    # クローリングとテストの実行
    urls_to_process = [start_url]
    processed_urls = set()
    max_pages = 6 # トップページ + 5サブページ (順序保持で主要ページを優先)

    results = []

    print(f"🚀 テスト実行を開始します: {start_url}")
    print(f"📂 保存先: {base_save_dir}")

    while urls_to_process and len(processed_urls) < max_pages:
        current_url = urls_to_process.pop(0)
        if current_url in processed_urls:
            continue

        print(f"\n🔍 Processing: {current_url} ({len(processed_urls) + 1}/{max_pages})")

        content, links = fetch_page_content(current_url)

        if not content:
            print(f"❌ コンテンツの取得に失敗しました: {current_url}")
            continue

        # 新しいリンクをキューに追加（トップページの場合のみ）
        if len(processed_urls) == 0: # Only filter links from the initial page to find subpages
            valid_links = filter_links(start_url, links)
            # 重複を避けつつ追加
            for link in valid_links:
                if link not in processed_urls and link not in urls_to_process:
                    urls_to_process.append(link)
            print(f"🔗 発見したリンク: {len(valid_links)}件 (キューに追加: {len(urls_to_process)}件)")

        # テスト生成と実行
        code, test_plan = generate_test_code(current_url, content)
        if code:
            # ファイル名をURLに基づいて生成
            page_slug = re.sub(r'^https?://', '', current_url).rstrip('/').replace('/', '_').replace('.', '_').replace(':', '_')
            filename = f"test_{page_slug}.py"
            filepath = os.path.join(base_save_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"✅ テストコード保存: {filename}")

            # テスト実行
            retcode, stdout, stderr = run_test(filepath)
            status = "PASS" if retcode == 0 else "FAIL"

            # レポート生成
            report_filename = f"report_{page_slug}.md"
            report_path = generate_report(current_url, test_plan, retcode, stdout, stderr, base_save_dir, report_filename)

            results.append({
                "url": current_url,
                "status": status,
                "report": report_filename
            })

        processed_urls.add(current_url)

    # サマリーレポートの作成
    summary_path = os.path.join(base_save_dir, "summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"# Test Run Summary\n\n")
        f.write(f"**Target:** {start_url}\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| URL | Status | Report |\n")
        f.write("| --- | --- | --- |\n")
        for res in results:
            status_icon = "✅" if res["status"] == "PASS" else "❌"
            f.write(f"| {res['url']} | {status_icon} {res['status']} | [View Report]({res['report']}) |\n")

    print(f"\n🎉 全てのテストが完了しました。サマリー: {summary_path}")
