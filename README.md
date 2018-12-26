## 百度百科的爬取，现在实现全站爬取

**持久化启动爬虫**
要启用一个爬虫的持久化，运行以下命令:
```bush
scrapy crawl baiduSpider -s JOBDIR=crawls/baiduSpider-1
```
然后，你就能在任何时候安全地停止爬虫(按Ctrl-C或者发送一个信号)。恢复这个爬虫也是同样的命令:
```bush
scrapy crawl baiduSpider -s JOBDIR=crawls/baiduSpider-1
```