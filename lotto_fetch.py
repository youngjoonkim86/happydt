import requests
import pandas as pd
import time

def fetch_lotto_data(start=1, end=1110):
    lotto_data = []

    for i in range(start, end + 1):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={i}"
        res = requests.get(url).json()

        if res.get("returnValue") != "success":
            break

        row = [
            res["drwNo"],
            res["drwtNo1"],
            res["drwtNo2"],
            res["drwtNo3"],
            res["drwtNo4"],
            res["drwtNo5"],
            res["drwtNo6"],
            res["bnusNo"]
        ]
        lotto_data.append(row)
        time.sleep(0.1)

    df = pd.DataFrame(lotto_data, columns=["회차", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6", "보너스"])
    df.to_csv("lotto_data.csv", index=False, encoding='utf-8-sig')
    return df
