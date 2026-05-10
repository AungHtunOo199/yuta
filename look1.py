import sys, os, hashlib, subprocess, datetime, requests, time
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
    print(f"{Fore.CYAN}--- AHO MASTER BYPASS (YUTA) ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    
    u_key = input(f"\n{Fore.WHITE}ENTER LICENSE KEY: ").strip()
    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if u_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f: f.write(u_key)
            return True
    return False

# --- ENGINE START ---
def start_bypass():
    os.system('clear')
    print(f"{Fore.BLUE}[*] Initializing Yuta Core Engine...")
    
    # လက်ရှိ yuta folder လမ်းကြောင်းကို အတိအကျ သတ်မှတ်မယ်
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    
    try:
        import core
        core.IS_LIFETIME = True
        
        # အစ်ကို့ရဲ့ Direct Bypass Engine ကို တိုက်ရိုက်နှိုးမယ်
        if hasattr(core, 'run_bg_bypass'):
            core.run_bg_bypass()
        else:
            core.main()
            
    except Exception as e:
        print(f"{Fore.RED}[✘] Engine Error: {e}")
        print(f"{Fore.YELLOW}[!] Make sure 'core.so' is in the same folder.")

if __name__ == "__main__":
    if check_access():
        start_bypass()
    else:
        print(f"{Fore.RED}[✘] ACCESS DENIED!")
        sys.exit()
