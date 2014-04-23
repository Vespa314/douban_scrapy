# -*- coding: utf-8 -*-
"""
Created on Wed Apr 02 00:58:10 2014

@author: Vespa
"""

import sys, time, os, re
import urllib, urllib2, cookielib


	

def GetRE(content,regexp):
    return re.findall(regexp, content)

def getURLContent(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url = url,headers = headers);   
        content = urllib2.urlopen(req).read();
        return content;
    except:
        return ""

def GetGuangzhu(opener,id):
    url = 'http://www.douban.com/people/'+id+'/contacts';
    content = opener.open(url).read();
    content = content.decode('utf8','ignore').encode('gbk','ignore');
    regexp = r'<a href="((?!href).*?)" class="nbg"><img src=.*?class="m_sub_img" alt="(.*?)"/></a></dt>';
    guanzhulist = GetRE(content,regexp);
    return guanzhulist


def logindouban():
    loginurl = 'https://www.douban.com/accounts/login'
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
    params = {
    "form_email":"XXXX@qq.com",
    "form_password":"XXXXXXX",
    "source":"index_nav" #没有的话登录不成功
    }
    
    #从首页提交登录
    response=opener.open(loginurl, urllib.urlencode(params))
    
    #验证成功跳转至登录页
    if response.geturl() == "https://www.douban.com/accounts/login":
        html=response.read()
  
    	#验证码图片地址
    imgurl=re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
    if imgurl:
        url=imgurl.group(1)
        res=urllib.urlretrieve(url, 'v.jpg')
        captcha=re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>' ,html)
        if captcha:
            vcode=raw_input('Input The Englished world:')
            params["captcha-solution"] = vcode
            params["captcha-id"] = captcha.group(1)
            params["user_login"] = "登录"
        response=opener.open(loginurl, urllib.urlencode(params))
    return opener


opener = logindouban()  
guanzhu = GetGuangzhu(opener,'lowsong-e');
f = open('a.txt','w');
for item in guanzhu:
    f.write(item[1]);
    f.write(":\n");
    f.write(item[0]+"\n\n\n");
f.close();
    


