import requests
import json

def send_discord_notification(webhook_url: str, items: list[str]):
    """
    商品のURLリストを受け取り、Discordに通知を送る関数
    """
    if not items:
        print("通知対象のアイテムがありません。")
        return

    # メッセージの作成
    message = f"🎉 **DIESEL KIDS** ({len(items)}件)\n\n"
    
    # URLをリスト形式で追加
    for link in items:
        message += f"• {link}\n"
        
    # 最後に一言添える
    message += "\nチェック完了しました！✨"

    # Discordに送信
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print("✅ Discordへの通知に成功しました！")
    except Exception as e:
        print(f"❌ Discordへの通知に失敗しました: {e}")