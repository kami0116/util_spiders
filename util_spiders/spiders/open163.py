import scrapy
import re
import os
from ..items import FileItem


# scrapy crawl open163 -a url=https://open.163.com/newview/movie/free?pid=AEUPUHOR7&mid=NEUPUHOS0 -a d=.
class Open163(scrapy.Spider):
    name = 'open163'

    def __init__(self, url=None, d='.', **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [url]
        self.directory = os.path.abspath(d)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def parse(self, response):
        data = re.search('return ({.+})', response.xpath("//script[not(@src)]")[0].get()).group(1)
        movieList = re.search('moiveList(.+),\s*isStore', data).group(1)
        ml = re.findall('{.*?title:\"?(cl|[^\"]+)\"?.*?mp4HdUrl:\"(.+?)\".*?}', movieList)
        cl = response.xpath('//div[@class="t-container__title"]/text()').get()
        index = 0
        for title, mp4Url in ml:
            index += 1
            if title == 'cl':
                title = cl
            yield scrapy.Request(mp4Url.encode('utf-8').decode('unicode_escape'), self.downloadMp4,
                                 meta={'path': os.path.join(self.directory, f'{index:02}.{title}.mp4')})

    def downloadMp4(self, response):
        return FileItem(path=response.meta['path'], context=response.body)
