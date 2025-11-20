import os
import sys
import google.generativeai as genai

# プロジェクトルートのパス
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

API_KEY = os.environ.get("GOOGLE_AI_STUDIO_API_KEY")
if not API_KEY:
    print("Skipping: GOOGLE_AI_STUDIO_API_KEY is not set.")
    sys.exit(0) # エラーにせず終了（ローカル誤爆防止）

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def read_repository_files():
    """リポジトリ内の主要なファイルを読み込む"""
    file_contents = ""
    ignore_list = {'.git', '.venv', '__pycache__', '.vscode', '.github', '.gemini', 'package-lock.json', 'yarn.lock'}
    target_exts = {'.py', '.md', '.yml', '.json', '.txt'}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in ignore_list]

        for file in files:
            # README自体は読み込まない（生成ループ防止）
            if file == 'README.md': continue

            ext = os.path.splitext(file)[1]
            if ext in target_exts:
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, PROJECT_ROOT)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        file_contents += f"\n--- File: {rel_path} ---\n{f.read()}\n"
                except Exception:
                    pass
    return file_contents

def call_gemini(prompt):
    """Gemini APIを呼び出すヘルパー関数"""
    try:
        resp = model.generate_content(prompt)
        return resp.text.replace("```markdown", "").replace("```", "").strip()
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def update_root_readme(context):
    """ルートディレクトリのREADME.mdを更新"""
    print("Updating ROOT README.md...")
    prompt = f"""
    あなたは優秀なエンジニアです。以下のコードベースを解析し、プロジェクト全体の `README.md` を作成してください。

    ## 要件
    - 言語: 日本語
    - 対象: プロジェクトルートの `README.md`
    - 内容: プロジェクト全体の概要、ディレクトリ構成図、各エージェントの一覧と役割要約、共通セットアップ方法

    ## コードベース
    {context}

    ## 出力
    README.md の中身（Markdown）のみ
    """
    content = call_gemini(prompt)
    if content:
        with open(os.path.join(PROJECT_ROOT, "README.md"), "w", encoding="utf-8") as f:
            f.write(content)
        print("ROOT README updated.")

def update_agent_readmes(context):
    """agents/ 以下の各エージェントのREADME.mdを更新"""
    agents_dir = os.path.join(PROJECT_ROOT, "agents")

    # agentsフォルダ内のディレクトリを取得
    if not os.path.exists(agents_dir):
        return

    for agent_name in os.listdir(agents_dir):
        agent_path = os.path.join(agents_dir, agent_name)

        # ディレクトリかつ、__init__.py などを除外
        if os.path.isdir(agent_path) and not agent_name.startswith("__"):
            print(f"Updating README for agent: {agent_name}...")

            prompt = f"""
            あなたは優秀なエンジニアです。以下のコードベースを解析し、
            `agents/{agent_name}` ディレクトリ専用の `README.md` を作成してください。

            ## 要件
            - 言語: 日本語
            - 対象: エージェント `{agent_name}` のフォルダ内の `README.md`
            - 内容:
                - この特定のエージェントの機能詳細と目的
                - 実行方法（ルートディレクトリからの実行コマンド例: `python agents/{agent_name}/main.py` など）
                - 依存している共通モジュール (`common/`) への言及
                - ファイル構成の解説

            ## コードベース
            {context}

            ## 出力
            README.md の中身（Markdown）のみ
            """

            content = call_gemini(prompt)
            if content:
                with open(os.path.join(agent_path, "README.md"), "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Agent {agent_name} README updated.")

if __name__ == "__main__":
    print("Reading repository...")
    context = read_repository_files()

    # ルートのREADME更新
    update_root_readme(context)

    # 各エージェントのREADME更新
    update_agent_readmes(context)

    print("All updates finished.")
