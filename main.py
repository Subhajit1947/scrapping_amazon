import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
chromedriver_path='C:\\Users\\Subhajit Das\\Downloads\\chromedriver-win64\\chromedriver.exe'
service = webdriver.chrome.service.Service(chromedriver_path)
driver = webdriver.Chrome(service=service,options=options)
link=[]
p_name=[]
p_review=[]
p_rating=[]
p_price=[]
p_desc=[]
p_manufac=[]
p_dimen=[]
p_asin=[]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}
proxies = {
  "http": None,
  
}

for page in range(1,30):
  try:
    n=5
    while n>0:
      r=requests.get(f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}',headers=HEADERS,proxies=proxies)
      if r.status_code==200:
        break
      n=n-1
    soup=BeautifulSoup(r.text,'html.parser')
    all_product=soup.find_all('div',class_='a-section a-spacing-small a-spacing-top-small')
    for i in all_product:
        url=i.find('a')
        prices=i.find('span',class_='a-offscreen')
        rat=i.find('div',class_='a-row a-size-small')
        name=i.find('span',class_='a-size-medium a-color-base a-text-normal')
        if name:
          p_name.append(name.text)
          # print(name.text)
        else:
          p_name.append('null')
        if rat:

          rr=rat.text
          data=rr.split()
          # print(rr)
          if(data[0]):
            p_rating.append(data[0][:3])
          else:
            p_rating.append('null')
          if(data[-1]):
            p_review.append(data[-1])
          else:
            p_review.append('null')
        else:
          p_review.append('null')
          p_rating.append('null')
          # print(data[0],data[-1])
        if prices:
          p_price.append(prices.text)
          # print(prices.text)
        else:
          p_price.append('null')
        if url:
          link.append(f"https://www.amazon.in{url.get('href')}")
          driver.get(f"https://www.amazon.in{url.get('href')}")
          try:
              
              all_p=driver.find_element(By.ID,'detailBullets_feature_div')
              desc=driver.find_element(By.ID,'productDescription')
              s=all_p.text
              if desc:
                p_desc.append(desc.text)
              else:
                p_desc.append('null')
              if s:
                data=s.split('\n')
                if len(data)>=3:
                  if 'Manufacturer' in data[2]:
                    p_manufac.append(data[2].split(':')[1])
                  else:
                    p_manufac.append('null')
                  if 'ASIN' in data[3]:
                    p_asin.append(data[3].split(':')[1])
                  else:
                    p_asin.append('null')
                else:
                  p_manufac.append('null')
                  p_asin.append('null')
              else:
                p_manufac.append('null')
                p_asin.append('null')
          except:
            p_manufac.append('null')
            p_asin.append('null')
            p_desc.append('null')
        else:
          p_manufac.append('null')
          p_asin.append('null')
          p_desc.append('null')
          link.append(f"null")
  except:
    pass
    




product_dict={
    'product_Name':p_name,
    'product_url':link,
    'price':p_price,
    'rating':p_rating,
    'review':p_review,
    'description':p_desc,
    'ASIN':p_asin,
    'manufacturer':p_manufac
}


df=pd.DataFrame(product_dict)


df.to_csv('python_amazon.csv')