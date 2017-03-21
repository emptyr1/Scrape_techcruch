# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from clearmobtest.items import Article

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import re
import collections


class ClearmobtestPipeline(object):
    header = False
    def __init__(self):
        self.data = collections.defaultdict(str)
        self.url = []


    def process_item(self, item, spider):
        'can process items here async'
        print item

        clean_body = self.remove_non_ascii(str(item['body']).encode('utf-8'))
        clean_article_url = self.remove_non_ascii(str(item['url']).encode('utf-8'))
        clean_title_with_html = self.remove_non_ascii(str(item['title']).encode('utf-8'))
        clean_article_title = self.remove_html_tags(clean_title_with_html)

        entities = self.extract_entities_from_articles(clean_body)
        ###
        self.data["company name"] = entities[1:8]
        self.data["company website"] = self.find_urls(str(item['body']))

        self.data["article url"] = clean_article_url
        self.data["article title"] = clean_article_title[1:-1]


        ### WRITE TO CSV ####
        with open("output.csv", "a") as csv_file:
            w = csv.DictWriter(csv_file, self.data.keys())
            if ClearmobtestPipeline.header == False: # Header row
                w.writeheader()
                ClearmobtestPipeline.header = True
            w.writerow(self.data)

        return item

    def extract_entities_from_articles(self, text):
        chunks = ne_chunk(pos_tag(word_tokenize(text)))
        prev = None
        cur_chunk, cont_chunk = [], []
        for i in chunks:
            if type(i) == Tree:
                cur_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif cur_chunk:
                named_entity = " ".join(cur_chunk)
                if named_entity not in cont_chunk:
                    cont_chunk.append(named_entity)
                    cur_chunk = []
        return cont_chunk


    def remove_html_tags(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext


    def find_urls(self, text):
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', text)

        url_string = (', '.join([url for url in urls[:3] if not url.startswith("https://techcrunch") or
                                 not url.startswith("https://crunchbase") or
                                 not url.startswith("https://blog")
                                ]))

        return url_string if url_string else "n/a"


    def remove_non_ascii(self, text):
        x = re.sub(r'[^\x00-\x7f]', r' ', text).strip()
        return x


    def close_spider(self, spider):
        print "Done processing text!"
