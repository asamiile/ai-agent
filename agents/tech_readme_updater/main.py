import os
import sys
import google.generativeai as genai

# プロジェクトルートのパス
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# APIキーの設定 (GitHub ActionsのSecretsから読み込む)
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    print("Skipping: GOOGLE_API_KEY is not set.")
    sys.exit(0) # エラーにせず終了（ローカル誤爆防止）

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def read_repository_files():
    """リポジトリ内の主要なファイルを読み込む"""
    file_contents = ""
    # 除外するディレクトリ・ファイル
    ignore_list = {'.git', '.venv', '__pycache__', '.vscode', '.github', '.gemini', 'package-lock.json', 'yarn.lock'}
    # 読み込む拡張子
    target_exts = {'.py', '.md', '.yml', '.json', '.txt'}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # 除外ディレクトリを探索対象から外す
        dirs[:] = [d for d in dirs if d not in ignore_list]

        for file in files:
            if file == 'README.md': continue # 自分自身は読まない

            ext = os.path.splitext(file)[1]
            if ext in target_exts:
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, PROJECT_ROOT)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        file_contents += f"\n--- File: {rel_path} ---\n{f.read()}\n"
                except Exception:
                    pass # 読み込めないファイルはスキップ
    return file_contents

def generate_readme(context):
    """AIにREADMEを生成させる"""
    prompt = f"""
    あなたは優秀なエンジニアです。以下のコードベースを解析し、プロジェクトの `README.md` を作成してください。

    ## 要件
    - 言語: 日本語
    - 内容: プロジェクト概要、ディレクトリ構成図、各エージェントの役割、セットアップ/実行方法
    - 既存の情報を網羅しつつ、コードの実態に合わせて最新化すること

    ## コードベース
    {context}

    ## 出力
    README.md の中身（Markdown）のみを出力してください。
    """
    try:
        resp = model.generate_content(prompt)
        return resp.text.replace("```markdown", "").replace("```", "").strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Generating README...")
    context = read_repository_files()
    readme = generate_readme(context)

    if readme:
        with open(os.path.join(PROJECT_ROOT, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme)
        print("README.md updated successfully.")
    else:
        sys.exit(1)
