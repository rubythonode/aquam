from gc import get_objects

import scrapy
import urllib.request

from PIL import Image
from naver_scraper.items import NaverScraperItem, ImageItem, CategorysItem
from django.conf import settings


class NaverBlogSpider(scrapy.Spider):
    name = "naverblog"
    allowed_domains = ["naver.com"]
    start_urls = [
        "http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage=9999",
    ]


    def parse(self, response):
        # find form and fill in
        # call inner parse to parse real results.
        num = int(response.xpath("//table[@class='page-navigation']/tr/td[@class='cnt']/a/text()").extract()[-1])
        for idx in range(1, num+1):
            request = scrapy.FormRequest("http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage="+ str(idx), callback=self.parse_blog)
            yield request

    def parse_blog(self, response):
        galleryItem=[]

        # 스마트 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                galleryItem = NaverScraperItem()
                categorysItem = CategorysItem()
                imageItem = ImageItem()
                galleryItem['title'] = e.xpath("..//h3/text()[2]").extract()[0]
                smart_body = e.xpath("..//div[@class='se_component_wrap sect_dsc __se_component_area']").extract()[0]
                galleryItem['detail'] = self.parse_download_image(smart_body)
                galleryItem['created_date'] = e.xpath("..//span[@class='se_publishDate pcol2 fil5']/text()").extract()[0].split('\n')[0].replace('.', '-', 2).replace('.', '')
                categorysItem['name'] = e.xpath("..//a[@class='pcol2']/text()").extract()[0]
                galleryItem['categorys'] = categorysItem['name']
                yield categorysItem
                yield galleryItem
                imageItem['gallery'] = galleryItem['title']
                imageItem['file'] = self.parse_image_url(e.xpath("..//div[@class='se_component_wrap sect_dsc __se_component_area']").extract()[0])
                yield imageItem
            except:
                continue

        # 일반 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                galleryItem = NaverScraperItem()
                categorysItem = CategorysItem()
                imageItem = ImageItem()
                galleryItem['title'] = e.xpath("..//span[@class='pcol1 itemSubjectBoldfont']/text()[1]").extract()[0]
                normal_body = e.xpath("..//div[@id='postViewArea']").extract()[0]
                galleryItem['detail'] = self.parse_download_image(normal_body)
                galleryItem['created_date'] = e.xpath("..//p[@class='date fil5 pcol2 _postAddDate']/text()").extract()[0].replace('.', '-', 2).replace('.', '')
                # YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] 형식이어야 합니다
                categorysItem['name'] = e.xpath("..//a[@class='pcol2']/text()").extract()[0]
                galleryItem['categorys'] = categorysItem['name']
                yield categorysItem
                yield galleryItem
                imageItem['gallery'] = galleryItem['title']
                imageItem['file'] = self.parse_image_url(e.xpath("..//div[@id='postViewArea']").extract()[0])
                yield imageItem
            except:
                continue

        return galleryItem

    def parse_download_image(self, response):
        # url = "http://postfiles1.naver.net/20141204_160/kdk926_14176651128371lr8c_JPEG/20141203_110254.jpg?type=w2"
        # file_name = 'D:/workspace/DjangoProjects/BlogWorkspace/aquam/media/images/abcd.jpg'
        download_local_url = 'D:/workspace/DjangoProjects/BlogWorkspace/aquam/media/images/'    #windows test
        # download_local_url = settings.MEDIA_ROOT + '/images/'  #ubuntu
        replace_item = response
        for i in range(0, response.count('src="')):
            temp = response.split('src="')[i+1]
            url = temp.split('"')[0]
            file_name = url.split('/')[-1].split('?')[0].replace('%', '')
            download_url = download_local_url + file_name
            media_url = settings.MEDIA_URL + 'images/' + file_name
            replace_item = str(replace_item).replace(url, media_url)
            if ImageItem.django_model.objects.filter(file='images/' + file_name).count() == 0:    #이미지 중복확인
                urllib.request.urlretrieve(url, download_url)      #이미지 다운로드
        return replace_item

    def parse_image_url(self, response):
        image_list = []
        for i in range(0, response.count('src="')):
            temp = response.split('src="')[i+1]
            url = temp.split('"')[0]
            image_list.append('images/' + url.split('/')[-1].split('?')[0].replace('%', ''))
        return image_list
