import requests
def search():
    qqnumE = int(input('请输入QQ号：'))
    url = 'https://zy.xywlapi.cc/qqapi?qq=%s'%qqnumE
    response = requests.post(url)
    result = response.json()
    print(result)


