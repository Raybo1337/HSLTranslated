import base64
import datetime
import hashlib
import json
import math
import requests
import logger
import threading

class HCaptchaSolver:
    def __init__(this, proxy, site_key, host):
        this.proxy = proxy
        this.site_key = site_key
        this.host = host
        
        this.headers = {
            "Host": "hcaptcha.com",
            "Connection": "keep-alive",
            "sec-ch-ua": 'Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92',
            "Accept": "application/json",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Discord/145.0 (iPhone; iOS 16.0.2; Scale/3.00)",
            "Content-type": "application/json; charset=utf-8",
            "Origin": "https://newassets.hcaptcha.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://newassets.hcaptcha.com/",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def ndata(this, req: str) -> str:
        try:
            e = "0123456789/:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

            req = req.split(".")
            
            header = json.loads(base64.b64decode(req[0] + "=======").decode("utf-8"))
            payload = json.loads(base64.b64decode(req[1] + "=======").decode("utf-8"))
            raw = {"header": req[0], "payload": req[1], "signature": req[2]}
            req = {"header": header, "payload": payload, "raw": raw}

            def _i(aa):
                for i in range(len(aa) - 1, -1, -1):
                    if aa[i] < len(e) - 1:
                        aa[i] += 1
                        return True
                    aa[i] = 0
                return False

            def _st(aa):
                return ''.join(e[n] for n in aa)

            def _ch(l, pr):
                x = hashlib.sha1(pr.encode())
                x2 = x.digest()
                x3 = []
                
                for i in range(l):
                    fart = x2[math.floor(i / 8)] >> i % 8 & 1
                    x3.append(fart)

                return (x3[0] == 0 and x3.index(1) >= l - 1) or (1 not in x3)

            def _obtain():
                for length in range(25):
                    aa = [0] * length
                    while _i(aa):
                        pm = req["payload"]["d"] + "::" + _st(aa)
                        if _ch(req["payload"]["s"], pm):
                            return _st(aa)

            res = _obtain()
            return f'1:{req["payload"]["s"]}:{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}:{req["payload"]["d"]}::{res}'

        except Exception as e:
            #print(e)
            return False
    
    def reqdata(this):
        try:
            r = requests.get(
                f"https://hcaptcha.com/checksiteconfig?host={this.host}&sitekey={this.site_key}&sc=1&swa=1",
                proxies={"http": f"http://{this.proxy}", "https": f"http://{this.proxy}"}
            )
            if r.json()["pass"]:
                return r.json()["c"]
            else:
                return False
        except:
            return False
    
instance =  HCaptchaSolver(None, "4c672d35-0701-42b2-88c3-78380b0db560", host="discord.com")
    
def start():
    while True:
        req = instance.reqdata()
        if req == False:
            logger.Logger().log("INFO", "Failed to obtain")
            continue
        else:
            req["type"] = "hsl"
            n =instance.ndata(req["req"])
            if n != False:
                logger.Logger().log("SUCCESS", "Obtained Data: ", n)
            else:
                logger.Logger().log("ERROR", "Data wasn't valid ")
                
if __name__ == "__main__":
    for _ in range(2):
        threading.Thread(target=start).start()