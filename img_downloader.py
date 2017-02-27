import config
import random
import requests
import pickle
import re
import math
import urllib.request
from bs4 import BeautifulSoup
import socket
socket.setdefaulttimeout(15)

def download_image(genere,page_no,img_no):
    print('inside download_image')
    url=fetch_url(genere,page_no,img_no)
    print('got image url '+url)
    img_downloader(url)
def source_code_shortner(source_code,start,end):
    count=1
    temp=''
    for line in source_code:
        if count>=start and count<=end:
            temp=temp+str(line.decode('utf-8'))
        else:
            if count>end:
                break
        count=count+1
    return temp
def fetch_url(genere,page_no,img_no):
    print('inside fetch_url')
    print('1')
    print('downloading '+genere+' '+str(page_no)+' '+str(img_no))
    page_url=\
        'https://wall.alphacoders.com/search.php?search='+genere+'&'+'page='+str(page_no)
    source_code=urllib.request.urlopen(page_url)
    print('2')
    source_code=source_code_shortner(source_code,800,2000)
    print('2-')
    soup=BeautifulSoup(source_code,'html.parser')
    print('2--')
    images=soup.findAll('div',{'class':'thumb-container-big '})
    img_page_url=config.home_url+images[img_no-1].div.div.a['href']
    print('3')
    print('got image page url = '+img_page_url)
    img_soup = BeautifulSoup(requests.get(img_page_url).text, 'html.parser')
    img_obj = \
        img_soup.find('div', {'style': re.compile('position:relative; width:.*px; max-width:98%; margin:auto;')})
    print('4')
    return img_obj.a['href']
def img_downloader(img_url):
    print('inside img_downloader')
    img_name=img_url.split('/')[-1]
    img_ext=img_name.split('.')[-1]
    img_name=img_name.split('.')[:-1]
    img_name=''.join(img_name)
    # try:
    #     urllib.request.urlretrieve(img_url,
    #                            config.wallpic_dir+'\\'+img_name+'.temp')
    # except:
    #     if type_of_use == 1:
    #         config.os.remove(config.wallpic_dir+'\\'+img_name+'.temp')
    urllib.request.urlretrieve(img_url,
                               config.wallpic_dir + '\\' + img_name + '.temp')
    config.os.rename(config.wallpic_dir + '\\' + img_name + '.temp',
              config.wallpic_dir + '\\' + img_name + '.' + img_ext)
def inter_add_new_img():
    print('inside inter_add_new_img')
    print('trying to download new image')
    genere = list(config.generes.keys())[random.randint(0, len(list(config.generes.keys())) - 1)]
    read_file = open('temp.pickle', 'rb')
    config.generes = pickle.load(read_file)
    download_image(genere, config.generes[genere][0], config.generes[genere][1])
    read_file.close()
    write_file = open('temp.pickle', 'wb')
    total_no_of_pages = math.ceil(config.genere_wallpic_count[genere] / 30)
    config.generes[genere][1] = config.generes[genere][1] + 1
    if config.generes[genere][1] == 31:
        config.generes[genere][0] = (config.generes[genere][0]) % total_no_of_pages + 1
        config.generes[genere][1] = 1
    pickle.dump(config.generes, write_file)
    write_file.close()
def add_new_img():
    print('inside add_new_img')
    try:
        inter_add_new_img()
        return True
    except :
        print('connection problem')
        return False
def listdir_by_date_created(dir_path):
    mtime = lambda f: config.os.stat(dir_path+'\\'+f).st_mtime
    return list(sorted(config.os.listdir(dir_path), key=mtime))
def remove_previous_img():
    files=listdir_by_date_created(config.wallpic_dir)
    if len(files) >=1:
        file = listdir_by_date_created(config.wallpic_dir)[0]
        print('removing '+file)
        config.os.remove(config.wallpic_dir+'\\'+file)
