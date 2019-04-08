# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 9:44
# @Author  : yueconger
# @File    : dirty_data_clean.py
import os
import re
import json
from lxml import etree


class DirtyDataClean(object):
    """法律文件转txt,法律信息抽取"""
    def html_trans(self, html_dir, txt_dir):
        html_list = os.listdir(html_dir)  # 列出文件夹下所有的目录与文件
        for j in range(0, len(html_list)):
        # for j in range(0, 3):
            html_path = os.path.join(html_dir, html_list[j])
            print(html_path)

            with open(html_path, 'r', encoding='utf-8') as f:
                html_str = f.read()
            tree = etree.HTML(html_str)
            item_list = []
            """标题"""
            law_name = html_path.split('/')[-1].split('.htm')[0]
            # law_name = tree.xpath('//div[@class="law-title"]/text()')[0]
            # law_name = law_name.strip().split('——')[-1]
            # print('——', law_name)
            # law_name = re.sub('法信汇编版', '', law_name)
            # law_name = re.sub('法信', '', law_name)
            item_list.append({'标题': law_name})

            """基本信息"""
            # 属性弹窗
            list_mod = tree.xpath('//div[@class="js-sxTab"]/div/div[@class="nat-listMod"]/ul//li')
            for mod in list_mod:
                item = {}
                name = mod.xpath('./div[1]/text()')[0].strip()
                con = mod.xpath('./div[2]/a/text()')
                if con:
                    item[name] = con[0].strip()
                else:
                    item[name] = mod.xpath('./div[2]/text()')[0].strip()
                item_list.append(item)

            list_mod_fr = tree.xpath('//div[@class="js-sxTab"]/div/div[@class="nat-listMod fr"]/ul//li')
            for mod in list_mod_fr:
                item = {}
                name = mod.xpath('./div[1]/text()')[0].strip()
                con = mod.xpath('./div[2]/a/text()')
                if con:
                    item[name] = con[0].strip()
                else:
                    item[name] = mod.xpath('./div[2]/text()')[0].strip()
                item_list.append(item)
            self.law_info_save(item_list)
            print(law_name, '属性信息保存完毕')

            """正文部分"""
            full_text = tree.xpath('//div[@class="box fulltext"]')[0]
            full_text_str = etree.tostring(full_text, encoding='utf-8').decode()
            full_text_str = re.sub('<!--remark-->|<a .*?>|</a>|<span.*?>|</span>|<br><br>|<div.*?>|<font.*?>|</font>|</div>|<h5>|</h5>', '', full_text_str)
            full_text_str = re.sub('<p.*?>', '', full_text_str)
            full_text_str = re.sub('</p>|<br.*?>', '\n', full_text_str)

            txt_path = txt_dir + law_name + '.txt'
            try:
                with open(txt_path, 'w', encoding='utf-8') as tf:
                    tf.write(full_text_str)
            except:
                file_name = html_path.split('/')[-1].split('.')[0]
                txt_path = txt_dir + file_name + '.txt'
                with open(txt_path, 'w', encoding='utf-8') as tf:
                    tf.write(full_text_str)
            print(law_name, '文件内容保存成功!')

    def law_info_save(self, law_info):
        jsObj = json.dumps(law_info, ensure_ascii=False)
        with open(r'E:\LocalServer\Faxin_Law\地方_法规信息\info_澳门.txt', 'a+', encoding='utf-8') as f:
            f.write(jsObj + '\n')


if __name__ == '__main__':
    dirty_data = DirtyDataClean()
    html_dir = r'E:\LocalServer\Faxin_Law\地方_html\澳门/'
    txt_dir = r'E:\LocalServer\Faxin_Law\地方_txt\澳门/'
    if os.path.isdir(txt_dir):
        print(txt_dir)
    else:
        os.makedirs(txt_dir)
    dirty_data.html_trans(html_dir, txt_dir)
