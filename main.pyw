import config
import threading
import time
import pickle
from img_downloader import add_new_img
from img_downloader import remove_previous_img
from img_downloader import listdir_by_date_created
file=open('temp.pickle','rb')
config.generes=pickle.load(file)
file.close()
file=open('genere_count_data.pickle','rb')
config.genere_wallpic_count=pickle.load(file)
file.close()
class downloader(threading.Thread):
    def __init__(self):
        super(downloader, self).__init__()
        self.daemon=True
    def run(self):
        while True:
            time.sleep(1)
            print('i am awake!')
            while config.signal is True:
                print('i am waiting')
            if add_new_img() is True:
                print('download complete')
                config.signal=True
            else:
                print('I exited due to no net')
def set_desktop_bckgnd(filename):
    import ctypes
    SPI_SETDESKWALLPAPER = 0x0014
    cbuffer = ctypes.c_buffer(str.encode(filename))
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 1, cbuffer, 1)
def remove_temp_files():
    for file in config.os.listdir(config.wallpic_dir):
        if file.split('.')[-1] == 'temp':
            config.os.remove(config.wallpic_dir+'\\'+file)
remove_temp_files()
t=downloader()
t.start()
img_list = listdir_by_date_created(config.wallpic_dir)
img_list_len = len(img_list)
no=0
while True:
    img=img_list[no]
    if img.split('.') == 'temp':
        continue
    set_desktop_bckgnd(config.wallpic_dir+'\\'+img)
    print('desktop background set to'+img)
    time.sleep(5)
    if config.signal is True:
        remove_previous_img()
        img_list = listdir_by_date_created(config.wallpic_dir)
        img_list_len = len(img_list)
        config.signal=False
    else:
        no=(no+1)%img_list_len