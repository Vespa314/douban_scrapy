# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 16:43:58 2014

@author: Administrator
"""
import re
import urllib
import urllib2
import time
import json

class Book:
    def __init__(self,JsonInfo):
        if JsonInfo.has_key('title'):
            self.Name = JsonInfo['title'];
        if JsonInfo.has_key('rating') and JsonInfo['rating'].has_key('average'):
            self.Rate = JsonInfo['rating']['average']
        if JsonInfo.has_key('rating') and JsonInfo['rating'].has_key('numRaters'):
            self.RateNum = JsonInfo['rating']['numRaters']
        if JsonInfo.has_key('pages'):
            self.Page = JsonInfo['pages']
        if JsonInfo.has_key('price'):
            self.Price = JsonInfo['price']
        if JsonInfo.has_key('pubdate'):
            self.Pubdate = JsonInfo['pubdate']
        if JsonInfo.has_key('publisher'):
            self.Publisher = JsonInfo['publisher']
        if JsonInfo.has_key('id'):
            self.Id = JsonInfo['id']
    Name = None
    Rate = None
    RateNum = None
    Page = None
    Price = None
    Pubdate = None;
    Publisher = None;
    Id = None

def GetRE(content,regexp):
    return re.findall(regexp, content)
    
def GetContent(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
    req = urllib2.Request(url = url,headers = headers);
    while True:    	
        flag = 1;
        try:
            content = urllib2.urlopen(req).read();
        except:
        	flag = 0;
        	time.sleep(5)
        if flag == 1:
        	break;
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
    url = 'https://api.douban.com/v2/book/'+id;
    content = GetContent(url)
    JsonInfo = json.loads(content.decode('gbk','ignore').encode('utf8','ignore'))
    book = Book(JsonInfo);
    return book
    
def WriteItem(fh,book):
    fh.write('%s\n'%book.Name.encode('gbk','ignore'));
    fh.write('\tId:%s\n'%book.Id.encode('gbk','ignore'));
    fh.write('\tRate:%s\n'%book.Rate.encode('gbk','ignore'));
    fh.write('\tRate Number:%d\n'%book.RateNum);
    fh.write('\tPrice:%s\n'%book.Price.encode('gbk','ignore'));
    fh.write('\tPublish Date:%s\n'%book.Pubdate.encode('gbk','ignore'));
    fh.write('\tPublisher:%s\n\n'%book.Publisher.encode('gbk','ignore'));

def GetAllIdOfBook():
    taglist = GetAllTagList();
    f = open('BookId.txt','w');
    for tag in taglist:
        f.write('%s\n'%(tag))
        tag = urllib.quote(tag.decode('gbk','ignore').encode('utf8','ignore'))
        BookIdList = GetBookWithTag(tag)
        for BookId in BookIdList:
            f.write('\t%s\n'%(BookId))
    f.close();

def scrawlAllBook():
    BookIdList = [];
    IDListFile = open('BookId.txt','r')
    for line in IDListFile:
        id = GetRE(line,r'^\t(\d+)$');
        if id == []:
            continue
        BookIdList.append(id[0])
    IDListFile.close()
    BookIdList = list(set(BookIdList))
    file_h = open('book_detail.txt','a+')
    for bookid in BookIdList:
        BookInfo = getBookInfo(bookid);
        print BookInfo.Id,BookInfo.Name.encode('gbk','ignore')
        WriteItem(file_h,BookInfo) 
        time.sleep(2)


    
if __name__ == "__main__":
    #爬取所有书ID保存到文件中
#    GetAllIdOfBook()
    scrawlAllBook()

    