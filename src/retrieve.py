import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urldefrag
import json
seed_urls = [
        "https://waitbutwhy.com",
"https://paulgraham.com",
"https://zenhabits.net",
"https://markmanson.net",
"https://lesswrong.com",
"https://aeon.co",
"https://longreads.com"   ]
pages=[]

visited=set()
max_depth=3
crawl_queue = [(url, 0) for url in seed_urls]
counter=0
while crawl_queue and counter<150 :
    counter+=1
    url,depth=crawl_queue.pop(0)
    if depth>max_depth:
        continue
    if url in visited :
        continue
    visited.add(url)

    try :
        headers = {"User-Agent": "SeekBot/1.0"}
        response = requests.get(url, timeout=5, headers=headers)

        html=response.text

    except:
        continue

    soup = BeautifulSoup(html,"html.parser")
    
    for link in soup.find_all('a',href=True):
        abs_link=urljoin(url,link['href'])


        abs_link, _ = urldefrag(abs_link)
        excluded_domains = ["wikipedia.org", "wikihow.com", "wiktionary.org"]
        if any(domain in abs_link for domain in excluded_domains):
            continue

        if abs_link not in visited:
            crawl_queue.append((abs_link, depth + 1))    
    text=soup.get_text()
    pages.append({"url": url,"content":text})
    print(f"Crawled : {url} | Words : {len(text.split())} with counter : {counter}")
    

with open("pages.json","w") as f:
    json.dump(pages,f,indent=2)

print("###########################################")
print("Succefully Crawled sites and Saved Page.")








