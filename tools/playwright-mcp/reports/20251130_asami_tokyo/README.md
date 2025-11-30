# 探索テスト結果: asami.tokyo

## テスト概要

| 項目 | 内容 |
|------|------|
| テスト対象 | https://asami.tokyo/ |
| テスト日 | 2025年11月30日 |
| テストツール | Playwright MCP (Model Context Protocol) |
| テスト環境 | macOS / VS Code / GitHub Copilot |
| 結果 | ✅ 全ページ正常動作 |

## テスト結果サマリー

### テストしたページ

| ページ | URL | タイトル | 結果 |
|--------|-----|----------|------|
| Top/About | https://asami.tokyo/ | About \| asami.tokyo | ✅ 正常 |
| Art | https://asami.tokyo/art | Art \| asami.tokyo | ✅ 正常 |
| Camera | https://asami.tokyo/camera | Camera \| asami.tokyo | ✅ 正常 |
| Apps | https://asami.tokyo/apps | App \| asami.tokyo | ✅ 正常 |
| Law | https://asami.tokyo/law | Law \| asami.tokyo | ✅ 正常 |
| Contact | https://asami.tokyo/contact | Contact \| asami.tokyo | ✅ 正常 |

### 確認した機能

- [x] ナビゲーション - Top, Art, Camera, Appsの全リンクが正常動作
- [x] フッターリンク - About, law, contactのリンクが正常動作
- [x] 外部リンク - GitHub, Behance, Medium, YouTube, Vimeo, Buy Me A Coffeeへのリンク設定済み
- [x] 問い合わせフォーム - ドロップダウン選択、テキスト入力が正常機能
- [x] 画像カルーセル - Appsページのカルーセルが正常動作
- [x] レスポンシブデザイン - モバイルビュー（375x812）で正常表示
- [x] コンソールエラー - JavaScriptエラーなし

### 発見した問題

**なし** - すべての機能が正常に動作

---

## ページ詳細

### Top/Aboutページ

**URL**: https://asami.tokyo/

**内容**:
- プロフィール画像表示
- 名前: Asami K
- 紹介文: "I'm a front-end engineer and I use technology to express my art."
- Work Skill: TypeScript, JavaScript, Vue.js, Nuxt.js, Git, Figma, Photoshop
- Hobby Skill: Python, C++, Arduino, Unreal Engine, Blender, TouchDesigner, DaVinci Resolve

**外部リンク**:
- GitHub (https://github.com/asamiile)
- Behance (https://www.behance.net/asamiile)
- Medium (https://medium.com/@asamiile)
- YouTube (https://www.youtube.com/@asamiile)
- Vimeo (https://vimeo.com/asamiile)
- Buy Me A Coffee (https://www.buymeacoffee.com/asamiile)

---

### Artページ

**URL**: https://asami.tokyo/art

**ツール**: TouchDesigner, Photoshop, Midjourney, Runway

**コンテンツ**:
- Adobe Stock画像リンク多数
- Vimeo動画埋め込み
  - Fluctuation
  - Emit
  - Green Sandstorm
  - Blue Sandstorm
  - Sandstorm
- Behanceリンク（Clock Tower, whaleなど）

---

### Cameraページ

**URL**: https://asami.tokyo/camera

**ツール**: DJI Osmo Pocket 3, DJI Action 2, Google Pixel 8 Pro, DaVinci Resolve

**コンテンツ**:
- 動画コンテンツ（iframe埋め込み）
- Adobe Stock画像リンク
- YouTube動画（Arduino Uno Chroma LED）
- Behanceリンク

---

### Appsページ

**URL**: https://asami.tokyo/apps

**紹介アプリケーション**:

| アプリ名 | 説明 | 技術スタック | リンク |
|----------|------|--------------|--------|
| Global Event Timeline | 気象データ可視化 | TypeScript, Express, Canvas API | GitHub |
| Stat Dashboard | CSVデータ可視化ダッシュボード | Nuxt.js v3, Fast API, Pandas | Demo |
| Livesync | リアルタイム同期アプリ | Nuxt.js v3, Supabase, Vitest | Demo |
| Marketplace | デジタルアセットマーケットプレイス | Nuxt.js v3, Supabase, Resend | Demo |

**UI機能**: 画像カルーセル（正常動作確認済み）

---

### Lawページ（特定商取引法に基づく表記）

**URL**: https://asami.tokyo/law

**内容**:
- 販売業社の名称: Asami Kakuishi
- メールアドレス: info@asami.tokyo
- Medium / Adobeポリシーへのリンク

---

### Contactページ

**URL**: https://asami.tokyo/contact

**フォーム要素**:
| フィールド | タイプ | 選択肢/説明 |
|------------|--------|-------------|
| Inquiry Type | ドロップダウン | Job requests / Purchase of artwork / Other inquiries |
| Name | テキスト入力 | - |
| Email | テキスト入力 | - |
| Message | テキストエリア | - |
| Submit | ボタン | - |

**テスト内容**: フォームへの入力テストを実施（実際の送信は未実行）

---

## 技術的な観察事項

1. **フレームワーク**: Nuxt.jsで構築と推測（Appsページの使用技術から）
2. **デザイン**: ダークテーマ、ゴールド/イエローのアクセントカラー
3. **埋め込みコンテンツ**: Vimeo動画、YouTube動画、Adobe Stock画像
4. **ページタイトル**: 各ページで適切に設定（「ページ名 | asami.tokyo」形式）
5. **フッター**: © 2025 Asami K. と About / law / contactリンク
6. **レスポンシブ対応**: モバイルビューで適切にレイアウト調整

---

## テスト手順

### 使用したPlaywright MCPツール

| ツール | 用途 |
|--------|------|
| `browser_navigate` | 各ページへのアクセス |
| `browser_snapshot` | ページ構造の取得 |
| `browser_click` | ナビゲーション、ボタンクリック |
| `browser_type` | フォーム入力テスト |
| `browser_select_option` | ドロップダウン選択 |
| `browser_resize` | レスポンシブテスト（375x812） |
| `browser_take_screenshot` | スクリーンショット撮影 |
| `browser_console_messages` | コンソールエラー確認 |

### テストフロー

```
1. https://asami.tokyo/ にアクセス
2. ページ構造を確認（snapshot）
3. Artページに遷移 → 構造確認
4. Cameraページに遷移 → 構造確認
5. Appsページに遷移 → カルーセル操作テスト
6. Lawページに遷移 → 構造確認
7. Contactページに遷移 → フォーム入力テスト
8. Topページに戻る
9. コンソールエラー確認
10. レスポンシブテスト（モバイルサイズ）
11. スクリーンショット撮影
```

---

## スクリーンショット

| ビュー | ファイル |
|--------|----------|
| Appsページ（デスクトップ） | `screenshots/asami_tokyo_apps_page.png` |
| Topページ（モバイル） | `screenshots/asami_tokyo_mobile_view.png` |

---

## 結論

https://asami.tokyo/ は以下の点で品質が確認されました：

- ✅ すべてのナビゲーションが正常に動作
- ✅ 外部リンクが適切に設定
- ✅ フォーム機能が正常動作
- ✅ インタラクティブ要素（カルーセル）が動作
- ✅ レスポンシブデザインが機能
- ✅ JavaScriptエラーなし

**総合評価**: 問題なし
