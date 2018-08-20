from dynamicCrawler import DownloadUrl, MyWebBrowser

import os
import bs4 as bs


def downloadLocalHtml(url: str):
    """
        声明为MyWebBrowser为局部变量，而不是全局变量
    :param url: 要下载的 url
    :return: 返回下载下来的 html
    """
    browser = MyWebBrowser()
    html = browser.downloadHtml(url)
    # f = open("download.html", "w+", encoding="utf-8")
    # f.write(html)
    # f.close()
    return html


def getImgUrlList(html: str):
    """
        从 html 网页字符串中解析所需要的图片的 url，存储进list中
    :param html:
    :return: list，存储图片的下载链接(url)，此 url 可能不是完整的 url，比如缺少域名等。
    """
    # 使用html.parser解析
    soup = bs.BeautifulSoup(html, 'html.parser')
    # 按条件查找img标签。解析方法依通过分析网页上要下载的图片而定
    imgTagList = soup.find_all('img', class_='test')
    print('imgTagList:', imgTagList)
    imgUrlList = list()
    for imgTag in imgTagList:
        # 获取img标签的src中的url
        imgUrl = imgTag.get("src", None)
        if imgUrl is None:
            continue
        imgUrlList.append(imgUrl)
    return imgUrlList


def downloadImage(imgUrlList: list, saveDir: str):
    """
        下载imgUrlList中所有的imgUrl，请注意，要组合完整的url
    :param imgUrlList: getImgUrlList()的返回值
    :param saveDir: 下载下来的图片的存储本地的路径
    :return:
    """
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    index = 0
    for imgUrl in imgUrlList:
        index = index + 1
        # 由于imgUrl可能不是完整的Url，所以需要组装成完整可访问的Url
        # 请根据实际情况，自己设计组装方案，或者，在上一步获取时，就组装好传递过来
        imgUrl = url.rsplit(r'/', 1)[0] + "/" + imgUrl.rsplit(r'/', 1)[1]
        # print(imgUrl)
        try:
            # referer_url 最好填写，参考Chrome中的referer结果填写
            # 这里是本地网页，所以没传此参数
            content = DownloadUrl.download(imgUrl)
        except Exception as e:
            print('Error:', e, imgUrl)
            continue
        print("success:", imgUrl)
        # 对下载文件重命名：路径 + 序号 + 原文件名后缀
        file_name = saveDir + str(index) + '.' + imgUrl.split(r'.')[-1]
        # 图片文件以二进制格式写入
        f = open(file_name, 'wb')
        f.write(content)
        f.close()


if __name__ == '__main__':
    htmlFilePath = os.path.abspath('./main.html').replace('\\', r'/')
    # 组合结果例如： url = r"file:///E:/Code/Python/AnimationCrawler/localTest/main.html"
    url = r"file:///" + htmlFilePath
    print(url)
    html = downloadLocalHtml(url)
    imgUrlList = getImgUrlList(html)
    print(imgUrlList)
    downloadImage(imgUrlList, "./downloadImage/")
