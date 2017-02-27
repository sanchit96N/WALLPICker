from img_downloader import source_code_shortner
from img_downloader import inter_add_new_img
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import urllib.request
import re
import pickle
from config import *
print('Enter genres of wallpaper you like')
while True:
    genere=input()
    generes[genere]=[1,1]
    print('add more(yes/no)')
    choice=input()
    if choice !='yes':
        break
file=open('temp.pickle','wb')
pickle.dump(generes,file)
file.close()
file=open('genere_count_data.pickle','wb')
print('counting the number of wallpapers in each genre')
for genere in generes:
    url='https://wall.alphacoders.com/search.php?search='+genere
    only_h1_tags=SoupStrainer('h1')
    source_code=urllib.request.urlopen(url)
    source_code=source_code_shortner(source_code,700,800)
    soup=BeautifulSoup(source_code,'html.parser',parse_only=only_h1_tags)
    re_str=str(soup.contents[0])
    result=re.search(' [0-9]* ',re_str)
    genere_wallpic_count[genere]=int(result.group())
    print(str(result.group())+' wallpapers found in '+genere)
pickle.dump(genere_wallpic_count,file)
file.close()
print('Do you want to download initial wallpapers(It might take time)(yes/no)')
input=input()
if input == 'yes':
    # Download 10 wallpapers
    print('downloading initial wallpapers')
    for _ in range(10):
        inter_add_new_img()
else:
    print('Then copy 10 wallpapers of your choice to the directory '+wallpic_dir)
# set the app to startup
os.rename(
    'main.pyw - Shortcut.lnk',
'C:\\Users\\'+os.getlogin()+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\main.pyw - Shortcut.lnk')
print('Restart your computer to launch the application')
