import sys, os, hashlib, subprocess, datetime, requests, time
from colorama import Fore, init

init(autoreset=True)
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
    
    # ၁။ သိမ်းထားတဲ့ Key ရှိမရှိ စစ်မယ်
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            saved_key = f.read().strip()
            for i in range(0, 366):
                check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                if saved_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
                    print(f"{Fore.GREEN}[✔] AUTO-LOGIN SUCCESS!")
                    return True

    # ၂။ သိမ်းထားတဲ့ Key မရှိရင် ဒါမှမဟုတ် Key အသစ်ထည့်ဖို့အတွက် Input တောင်းမယ်
    os.system('clear')
    print(f"{Fore.CYAN}--- AHO MASTER BYPASS (YUTA) ---")
    print(f"DEVICE ID: {Fore.YELLOW}{uid}")
    
    user_key = input(f"{Fore.WHITE}\nENTER YOUR LICENSE KEY: ").strip()

    for i in range(0, 366):
        check_date = (now + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if user_key == hashlib.md5(f"{uid}|{check_date}|{SALT}".encode()).hexdigest()[:12].upper():
            with open(KEY_FILE, "w") as f: f.write(user_key)
            print(f"{Fore.GREEN}[✔] KEY ACTIVATED!")
            return True
    
    # Key မှားမှသာ Error ပြပြီး ပိတ်မယ်
    print(f"{Fore.RED}[X] INVALID KEY!")
    return False

if __name__ == "__main__":
    if check_access():
        print(f"{Fore.BLUE}[*] Initializing Engine...")
        try:
            sys.path.append(os.getcwd())
            import core
            core.IS_LIFETIME = True
            core.run_bg_bypass() if hasattr(core, 'run_bg_bypass') else core.main()
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}")
    else:
        # ဒီနေရာမှာ sys.exit() လုပ်ပေးရမယ်
        sys.exit()
