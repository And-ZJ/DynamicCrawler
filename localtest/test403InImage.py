from dynamicCrawler import DownloadUrl,MyWebBrowser

if __name__ == '__main__':
    imgFile = open(r"./include403.bmp",'rb')
    if imgFile.readable():
        imgContent = imgFile.read()
        imgContentLen = len(imgContent)
        print(imgContentLen)
        if b'403' in imgContent:
            print("Found b'403' in img file")
    imgFile.close()

    url = "file:///E:/Code/Python/SimpleCrawler/CrawlerImageExample/main.html"
    # useRequestMethod(url)
    html = DownloadUrl(url)
    imgUrlList = getImgUrlList(html)
    print(imgUrlList)
    downloadImage(imgUrlList, "./downloadImage/")