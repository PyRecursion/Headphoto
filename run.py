from headphoto.main import *

if __name__ == '__main__':
    kw,startpn,endpn=get_info()
    headphoto=Headphoto(PATH,kw,startpn,endpn)
    headphoto.run()