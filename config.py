import os
home_url='https://wall.alphacoders.com/'
generes={}
genere_wallpic_count={}
signal=False
pic_dir='C:\\Users\\'+os.getlogin()+'\\Pictures'
wallpic_dir=pic_dir+r'\auto_wallpapers'
if os.path.exists(wallpic_dir)==False:
    os.mkdir(wallpic_dir)