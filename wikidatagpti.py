# -*- coding: utf-8 -*-
"""wikidata.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gFGar313eLILWfE6l4uDdLCAtfkRWGHK
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install wikidataintegrator
# !pip install wikidata
# !pip install opencc

"""# Code to retrieve English entry name(s) from a Chinese entry name"""

from wikidataintegrator import wdi_core
from wikidata.client import Client
from opencc import OpenCC
t2s = OpenCC('t2s.json')
s2t = OpenCC('t2s.json')

def en2zh(s, lang='en', zhalt=0):
    #if lang in ['zh', 'zh-hant', 'zh-hans']:
    if zhalt == 1:
        s = t2s.convert(s)
    client = Client()
    enList = {}
    search_results = wdi_core.WDItemEngine.get_wd_search_results(s, language=lang)
    person = None
    for qid in search_results:
        person = client.get(qid, load=True)
        en, zh, zh_hant, zh_hans = None, None, None, None
        if 'en' in person.data['labels']:
            en = person.data['labels']['en']['value']
        if 'zh-hant' in person.data['labels']:
            zh_hant = person.data['labels']['zh-hant']['value']
        if 'zh-hans' in person.data['labels']:
            zh_hans = person.data['labels']['zh-hans']['value']
        if 'zh' in person.data['labels']:
            zh = person.data['labels']['zh']['value']
        print(f"{qid}\t[{zh_hant}|{zh}|{zh_hans}]\t{en}")
        if 'zh' in person.data['aliases']:
            aliases = person.data['aliases']['zh']
            print("Other names:")
            for a in aliases:
                print(f"  {a['value']}")
        if 'en' in person.data['aliases']:
            aliases_ed = person.data['aliases']['en']
            for a in aliases_ed:
                print(f"  {a['value']}")
        if 'zh' in person.data['descriptions']:
            desc = person.data['descriptions']['zh']['value']
            print(f"[Note] {desc}")
        print('-'*50)
        enList[qid] = (zh, en)
    return person, enList

def zh2en(s, zhalt):
    return en2zh(s, lang='zh-hant', zhalt=zhalt)


if __name__ == "__main__":
    s = '''
    Howard Taft
    Chinese Exclusion Act
    '''.strip().split('\n')[-1]
    p, L = en2zh(s)
    
    s = '''
    鄒族
    庚款
    八國聯軍
    '''.strip().split('\n')[-1]
    p, L = zh2en(s, zhalt=0)  # zhalt=0 以傳統漢字搜尋；zhalt=1 以簡體漢字搜尋：搜尋結果可能相差很大
    
