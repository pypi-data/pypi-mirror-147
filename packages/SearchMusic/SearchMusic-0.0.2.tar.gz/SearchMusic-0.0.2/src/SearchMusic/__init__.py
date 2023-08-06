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
# =================== download ================= #
def download(links,auto):
    url = f"{links}"
    result = requests.get( url,timeout=10 )
    msoup = BeautifulSoup(result.text ,"html.parser")
    for down in msoup.find_all('div',attrs={'class','cntfa'}):
        dn = down.audio.get('src')
    if auto:
        local_file = dn.split('/')[-1]
        with requests.get(dn, stream=True) as r:
            r.raise_for_status()
            with open(local_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        return print(f"""*****************************************
*                                       *
*    Download completed.                *
*    Song name: {local_file}            *
*    For criticisms and suggestions,    *
*    contact the author of this library *
*    on Telegram and Instagram :)       *
*    telegram --> @SudoSaeed            *
*    instagram --> SudoSaeed            *
*                                       *
*                                       *
*****************************************""")
    else:
        return dn
# print(download(links="https://music-fa.com/download-song/44384/",auto=True))
# =================== dev ================= #
# telegram.me --> @SudoSaeed
# instagram --> SudoSaeed