# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 16:43:58 2014

@author: Administrator
"""
import re
import urllib2
import urllib
import time
import json

def GetRE(content,regexp):
    return re.findall(regexp, content)
    
def GetContent(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
    req = urllib2.Request(url = url,headers = headers);   
    content = urllib2.urlopen(req).read();
    return content.decode('utf8','ignore').encode('gbk','ignore');

    
def GetAllTagList():
    """
    http://book.douban.com/tag/
    获取全部分类列表
    """
    content = GetContent("http://book.douban.com/tag/")
    regexp = r"<td><a href=\"./(.+)\">\1";
    return GetRE(content,regexp);
    
def GetBookWithTag(tag):
    """
    http://book.douban.com/tag/:tag?start=0&type=T
    获取书本信息
    """
    startid = 0;
    TotalList = [];
    while True:
        url = "http://book.douban.com/tag/"+tag+"?start="+str(startid)+"&type=T"
        content = GetContent(url)
        cut_idx = content.find('block5 movie_show');
        #截断右边栏的推荐书目
        if cut_idx >= 0:
            content = content[:cut_idx]
        #提取书本ID
        regexp = r"http://book.douban.com/subject/(\d+)/\"";
        #去重
        BookIdList = list(set(GetRE(content,regexp)))
        if len(BookIdList) != 0:
            TotalList += BookIdList
            startid += 20;
            time.sleep(2)
        else:
            break
    return list(set(TotalList))
            
def getBookInfo(id):
    """
    根据API来获取书本信息
    """
    url = 'https://api.douban.com/v2/book/'+str(id);
    content = GetContent(url)
    info = json.loads(content.decode('gbk','ignore').encode('utf8','ignore'))
    print info['title'].encode('gbk','ignore')

if __name__ == "__main__":
    taglist = GetAllTagList();
    f = open('BookId.txt','w');
    for tag in taglist:
        f.write('%s\n'%(tag))
        tag = urllib.quote(tag.decode('gbk','ignore').encode('utf8','ignore'))
        BookIdList = GetBookWithTag(tag)
        for BookId in BookIdList:
            f.write('\t%s\n'%(BookId))
#            getBookInfo(BookId)
    f.close();