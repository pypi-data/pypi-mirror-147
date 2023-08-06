import requests
import os
from lxml import etree
import gensim
import random
import numpy as np
import jieba
from .DATA_USE import load_negative, load_positive


class newsSpider:
    def __init__(self, sample_num=-1):
        self.base1 = "https://finance.sina.com.cn/head/finance"


    def getDayUrls(self, date, sample_num=-1):
        url = self.base1 + date + "pm.shtml"
        base = "http://finance.sina.com.cn/"
        response = requests.get(url=url)
        tree = etree.HTML(response.text)
        a_s = tree.xpath("*//a[@href != '']/@href")
        new_a_s = []
        for a in a_s:
            if '.shtml' in a or '.html' in a:
                new_a_s.append(a)
        import random
        random.shuffle(new_a_s)
        curr_index = 0
        valid_a_s = []
        valid_index = 0
        while curr_index < len(a_s) and (sample_num==-1 or sample_num > valid_index):
            url = a_s[curr_index]
            try:
                response = requests.get(url, timeout=0.2)
                response.encoding = self.__findCharSet(response.text)
                tree2 = etree.HTML(response.text)
                p_s = tree2.xpath("*//p")
                texts = []
                for p in p_s:
                    if p.text and len(p.text) > 80:
                        texts.append(p.text)

                if len(texts) > 3:
                    valid_index += 1
                    valid_a_s.append(url)
                curr_index += 1
            except:
                curr_index += 1

        return valid_a_s


    def getDayText(self, date, dir_path, num=-1):
        urls = self.getDayUrls(date, sample_num=num)

        for i in range(1, len(urls)+1):
            with open(dir_path+"/"+date+str(i)+".txt", 'w', encoding="UTF-8") as fp:
                response = requests.get(urls[i-1])
                response.encoding = self.__findCharSet(response.text)
                text = response.text
                p_s = etree.HTML(text).xpath("*//p")
                for p in p_s:
                    if p.text and len(p.text) > 80:
                        fp.write(p.text + "\n")


    def getMonthUrls(self, date, sample_num_each_day=-1):
        import datetime
        # 解析date
        year = eval(date[:4])
        month = eval(date[-1] if date[4] == "0" else date[4:])
        curr_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month+1 if month != 12 else 1, 1)
        dic_urls = {}
        while curr_date < end_date:
            print(curr_date)
            dic_urls[curr_date] = self.getDayUrls(curr_date.strftime("%Y%m%d"), sample_num_each_day)
            curr_date += datetime.timedelta(1)
        return dic_urls


    def getMonthText(self, date, dir_path ,sample_num_each_day=-1):
        dic_url = self.getMonthUrls(date, sample_num_each_day)
        # 开始下载
        for key, value in dic_url.items():
            os.makedirs(dir_path+"/"+key.strftime("%Y%m%d"))
            count = 1
            for day in value:
                with open(dir_path + "/" + key.strftime("%Y%m%d") + '/' + str(count) + ".txt", 'w', encoding="UTF-8") as fp:
                    response = requests.get(day)
                    response.encoding = self.__findCharSet(response.text)
                    text = response.text
                    p_s = etree.HTML(text).xpath("*//p")
                    for p in p_s:
                        if p.text and len(p.text) > 80:
                            fp.write(p.text + "\n")
                count += 1



    def __findCharSet(self, text):
        index1 = text.find('charset')
        text2 = text[index1+8:]
        index2 = text2.find('"')

        return text2[:index2]


class newsAnalyser:
    def __init__(self):
        self.positive_dic = gensim.corpora.Dictionary(load_positive())
        self.negative_dic = gensim.corpora.Dictionary(load_negative())
        for i in self.negative_dic.itervalues():
            jieba.add_word(i)
        for i in self.positive_dic.itervalues():
            jieba.add_word(i)

    def getSentiment(self, dir_path, sample_percent=1):
        file_list = []
        for curDir, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".txt"):
                    file_list.append(os.path.join(curDir, file))
        random.shuffle(file_list)
        file_list = file_list[:len(file_list)*sample_percent]

        num_pos = 0
        num_neg = 0
        for file in file_list:
            with open(file, 'r', encoding="GBK") as fp:
                text_list = fp.readlines()
                for sentence in text_list:
                    pos_trans = self.positive_dic.doc2idx(jieba.lcut(sentence))
                    num_pos += (sum(np.array(pos_trans) != -1))
        for file in file_list:
            with open(file, 'r', encoding="GBK") as fp:
                text_list = fp.readlines()
                for sentence in text_list:
                    neg_trans = self.negative_dic.doc2idx(jieba.lcut(sentence))
                    num_neg += (sum(np.array(neg_trans) != -1))
        return (num_neg * -1 + num_pos) / (num_neg + num_pos)