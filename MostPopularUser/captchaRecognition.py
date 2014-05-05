# -*- coding: utf-8 -*-
"""
Created on Tue May 06 00:45:44 2014

@author: Administrator
"""

from PIL import Image
from pytesser import *


def Binarize(img,threshold):
    img = img.convert('L')
    table = [0]*threshold+[1]*(256-threshold) 
    return img.point(table,'1').convert('L')

def scrap_img(imgdata,dst,width,heigth,x,y):
    findlist = []
    waitlist = [(x,y)]
    while waitlist != []:
        cur = waitlist.pop(0)
        for (i,j) in [(1,0),(-1,0),(0,1),(0,-1)]:
            if  cur[0]+i < 0 or cur[0]+i>=width or cur[1]+j<0 or cur[1]+j>=heigth:
                continue
            if imgdata[cur[0]+i,cur[1]+j] == dst:
                if not (cur[0]+i,cur[1]+j) in findlist:
                    findlist.append((cur[0]+i,cur[1]+j));
                    if not (cur[0]+i,cur[1]+j) in waitlist:
                        waitlist.append((cur[0]+i,cur[1]+j));
    return findlist
    

def m_filter2(img):
    imgdata1 = img.load()
    w,h = img.size
    for x in range(w):
        for y in range(h):
            if imgdata1[x,y] == 0:
                scraplist = scrap_img(imgdata1,0,w,h,x,y);
                imgdata1[x,y] = 255 - 254*(len(scraplist) > 30)
                for p in scraplist:
                    imgdata1[p[0],p[1]] = 255 - 254* (len(scraplist) > 30)
    return img

def recognition(path):
    img = Image.open(path)
    img = Binarize(img,45)
    img = m_filter2(img)
#    img.show()
    string_re =  image_to_string(img)
    if string_re.find(" ") >= 0:
        string_re = string_re.replace(" ","")
    if string_re.find("\n") >= 0:
        string_re = string_re.replace("\n","")
    return string_re

if __name__ == "__main__":
    print recognition('./captcha.jpg')