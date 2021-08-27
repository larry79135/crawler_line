from selenium import webdriver
import requests,time,csv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

option = webdriver.ChromeOptions()
option.add_argument('headless')
chrome = webdriver.Chrome(options=option)
chrome.get("https://today.line.me/tw/v2/tab/domestic")
chrome.execute_script("window.scrollTo(0,document.body.scrollHeight);");
time.sleep(2)
chrome.execute_script("window.scrollTo(0,document.body.scrollHeight);");
datas=[]
C=list()
index = 0
#最新國內新聞 part1
newss1=chrome.find_elements_by_css_selector("#__layout > div > div.universalFrame-wrap > div.main > div.main-wrap.main-wrap > div > div:nth-child(10) > div > section > div.listModule > a")
for new1 in newss1:
    
    if new1.text.split("\n")[0] =="影音":
        title=new1.text.split("\n")[1]
        source=new1.text.split("\n")[2]
    else:
        title=new1.text.split("\n")[0]
        source=new1.text.split("\n")[1]
    
    
    
    url=new1.get_attribute("href")
    datas.append({
        'title':title,
        'source':source,
        'url':url,
        
    })
    
    

#最新國內新聞 part2
newss2=chrome.find_elements_by_css_selector("#__layout > div > div.universalFrame-wrap > div.main > div.main-wrap.main-wrap > div > div:nth-child(11) > div > section > div>a")
for new2 in newss2:
    
    if new2.text.split("\n")[0] =="影音":
        title=new2.text.split("\n")[1]
        source=new2.text.split("\n")[2]
    else:
        title=new2.text.split("\n")[0]
        source=new2.text.split("\n")[1]
    
    url=new2.get_attribute("href")
    datas.append({
        'title':title,
        'source':source,
        'url':url,
        
    })

print("===最多留言====")
#最多留言
Mostmessages=chrome.find_elements_by_css_selector("#__layout > div > div.universalFrame-wrap > div.main > div.main-wrap.main-wrap > div > div:nth-child(13) > div > section > div.listModule >a")
for message in Mostmessages:
    
    title=message.text.split("\n")[0]
    source=message.text.split("\n")[1]
    url=message.get_attribute("href")
    datas.append({
        'title':title,
        'source':source,
        'url':url,
        
    }) 


for data in datas:
    i=data.get("url")
    chrome.get(i)
    time_before=chrome.find_element_by_css_selector("#__layout > div > div.universalFrame-wrap > div.swipeBack > div > div > div > div.entityPublishInfo > div > div > span.entityPublishInfo-meta-info.text.text--f.text--secondary.text--regular").text
    d = datetime.today() - timedelta(hours=int(time_before.split(' ')[1][:1]))
    datas[index]["time_before"] = d.strftime('%Y-%m-%d %H:%M')
    index=index+1
print("full_datas:",datas)

chrome.close()
with open('line_full.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['title','source','url','time_before'])
    for data in datas:
        title=data.get('title')
        source=data.get('source')
        url=data.get('url')
        time_before=data.get('time_before')
        writer.writerow([title,source,url,time_before])
