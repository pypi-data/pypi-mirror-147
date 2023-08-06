from bs4 import BeautifulSoup
import requests
# =================== search ================= #
def search(name):
    url = f"https://music-fa.com/search/{name}/"
    result = requests.get( url,timeout=10 )
    msoup = BeautifulSoup(result.text ,"html.parser")
    for k in msoup.find_all('div',attrs={'class':'cntfa'}):
        res = k.text
        print(res)
    for j in msoup.find_all('footer'):
        if len(j) >=0:
            rest = j.a.get('href')
            print(rest)
# search('آرمین+زارعی')            
# =================== download ================= #
def download(links):
    url = f"{links}"
    result = requests.get( url,timeout=10 )
    msoup = BeautifulSoup(result.text ,"html.parser")
    for down in msoup.find_all('div',attrs={'class','cntfa'}):
        print(down.audio.get('src'))
# download("https://music-fa.com/download-song/50970/")
# =================== dev ================= #
# telegram.me --> @SudoSaeed
# instagram --> SudoSaeed