import time
from lxml import etree
import requests
from threading import Thread
import random as R
from config import *


#url url='http://tieba.baidu.com/f?kw= pn= '  0第一页 50第二页
#链接Xpath
# //*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a[@rel='noreferrer']/@href
# http://tieba.baidu.com/p/6287270158
# //img[@class="BDE_Image"]/@src


def get_info():
    kw = input("请输入贴吧名:").strip()
    while True:
        try:
            startpn = int(input("输入起始页:"))
            endpn = int(input("输入终止页:"))
            if endpn >= startpn:
                break
            else:
                print("输入正确页码")
                continue
        except Exception as e:
            print("请重新输入数字")

    return kw,startpn,endpn


#设置User-Agent
class Headphoto:
    def __init__(self,path,kw,startpn,endpn):
        self.path=path
        self.startpn=startpn
        self.endpn=endpn
        self.kw=kw
        self.n = 0
    #取网页
    def get_html(self):
        for i in range(self.endpn+1-self.startpn):
            print("第{}页开始".format(self.startpn+i))
            html=requests.get(URL, params={"kw":self.kw,"pn":(self.startpn+i-1)*50}, headers={"User_Agent":R.choice(USER_AGENT)})
            html.encoding="utf-8"
            #线程并发处理
            Thread(target=self.htmlhandle,args=(html,)).start()



    #获取帖子链接处理
    def htmlhandle(self,html):
        parseHtml=etree.HTML(html.text)
        # 获取帖子
        link_list=parseHtml.xpath('//li[@class=" j_thread_list clearfix"]//div[@class="threadlist_title pull_left j_th_tit "]/a[@rel="noreferrer"]/@href')
        print("***************",len(link_list))
        for p in link_list:
            r_url = "http://tieba.baidu.com" + p
            self.imghandler(r_url)

    #获取图片处理
    def imghandler(self,r_url):
        html = requests.get(r_url, headers={"User_Agent":R.choice(USER_AGENT)})
        html.encoding="utf-8"
        parseHtml = etree.HTML(html.text)
        #图片链接列表
        imglink_list = parseHtml.xpath('//img[@class="BDE_Image"]/@src')

        for imglink in imglink_list:
            img=requests.get(imglink, headers={"User_Agent":R.choice(USER_AGENT)}).content
            filename =imglink[-12:]
            self.save(filename,img)

    #保存图像
    def save(self,filename,img):

        with open(self.path+"/"+filename,"wb") as f:
            f.write(img)
        self.n += 1
        print('第{}张完成'.format(self.n))

    def run(self):
        self.get_html()

# if __name__ == '__main__':
#     kw = input("请输入贴吧名:").strip()
#     while True:
#         try:
#             startpn = int(input("输入起始页:"))
#             endpn = int(input("输入终止页:"))
#             if endpn >= startpn:
#                 break
#             else:
#                 print("输入正确页码")
#                 continue
#         except Exception as e:
#             print("请重新输入数字")
#
#
#     headphoto=Headphoto(PATH,kw,startpn,endpn)
#     headphoto.run()