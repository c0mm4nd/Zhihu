大力出奇迹的知乎爬虫
====

额……这个应该不能叫爬虫

由于呢那个时间紧迫～我又要写论文～我就随手写了个知乎爬虫～

因为把所有精力都放到数据库上了，所有就没有好好做爬取啦，直接用嵌套保证了loop～

So，用的时候会**非常非常非常卡**～爬取**效率也不是特别高**(因为**重复多**，**错误多**)

唯一好的大概就是我爬的People、Topic、Question之间关系比较全面吧～毕竟我就是要建立Relationship呀

有Star就改良，没有那就烂在Github吧，反正烂掉的项目也不少了。

有关##使用方法##呢

本人环境Ubuntu16.04.1 + Py2

使用Py3有迷之崩溃现象(可能和线程有关？)

依赖：`pip install zhihu_oauth pymongo`

记得先开MongoDB【也许是`sudo apt install mongodb-server` ?～

UN就是UserName, PW就是PassWord

大致就是这样啦反正也就才240行左右的脚本嘛

最后感谢zhihu_oauth的帮助，感谢zhihu接受我数百线程的请求

最后的最后感谢各位知乎用户让我爬……(逃

