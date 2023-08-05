import os
from components.pic2latex import pic2latex
import demo1


__all__=["svg2emf","about","m3u8_download",'pic2latex']
# __version__=666

def m3u8_download(url=None,savename=None):
    workDir=' --workDir "E:"'
    args = ""
    cmd = "N_m3u8DL-CLI.exe"
    os.system(cmd)

def svg2emf(FileName):
    os.system("inkscape --export-type=emf "+ FileName)

def about():
    print("Hi, I am Dagwbl. ")
    return True

if __name__=="__main__":
    print(__all__)
    while True:
        key = input("从模块直接启动，请使用命令行交互，输入命令以开始：")
    print('pygwbl: running by myself')
else:
    print('pygwbl: I am being imported from other module')
