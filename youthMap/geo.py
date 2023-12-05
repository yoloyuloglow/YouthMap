
import json
import requests
import dbconnect as db

api_key = "앱키"
# 위도, 경도 반환하는 함수
def addr_to_lat_lon(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    headers = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=headers).text))
    if 'documents' in result and result['documents']:
        match_first = result['documents'][0]['address']
    else:
        match_first = {'x':0,'y':0} 
    return [float(match_first['x']), float(match_first['y'])]

n=0    
r = db.select_all_data()
print(r[0][0])
for i in r:
    a = addr_to_lat_lon(i[4])
    l = round(a[1],6)
    t = round(a[0],6)
    db.update_ll(i[0], l, t)
    print(n,'번째임',l,' ',t)
    n=n+1

r = db.select_all_data()
print(r)

