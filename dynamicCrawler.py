# -*— coding:utf-8 -*-
import urllib.request
import urllib.response
import random,sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

# 用于下载时，渲染页面使用，当渲染完成，即可开始下载
class MyWebBrowser(QWebEnginePage):
    app = None
    # 类变量 QApplication
    # 实际测试时，若调用了多个MyWebBrowser对象（有先后顺序的调用）
    # 比如现在某些页面上，获取了所有包含图片的页面链接，再去打开这些链接上抓取图片
    # 容易在这一步 super().__init__() 异常崩溃
    # 可能是在 QApplication.quit()调用时，出现了资源释放异常
    # 改成类变量控制后，没有出现崩溃现象，这个还需要再测试测试

    def __init__(self):
        if MyWebBrowser.app is None:
            MyWebBrowser.app = QApplication(sys.argv)
        # self.app = QApplication(sys.argv)
        # print("DownloadDynamicPage")
        super().__init__()
        self.html = ''
        # 将加载完成信号与槽连接
        self.loadFinished.connect(self._on_load_finished)
        # print("DownloadDynamicPage Init")

    def downloadHtml(self, url):
        """
            将url传入，下载此url的完整HTML内容（包含js执行之后的内容）
            貌似5.10.1自带一个download函数
            这个在5.8.2上也是测试通过的
        :param url:
        :return: html
        """
        self.load(QUrl(url))
        print("\nDownloadDynamicPage", url)
        # self.app.exec_()
        # 函数会阻塞在这，直到网络加载完成，调用了quit()方法，然后就返回html
        MyWebBrowser.app.exec_()
        return self.html

    def _on_load_finished(self):
        """
            加载完成信号的槽
        :return:
        """
        self.html = self.toHtml(self.___callable)

    def ___callable(self, html_str):
        """
            回调函数
        :param html_str:
        :return:
        """
        self.html = html_str
        MyWebBrowser.app.quit()
        # self.app.quit()


class DownloadUrl:
    """
        使用urllib下载文件
    """
    # 用于绕过403错误的不同的浏览器标识
    userAgentList = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    ]

    @staticmethod
    def download(url, referer_url: str = ""):
        '''
            下载url所指文件，可一定程度上绕过403错误
        '''
        randomUserAgent = random.choice(DownloadUrl.userAgentList)
        request = urllib.request.Request(url)
        request.add_header("User-Agent", randomUserAgent)
        if "http" in url:
            host = url.split(r'/')[2]
        else:
            host = url.split(r'/')[0]
        # 请自行测试分割host方案，host最好也填写
        request.add_header("Host", host)
        request.add_header("GET", url)
        if referer_url != "":
            request.add_header("Referer", referer_url)
        response2 = urllib.request.urlopen(request)
        print(response2.getcode(), url)
        # 返回下载的所有内容
        return response2.read()



