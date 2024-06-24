# -*- coding: utf-8 -*-
import requests
from time import time
from loguru import logger
import re


# 获取 pt_key, pt_pin 从 cookies
def extract_pt_key_and_pt_pin(cookie_str):
    pt_key_match = re.search(r'pt_key=([^;]+)', cookie_str)
    pt_pin_match = re.search(r'pt_pin=([^;]+)', cookie_str)
    
    pt_key = pt_key_match.group(1) if pt_key_match else None
    pt_pin = pt_pin_match.group(1) if pt_pin_match else None
    
    return pt_key, pt_pin


# 请求函数
def req(**kwargs):
    url = kwargs.get("url", "")
    if not url:
        return None
    headers = kwargs.get("headers", {"User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;"})
    proxy = None
    proxies = kwargs.get("proxies", {"all://": proxy} if proxy else {})
    try:
        response = requests.request(
            method=kwargs.get("method", "GET"),
            url=url,
            params=kwargs.get("params", {}),
            data=kwargs.get("data", {}),
            json=kwargs.get("json", {}),
            files=kwargs.get("files", {}),
            headers=headers,
            cookies=kwargs.get("cookies", {}),
            verify=False,
            timeout=20
        )
        return response
    except Exception as e:
        logger.error(f'req {url} {e}')
        retry = kwargs.get("retry", 0)
        retry += 1
        if retry > 2:
            return None
        return req(**kwargs | {"retry": retry})


# 京豆签到
def signBeanAct(jd_ck):
    pt_key, pt_pin = extract_pt_key_and_pt_pin(jd_ck)
    result = {
        "code": 400,
        "msg": f'请输入pt_key及pt_pin',
        "time": int(time())
    }
    if not all([pt_pin, pt_key]):
        return result
    meta = {
        "method": "POST",
        "url": "https://api.m.jd.com/client.action",
        "data": {
            'functionId': 'signBeanAct',
            'body': '{}',
            'appid': 'signed_wh5_ihub',
            'client': 'apple',
            'clientVersion': '13.0.2',
            'h5st': '20240528100518226;5iy5yi6zngmi9yy4;9d49c;tk03w8a731b9741lMisyKzMrMjR382m8OHl6CME_42gdIK27Ztj59og7qFiXW6ANYumVHShrpZ3_ZS0YdGWqK3iY4Ppz;a791835d42061f132ff014304320d32c1e961322573832c7224985fdbbdb4a80;4.7;1716861918226;TKmWymVS34wMWdBCuoFxiVU9ZqmOQttKGrKnVObP83GJZYMza1mupKRvk-ZU6Nj4VdHOVgWbZu9qpwinIhHDWj703eS-Lz7cpZSUJmuAoevLoTGJlVk6nrDCJdsEqPdA9VL9QQJR-PzYFJipNAfyfKvauarIRTW7fGPA3pkTLjrAv_LsOFwkARWPBstGvW-pydLMlupoMyLwh15Je73wD50dMGxrcZXqP7KOLYCx4Hx-qv2YVtqPIE7qCyGHs292qExyfL-Qs_zDVBv1VTC1WM4xDMmWUHeHJUS_WWDFGYnOuVooASH9TGgekE09b_Aj42dBNZkEFasDO7ahC5QYbLg43mTNIeOt1gtErtxLkus9fR6JaZOlgE5dzuZ_tAfhzDpmY2LQb1zwv8oA91VEmsQRYtqe3KzB7K89QdjAvxWa1hwGxzRNDtBwYXJoTMRJ0YDA',
        },
        "headers": {
            "User-Agent": "jdapp",
            "Referer": "https://pro.m.jd.com",
        },
        "cookies": {
            "pt_key": pt_key,
            "pt_pin": pt_pin
        }
    }
    res = req(**meta)
    result.update({"msg": f'pt_key: {pt_key}; pt_pin: {pt_pin} 已失效，请重新获取pt_key和pt_pin'})
    if res.status_code == 200:
        text = res.text
        try:
            res = res.json()
            if res.get("errorMessage"):
                pass
            else:
                if res["data"]["status"] == '1':
                    result.update({
                        "code": 200,
                        "msg": f'{pt_pin} {res["data"]["newUserAward"]["title"]}' if res["data"].get(
                            "newUserAward") else f"{pt_pin} 今天已签到",
                    })
                else:
                    result.update({
                        "code": 200,
                        "msg": f"京东用户：{pt_pin} 今天已签到",
                    })
        except Exception as e:
            logger.error(f'{text} {e}')
            result.update({"msg": f"京豆签到程序异常 {kwargs}"})

        # 京东快递
        meta.update({
            "url": "https://lop-proxy.jd.com/jiFenApi/signInAndGetReward",
            "params": {},
            "json": [{"userNo": "$cooMrdGatewayUid$"}],
            "headers": {
                "AppParams": '{"appid":158,"ticket_type":"m"}',
                "uuid": "%.f" % (time() * 10 ** 13),
                "LOP-DN": "jingcai.jd.com"
            }
        })
        req(**meta)
    # tg 通知
    logger.info(result)
    
    return result.get("msg")

if __name__ == '__main__':
    import os
    jd_ck = os.getenv('JD_COOKIE')
    cookies = [jd_ck]
    print(jd_ck)
    for ck in cookies:
        print(signBeanAct(ck))
