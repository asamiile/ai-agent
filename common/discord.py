import requests
import json
from urllib.parse import urlparse, parse_qs

def extract_product_info(url: str) -> dict:
    """
    Yahoo!ショッピングのURLから商品情報を抽出する
    """
    try:
        parsed = urlparse(url)
        # 商品IDを取得（URLの最後の部分）
        path_parts = parsed.path.strip('/').split('/')
        product_id = path_parts[-1] if path_parts else "unknown"

        # 商品名をURLから推測（完全ではないが、何もないよりは良い）
        title = f"商品 {product_id[:20]}"

        return {
            "title": title,
            "url": url,
            "product_id": product_id
        }
    except Exception as e:
        print(f"  [警告] URL解析エラー: {e}")
        return {
            "title": "商品",
            "url": url,
            "product_id": "unknown"
        }

def send_discord_notification(webhook_url: str, items: list[str]):
    """
    商品のURLリストを受け取り、Embedsを使用してDiscordに通知を送る関数
    1メッセージあたり最大10個のembedsを送信し、それを超える場合は複数メッセージに分割
    """
    if not items:
        print("通知対象のアイテムがありません。")
        return

    # 10件ずつに分割（Discordの制限: 1メッセージあたり最大10 embeds）
    EMBEDS_PER_MESSAGE = 10
    total_items = len(items)

    for batch_index in range(0, total_items, EMBEDS_PER_MESSAGE):
        batch = items[batch_index:batch_index + EMBEDS_PER_MESSAGE]
        batch_num = (batch_index // EMBEDS_PER_MESSAGE) + 1
        total_batches = (total_items + EMBEDS_PER_MESSAGE - 1) // EMBEDS_PER_MESSAGE

        # Embedsの作成
        embeds = []
        for idx, url in enumerate(batch, start=1):
            product_info = extract_product_info(url)

            embed = {
                "title": f"🛍️ 商品 {batch_index + idx}",
                "url": url,
                "color": 0x00A0DC,  # DIESELブランドカラー（青系）
                "footer": {
                    "text": f"DIESEL KIDS アウトレット | {batch_index + idx}/{total_items}"
                }
            }
            embeds.append(embed)

        # メッセージコンテンツ（最初のバッチのみ）
        if batch_index == 0:
            content = f"🎉 **DIESEL KIDS アウトレット** - {total_items}件の商品が見つかりました！✨"
        else:
            content = f"📦 続き ({batch_num}/{total_batches})"

        # Discordに送信
        payload = {
            "content": content,
            "embeds": embeds
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print(f"✅ Discordへの通知に成功しました！ (バッチ {batch_num}/{total_batches})")
        except Exception as e:
            print(f"❌ Discordへの通知に失敗しました (バッチ {batch_num}): {e}")
            return  # エラーが発生したら以降の送信を中止

    print(f"✅ すべての通知が完了しました！ (合計 {total_items}件)")
