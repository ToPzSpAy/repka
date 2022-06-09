import base64
import requests
from urllib import request
def upload(ava):
    with open(ava, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "0528a80aeea4a87bc9efa09110cd00d9",
            "image": base64.b64encode(file.read()),
        }
        try:
            res = requests.post(url, payload)
            data = res.json()
        except Exception as er:
            print("Не получилось отправить",er)
    print(data['data']['url'])
    return data['data']['url']

def load(url):
    data = request.urlopen(url).read()
    return data