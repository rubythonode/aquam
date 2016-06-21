# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from blog.models import Gallery, Image, Categorys

class NaverScraperPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    #몰라 예제에있던거
    def process_item(self, item, spider):

        if item.django_model == Categorys:
            if item.django_model.objects.filter(name=item['name']).count() == 0:        #카테고리 중복확인
                item.save()
        elif item.django_model == Image:
            gallery_id = item.django_model.gallery_id
            item.django_model.gallery_id = Gallery.objects.filter(title=gallery_id)[0].id
            files = item['file']
            for file in files:
                item['file'] = file
                if item.django_model.objects.filter(file=item['file']).count() == 0:    #이미지 중복확인
                    item.save()
        elif item.django_model == Gallery:
            categorys = item['categorys']
            item['categorys'] = Categorys.objects.filter(name=categorys)[0].id
            if item.django_model.objects.filter(title=item['title']).count() == 0:    #게시글 중복확인
                item.save()
        return item
