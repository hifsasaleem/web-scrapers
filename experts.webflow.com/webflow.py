import requests
import pandas as pd
import sys
import time
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

start = 0
end = 80
for n in range(start,end):
  newrow_list = []
  url = f"https://experts.webflow.com/browse?fe088fc9_page={n}"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  divs = soup.find_all("div", {"class": "experts-item w-dyn-item"})
  for div in divs:
    try:
       p = div.find("p",{"class":"line-clamp-3"}).text
       a = div.find("a",{"class":"experts-item_link w-inline-block"})["href"]
       name = div.find("h2",{"class":"experts-item_name"}).text
       info = div.find("div",{"class":"experts-item-info_wrapper"}).text
       img = div.find("img",{"class":"experts-item_profile-image"})["src"]
       res = requests.get(a)
       soup2 = BeautifulSoup(res.content, "html.parser")
       weblink = soup2.find("a",{"class":"--styled-dbGEqI wf-1ecmo1"})["href"]
       starting = soup2.find("span",{"class":"--styled-cfxuxD --pick-dBJKbx wf-dq4t4e"}).text
       about = soup2.find("p",{"class":"--styled-gqIQop --pick-dBJKbx wf-1oigpre"}).text
       new_row = [name,a,img,info,p,about,weblink,starting]
       newrow_list.append(new_row)
    except:
      pass


  df = pd.DataFrame.from_dict(newrow_list)
  df.to_csv('webflow_data.csv', mode='a', index=False, header=False)
  sys.stdout.write("\r %d of %d Pages Successfully Scraped"%(n,end))
  sys.stdout.flush()

columns=["Company","Profile","img_link","Location","description","About","Website Link","Strating At"]
csv_data = pd.read_csv("webflow_data.csv",names=columns)
df = pd.DataFrame(csv_data,columns=columns)
df.to_csv('webflow_data.csv')
