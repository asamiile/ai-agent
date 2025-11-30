import os
import sys
from google import generativeai as genai

# プロジェクトルートのパス
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

API_KEY = os.environ.get("GOOGLE_AI_STUDIO_API_KEY")
if not API_KEY:
    print("Skipping: GOOGLE_AI_STUDIO_API_KEY is not set.")
    sys.exit(0)  # エラーにせず終了（ローカル誤爆防止）

genai.configure(api_key=API_KEY)  # type: ignore
model = genai.GenerativeModel('gemini-2.5-flash')  # type: ignore


def has_python_files(directory):
    """指定ディレクトリ内にPythonファイルが存在するかチェック（再帰的）"""
    if not os.path.exists(directory):
        return False
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith('.py') and not f.startswith('__'):
                return True
    return False


def read_repository_files():
    """リポジトリ内の主要なファイルを読み込む"""
    file_contents = ""
    ignore_list = {'.git', '.venv', '__pycache__', '.vscode', '.github', '.gemini', 'node_modules'}
    target_exts = {'.py', '.yml', '.json', '.txt'}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in ignore_list]

        for file in files:
            if file == 'README.md':
                continue

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


def update_readme(target_path, readme_type, context):
    """
    指定パスのREADME.mdを更新

    Args:
        target_path: READMEを作成するディレクトリのパス
        readme_type: "root" | "subdir"
        context: コードベースのコンテキスト
    """
    rel_path = os.path.relpath(target_path, PROJECT_ROOT)
    if rel_path == ".":
        rel_path = "root"

    print(f"Updating README for {rel_path}...")

    if readme_type == "root":
        prompt = f"""
あなたは優秀なエンジニアです。以下のコードベースを解析し、プロジェクトルートの README.md を作成してください。

## 要件
- 言語: 日本語

## README.mdの構成（この2つのセクションのみ）

### 1. プロジェクト概要
- プロジェクト全体の目的と概要を簡潔に説明
- 各エージェントの一覧と役割の要約（1〜2行程度）
- ディレクトリ構成図は記載しない（各ディレクトリのREADMEに記載するため）
- 各エージェントの詳細説明は記載しない（各ディレクトリのREADMEに記載するため）

### 2. セットアップと実行方法
- 前提条件（Python バージョン等）
- リポジトリのクローン
- 仮想環境の作成（macOS/LinuxとWindowsの両方のコマンド）
- 依存ライブラリのインストール
- 環境変数の設定（.env.exampleを.envにコピーして編集）
- Playwrightブラウザのインストール
- 実行方法の例

## 重要な制約
- マークダウンのテーブルは正しい形式で出力すること
- コードブロックは必ず 言語名 で囲むこと

## コードベース
{context}

## 出力
README.md の中身（Markdown）のみ
"""
    else:
        prompt = f"""
あなたは優秀なエンジニアです。以下のコードベースを解析し、{rel_path}/ ディレクトリの README.md を作成してください。

## 要件
- 言語: 日本語
- 対象: {rel_path}/ フォルダ内の README.md

## README.mdの構成
1. ディレクトリ名（見出し）
2. 概要: このディレクトリの目的と機能
3. ディレクトリ構成: フォルダ内のファイル/サブフォルダ構成
4. 各ファイル/モジュールの説明
5. 実行方法（該当する場合）: python {rel_path}/main.py など
6. 環境変数（該当する場合）

## 重要な制約
- マークダウンのテーブルは正しい形式で出力すること
- コードブロックは必ず 言語名 で囲むこと

## コードベース
{context}

## 出力
README.md の中身（Markdown）のみ
"""

    content = call_gemini(prompt)
    if content:
        readme_path = os.path.join(target_path, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  -> {rel_path}/README.md updated.")


def find_python_directories():
    """Pythonファイルが存在するサブディレクトリを探す（agents/, common/配下）"""
    target_dirs = []
    search_roots = ["agents", "common"]

    for search_root in search_roots:
        root_path = os.path.join(PROJECT_ROOT, search_root)
        if not os.path.exists(root_path):
            continue

        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            if os.path.isdir(item_path) and not item.startswith("__"):
                if has_python_files(item_path):
                    target_dirs.append(item_path)

        # search_root自体にPythonファイルがあれば追加
        direct_py_files = [f for f in os.listdir(root_path)
                          if f.endswith('.py') and not f.startswith('__')]
        if direct_py_files and root_path not in target_dirs:
            target_dirs.append(root_path)

    return target_dirs


if __name__ == "__main__":
    print("Reading repository...")
    context = read_repository_files()

    # ルートのREADME更新
    update_readme(PROJECT_ROOT, "root", context)

    # Pythonファイルが存在するディレクトリのREADME更新
    python_dirs = find_python_directories()
    for dir_path in python_dirs:
        update_readme(dir_path, "subdir", context)

    print("\nAll updates finished.")
