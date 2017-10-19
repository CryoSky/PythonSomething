# -*- coding:utf-8 -*-
# Written by cryosky, 2017-10-17

import re
import urllib.request
from bs4 import BeautifulSoup
import os


# 下载 HTML
def get_HTML_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'} # 加头部
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req)
    content = html.read().decode('utf-8') # 转码
    html.close() # 记得要将打开的网页关闭，否则会出现意想不到的问题
#    print (content)
#    print (type(content))
    return content

# 找到漫画的题目
def get_Title(content):
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('h1').get_text()
    print (title)
    return title

# 找到漫画的页数
def get_PageNum(title):
    temp = re.findall(r"\[(.+?)\]", title)  # 这一步先把标题中所有[]中的抠出来组成一个列表
    length = len(temp)
    tempPageNum = temp[length-1]
#    print (temp[length-1])  # 这一步成功抽出了XXp
    realPageNum = re.findall(r"\d+", tempPageNum)
#    print (realPageNum) # 这里成功抽出了最后的页数，但是以列表形式表示
    intrealPageNum = int(realPageNum[0]) #  抠出来改成int
#    print (type(intrealPageNum))
    return intrealPageNum

def get_DownloadNum(content):
    soup = BeautifulSoup(content, 'html.parser')
    linkpage = soup.find_all("script", attrs={"language":"javascript"})
    aorb = 0
    for flag in linkpage:
#        print(str(flag))  #这网页会随机变换……有的时候会多一层script标签
        if 'Large_cgurl' not in str(flag):  # 判断，若获取的flag值里面没有Large_cgurl，则结束本次循环
            continue
        directlink = re.search('http://hahost2.imgscloud.com/file/'+r".*?.jpg", str(flag))  #总算把第一个直接链接给TM抠出来了
        if directlink == None:
            aorb = 1 # 这里立一个flag用于后面下载链接判断
            directlink = re.search('http://hbhost2.imgscloud.com/file/' + r".*?.jpg", str(flag))  # 这个链接也会随机变换！有时a有时b！用aorb判断

    checklist = directlink.group(0).split('/') # 这里把刚才的结果以/分段
    downlinknum = checklist[-2]
    print("The manga number in website source: %d" % int(downlinknum))
    return downlinknum, aorb  #这个函数返回了两个值

# 利用Soup第三方库实现抓取
def get_Image(html, title, number, downlinknum, flag):
    tempnumber = str(downlinknum) #把真正的下载地址转为str
    downloadlink = 'http://hahost2.imgscloud.com/file/' + tempnumber
    if flag == 1:
        downloadlink = 'http://hbhost2.imgscloud.com/file/' + tempnumber
    all_image = re.findall(downloadlink+r".*?.jpg", html) # 这一步把所有的downloadlink抓出来了
#    print (all_image)
    start = 1
    os.mkdir('C:\\下载\\comic\\' + '%s' % title)  # 使用os库里的命令先创建一个文件夹，不然下面urlretrieve会报错
    for image in all_image:
        filename = number+'_'+ str(start).zfill(3)   # 输出6300_001这样的文件名
        print (filename)
        urllib.request.urlretrieve(image, 'C:\\下载\\comic\\'+'%s\\'% title + '%s.jpg' % filename)
        start += 1


# 主函数
def main():
    number = input("Enter your manga number in website: ")
    url = 'http://18h.mm-cg.com/18H_'+number+'.html'
    html = get_HTML_content(url)
    title = get_Title(html)
    pagenumber = get_PageNum(title)
    print('The total page is : %d' %pagenumber)
    downlinknum, aorb = get_DownloadNum(html)
    get_Image(html, title, number, downlinknum, aorb)


'''
    for intnumber in range (1,100):  # 为什么不使用for循环呢？
        number = str(intnumber)
'''

# 执行主函数
if __name__== '__main__':
    main()
