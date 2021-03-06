#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import urllib2
import re
import sys


class MovieComment:
    def __init__(self):
        # set encoding as utf-8
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.start = 0
        self.param = '&filter=&type='
        #User-Agent是用户代理，用于使服务器识别用户所使用的操作系统及版本、浏览器类型等，可以认为是爬虫程序的伪装。
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        self.commentList = []
        self.filePath = '/home/zkpk/test/DoubanComment.txt'

    def getPage(self):
        try:
            URL = 'https://movie.douban.com/subject/25823277/comments?start=' + str(self.start)
            request = urllib2.Request(url=URL, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            pageNum = (self.start + 20)/20
            print '正在抓取第' + str(pageNum) + '页数据...'
            self.start += 20
            return page
        except(urllib2.URLError, Exception), e:
            if hasattr(e, 'reason'):
                print '抓取失败，具体原因：', e.reason

    def getMovie(self):
        pattern=re.compile(u'<div.*?class="avatar">.*?'
                           +u'<a.*?title="(.*?)".*?href=".*?">.*?</a>.*?'
                           + u'<p.*?class="">(.*?)</p>', re.S)  #正则表达式
        while self.start <= 100:
            page = self.getPage()
            comments = re.findall(pattern, page)
            for comment in comments:
                self.commentList.append([comment[0], comment[1].strip()])#将捕获组数据写入评论List中

    def writeText(self):
        fileComment = open(self.filePath,'w')
        try:
            for comment in self.commentList:
                fileComment.write(comment[1]+'\n\n')
            print '文件写入成功...'
        finally:
            fileComment.close()

    def main(self):
        print '正在从《三生三世十里桃花》电影短评中抓取数据...'
        self.getMovie()
        self.writeText()
        print '抓取完毕...'


if __name__ == '__main__':
    doubanSpider = MovieComment()
    doubanSpider.main()


