from dynamicCrawler import DownloadUrl, MyWebBrowser
import os
import bs4 as bs


class AnimationUrl:
    """
        漫画对象，记录要下载的漫画名称及其url，可选字段describe为备注
    """

    def __init__(self, name: str, url: str, describe: str = ""):
        self.name = name
        self.url = url
        self.describe = describe

    def __str(self):
        return '{{"name":{name},"describe":{describe},"url":{url}}}'.format(**self.__dict__)

    def __repr__(self):
        return self.__str()


class AnimationChapterUrl:
    """
        漫画章节对象，记录要下载的漫画名称，以及某一章的名称及其url
    """

    def __init__(self, name: str, chapter: str, url: str):
        self.name = name
        self.chapter = chapter
        self.url = url

    def __str(self):
        return '{{"name":{name},"chapter":{chapter},"url":{url}}}'.format(**self.__dict__)

    def __repr__(self):
        return self.__str()


class DownloadAnimationImage:
    """
        下载漫画某一章的图片
    """

    def __init__(self, animationChapterUrl: AnimationChapterUrl, path: str):
        """
        :param animationChapterUrl: 漫画某一章的url
        :param path: 漫画图片保存位置（不是本章节保存路径，是整个漫画的保存位置），根据此路径，按照漫画名、章节名自动计算出本章节图片应保存的位置
        """
        self.animationChapterUrl = animationChapterUrl
        self.saveDir = path + self.animationChapterUrl.name + "/" + self.animationChapterUrl.chapter + "/"
        if not os.path.exists(self.saveDir):
            os.makedirs(self.saveDir)
        if self.animationChapterUrl.url == "":
            print(self.animationChapterUrl, "EmptyUrl")
            return
        self.downloadWebPage()
        # self.saveWebPage()
        self.getImageUrlList()
        self.downloadImage()

    def downloadWebPage(self):
        """
        下载漫画某一章节的网页，此网页中含有本章节所有图片的链接
        :return:
        """
        webBrowser = MyWebBrowser()
        self.html = webBrowser.downloadHtml(self.animationChapterUrl.url)

    def saveWebPage(self):
        """
            如果无法下载，或下载不对，可保存网页，查看网页内容是否渲染完毕，是否出现某些意外情况
        :return:
        """
        f = open(self.saveDir + self.animationChapterUrl.name + ".html", "w+", encoding="utf-8")
        f.write(self.html)
        f.close()

    def getImageUrlList(self):
        """
            在此章节网页上，查找并保存该章节所有漫画图片的链接
        :return:
        """
        self.soup = bs.BeautifulSoup(self.html, 'html.parser')
        self.pageSelectEle = self.soup.find('select', id='page_select')
        self.pageOptionList = self.pageSelectEle.find_all('option')
        print(self.pageOptionList)
        # 该章节所有漫画图片链接的链表
        self.imgUrlList = list()
        for pageOptionEle in self.pageOptionList:
            imgUrl = pageOptionEle.get("value", None)
            if imgUrl is None:
                continue
            if 'https' not in imgUrl:
                imgUrl = "https:" + imgUrl
            self.imgUrlList.append(imgUrl)

    def downloadImage(self):
        """
            下载 imgUrlList 中所有漫画图片
        :return:
        """
        index = 0
        for imgUrl in self.imgUrlList:
            index = index + 1
            try:
                content = DownloadUrl.download(imgUrl, self.animationChapterUrl.url)
            except Exception as e:
                print('Error:', e, imgUrl)
                continue
            #这里关于403错误的问题，之前误认为不会引发Exception，其实是会的，故去掉这里
            # if b'403' in content:
            #     print("403", imgUrl)
            #     continue
            # 获取图片的名字方便命名
            file_name = self.saveDir + str(index) + '.' + imgUrl.split(r'.')[-1]
            # 以二进制格式写入
            f = open(file_name, 'wb')
            f.write(content)
            f.close()


class GetAnimationChapterUrl:
    """
        在某漫画的主页上，获取所有章节的url链接
        注意，此处未保存其他系列、单行本等章节链接，同样也未实现翻页功能（如果漫画章节有多页）
        此处思路同 DownloadAnimationImage 类
    """

    def __init__(self, animationUrl: AnimationUrl, path: str):
        self.animationUrl = animationUrl
        self.path = path
        if self.animationUrl.url == "":
            return
        self.downloadWebPage()
        self.getAnimationChapterUrl()

    def downloadWebPage(self):
        # self.downloadDynamicPage = DownloadDynamicPage(self.animationUrl.url)
        webBrowser = MyWebBrowser()
        self.html = webBrowser.downloadHtml(self.animationUrl.url)

    def saveWebPage(self):
        f = open(self.path + self.animationUrl.name + ".html", "w+", encoding="utf-8")
        f.write(self.html)
        f.close()

    def getAnimationChapterUrl(self):
        self.soup = bs.BeautifulSoup(self.html, 'html.parser')
        self.chapterDivEles = self.soup.find_all('div', class_='cartoon_online_border')
        self.animationChapterUrlList = list()
        # print(self.chapterDivEles)
        for chapterDivEle in self.chapterDivEles:
            chapterEles = chapterDivEle.find_all('a')
            for chapterEle in chapterEles:
                chapterText = chapterEle.get_text()
                chapterUrl = chapterEle.get('href', None)
                if chapterUrl is None:
                    print("GetUrlFailed:", chapterEle)
                    continue
                if 'https' not in chapterUrl:
                    chapterUrl = r"https://" + self.animationUrl.url.split(r'/')[2] + chapterUrl
                self.animationChapterUrlList.append(
                    AnimationChapterUrl(self.animationUrl.name, chapterText, chapterUrl))


def main():
    # 定义一个要下载的漫画对象，存放该漫画名，及其漫画主页
    animationUrl = AnimationUrl("未闻花名", r"https://manhua.dmzj.com/wmrwzdntskjdhdmz")
    # 从漫画主页上，获取所有章节的url
    chapterUrl = GetAnimationChapterUrl(animationUrl, r'./')
    print(chapterUrl.animationChapterUrlList)

    # 将每章节链接保存下来（虽然还没有利用上）
    f = open(animationUrl.name + r"-Url.txt", "w+", encoding='utf-8')
    f.write(chapterUrl.animationChapterUrlList.__str__())
    f.close()

    # 通过range范围控制下载的章节数，例如这里下载前2话
    # （如果超出list范围，此处会崩溃）
    for i in range(0, 2):
        animationChapterUrl = chapterUrl.animationChapterUrlList[i]
        print(i)
        # 下载某章节url的图片，存储路径为当前文件夹
        DownloadAnimationImage(animationChapterUrl, r'./')


if __name__ == '__main__':
    main()