import scrapy
from HackerNew.items import HackernewItem


def path_append(current_path: str, appended_path: str) -> str:
    """Find child of current path"""
    return current_path+appended_path


class NewsscraperSpider(scrapy.Spider):
    count = 0
    name = 'newsScraper'
    start_urls = ['https://news.ycombinator.com/']
    def parse(self, response):
        item = HackernewItem()
        pair = 1
        
        athing_path = '//tr[@class="athing"]['+str(pair)+']'
        athing_path_sibling = path_append(athing_path, '/following::tr[1]')
        while(bool(response.xpath(athing_path)) is not False):
            item['id_post'] = response.xpath(
                path_append(athing_path, '/@id')).extract_first()
            athing_path = '//tr[@class="athing"]['+str(pair)+']'
            item['rank'] = response.xpath(path_append(
                athing_path, '/td/span[@class="rank"]/text()')).extract_first()
            item['title'] = response.xpath(path_append(
                athing_path, '/td/a[@class="storylink"]/text()')).extract_first()
            item['link'] = response.xpath(path_append(
                athing_path, '/td/a[@class="storylink"]/@href')).extract_first()
            if(response.xpath(path_append(athing_path_sibling,
                                                           '/td/span[@class="score"]/text()')).extract_first() is not None):
                item['point'] = response.xpath(path_append(athing_path_sibling,
                                                           '/td/span[@class="score"]/text()')).extract_first()
            else:
                item['point'] = "None"
            if(response.xpath(path_append(athing_path_sibling,
                                                          '/td/a[@class="hnuser"]/text()')).extract_first() is not None):
                item['user'] = response.xpath(path_append(athing_path_sibling,
                                                          '/td/a[@class="hnuser"]/text()')).extract_first()
            else:
                item['user'] = "Unknown"
            if(response.xpath(path_append(
                    athing_path_sibling, '/td/span[@class="age"]/a/text()')).extract_first() is not None):
                item['time_post'] = response.xpath(path_append(
                    athing_path_sibling, '/td/span[@class="age"]/a/text()')).extract_first()
            else:
                item['time_post'] = "Unknown"
            if(response.xpath(path_append(athing_path_sibling,
                                                             '/td/a[3]/text()')).extract_first() is not None):
                item['comment'] = response.xpath(path_append(athing_path_sibling,
                                                             '/td/a[3]/text()')).extract_first().replace("\u00a0", " ")
            else:
                item['comment'] = "None"
            pair += 1
            athing_path = '//tr[@class="athing"]['+str(pair)+']'
            athing_path_sibling = path_append(athing_path, '/following::tr[1]')
            yield item

        nextPage = response.xpath(
            '//tr/td/a[@class="morelink"]/@href').extract_first()

        if (nextPage and self.count<4):
            self.count+=1
            yield response.follow('https://news.ycombinator.com/'+nextPage, callback=self.parse)
        print('Completed')
        pass
