# -*- coding: utf-8 -*-
"""
Created on Tue May 06 00:45:44 2014

@author: Administrator
"""

from PIL import Image
from pytesser import *

#class img_pixel:
#    def __init__(self,img):
#        self.listdata = list(img.getdata())
#        self.width,self.heigth = img.size
#    def getxy(self,x,y):
#        return self.listdata[y*self.width+x]

def Binarize(img,threshold):
    img_G = Image.new('L',img.size,1)
    w,d = img.size
    imgdata,imggraydata = img.load(),img_G.load()
    for x in range(w):
        for y in range(d):
            imggraydata[x,y] = 255*(imgdata[x,y][0]>threshold or imgdata[x,y][1]>threshold or imgdata[x,y][2] > threshold)
    return img_G


def scrap_img(imgdata,dst,width,heigth,x,y):
    findlist = []
    waitlist = [(x,y)]
    while waitlist != []:
        cur = waitlist.pop(0)
        for (i,j) in [(cur[0]+1,cur[1]),(cur[0]-1,cur[1]),(cur[0],cur[1]+1),(cur[0],cur[1]-1)]:
            if  i < 0 or i>=width or j<0 or j>=heigth:
                continue
            if imgdata[i,j] == dst:
                if not (i,j) in findlist:
                    findlist.append((i,j));
                    if not (i,j) in waitlist:
                        waitlist.append((i,j));
    return findlist
    
def m_filter2(img):
    imgdata = img.load()
    w,h = img.size
    for x in range(w):
        for y in range(h):
            if imgdata[x,y] == 0:
                scraplist = scrap_img(imgdata,0,w,h,x,y);
                for p in scraplist:
                    imgdata[p[0],p[1]] = 255 - 254* (len(scraplist) > 30)
                imgdata[x,y] = 255 - 254*(len(scraplist) > 30)
    return img

def recognition(path):
    img = Image.open(path)
    img = Binarize(img,45)
    img = m_filter2(img)
    string_re =  image_to_string(img)
    if string_re.find(" ") >= 0:
        string_re = string_re.replace(" ","")
    if string_re.find("\n") >= 0:
        string_re = string_re.replace("\n","")
    return string_re

if __name__ == "__main__":
    print recognition('./captcha.jpg')