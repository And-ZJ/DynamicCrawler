=================
DynamicCrawler
=================

用于演示如何使用PyQt5渲染动态页面，然后下载动态页面中的内容

更新 2018-08-20 16:31
    已知 BUG：
        1. 类 MyWebBrowser 中:
            经测试发现，若实例化类 MyWebBrowser 为全局变量，易出现进程 qtwebengineprocess 无法自动退出的状况（此进程会占用大量CPU）
            初步推测是 QWebEnginePage 对象 没有正常退出所致。若是局部变量，则不会出现此情况，可参见 localTest/example.py 写法
    修改：
        1. 403 错误，会引发 Exception，而不是之前说的不会引发 Exception。因此，去掉了手动排除403错误的代码

License
============
    仅供学习交流，如有侵权，请联系删除

Examples
========
    详见 webTest/example.py 和 localTest/example.py 文件
    此处测试网站是动漫之家（如有侵权，请立即联系删除）

参考文献等资料已在此文章中声明：https://blog.csdn.net/And_ZJ/article/details/80003543