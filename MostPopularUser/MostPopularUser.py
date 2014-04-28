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
    regexp = r'<a href="http:\/\/www.douban.com\/people\/([-\.\w]+)\/" class="nbg">.*alt="(.+)"';
    guanzhulist = GetRE(content,regexp);
    return guanzhulist


def logindouban():
    loginurl = 'https://www.douban.com/accounts/login'
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    
    params = {
    "form_email":"xxx@qq.com",
    "form_password":"xxx",
    "source":"index_nav" 
    }
    
    response=opener.open(loginurl, urllib.urlencode(params))
    
    html = ''
    if response.geturl() == "https://www.douban.com/accounts/login":
        html=response.read()
  
    #如果需要验证码
    imgurl=re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
    if imgurl:
        url = imgurl.group(1)
        urllib.urlretrieve(url, 'captcha.jpg')
        captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>' ,html)
        if captcha:
            vcode = raw_input('Input The Englished world:')
            params["captcha-solution"] = vcode
            params["captcha-id"] = captcha.group(1)
            params["user_login"] = "登录"
        response = opener.open(loginurl, urllib.urlencode(params))
    return opener

if __name__ == '__main__':
    seed = 'MovieL'  #种子人物
    opener = logindouban()  
    guanzhu = GetGuangzhu(opener,seed);
    f = open('a.txt','w');
    for item in guanzhu:
        f.write('%s:%s\n'%(item[1],item[0]))
    f.close();
    