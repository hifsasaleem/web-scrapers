import requests
import pandas as pd
import sys
import time

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
"Content-Type": "application/json"}


start = 0
end = 10000
for n in range(start,end,20):
  dict_list = []
  response = requests.get(f"https://www.knx.org/knx-de/fuer-fachleute/community/partner/?type=json&country=&per_page={n}&qualification=total",headers = headers)
  data = response.json()
  rows = data['rows']
  for i in range(len(rows)):
    company = rows[i]["company"]
    city = rows[i]["city"]
    owner = f"{rows[i]['lastname']} {rows[i]['firstname']}"
    Address = f"{rows[i]['street']} {rows[i]['housenumber']} {rows[i]['city']}"
    Telephone = rows[i]["phone"]
    mobile = rows[i]["mobile"]
    Email = rows[i]["email"]
    website = rows[i]["website"]
    new_row = {"Company":company,"City":city,"Owner":owner,"Address":Address,"Telephone":Telephone,"Mobile":mobile,"Email":Email,"Website":website}
    dict_list.append(new_row)
  df = pd.DataFrame.from_dict(dict_list)
  df.to_csv('knx_data.csv', mode='a', index=False, header=False)
  fethed = n + 20
  percentage = (fethed / end)*100
  sys.stdout.write("\r %d"%percentage + "%"+ "    %d of %d Data Successfully Scraped"%(fethed,end))
  sys.stdout.flush()

columns=["Company","City","Owner","Address","Telephone","Mobile","Email","Website"]
csv_data = pd.read_csv("knx_data.csv",names=columns)
df = pd.DataFrame(csv_data,columns=columns)
df.to_csv('knx_data.csv')