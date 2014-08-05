#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# By: André Costa, Wikimedia Sverige
# License: MIT
# 2014
#
# known issues:
## if more entities are added (i.e. more than 50 in total) then the API 
## call would have to be slpit into several batches.
import WikiApi as wikiApi
import codecs
from collections import OrderedDict as OrderedDict

#input params
entities = ['Q10709194', 'Q7053360', 'Q3578460', 'Q15980608', 'Q15982300', 'Q10502451', 'Q10526701', 'Q4348256', 'Q10663150', 'Q7881526', 'Q4671458', 'Q4907651', 'Q2000141', 'Q3603778', 'Q3603782', 'Q3289', 'Q10681271', 'Q10674434', 'Q2293110', 'Q10717405', 'Q10478622', 'Q5702508', 'Q10709148', 'Q3374603', 'Q4491003', 'Q10509958', 'Q7944387', 'Q10700597', 'Q2091049', 'Q1228854', 'Q10602562', 'Q10651272', 'Q1144565', 'Q10709207', 'Q10709747', 'Q1654001', 'Q10709162', 'Q7944384', 'Q2261865', 'Q10716747']
statLanguages = ['en', 'de', 'fr', 'es', 'it', 'nl', 'pl', 'ru', 'pt', 'sv', 'zh', 'simple', 'zh-classical', 'no', 'fi', 'hi']
outfile = u'statistik2.csv'

#setUp without login
wd_site='https://www.wikidata.org/w/api.php'
user = 'UmepediaChallengeList'
scriptidentify = 'UmepediaChallengeList/1.0'
reqlimit=50
separator='w'
wdApi = wikiApi.WikiDataApi(wd_site, user, scriptidentify)

jsonr = wdApi.httpPOST("wbgetentities", [('props', 'sitelinks'),
                            ('ids', '|'.join(entities).encode('utf-8'))])
#deal with problems
if not jsonr['success'] == 1:
    print 'Some went wrong'

dDict = OrderedDict()
for l in statLanguages:
    dDict[l] = []

#all is good
pages = jsonr['entities'] #a dict
for k, v in pages.iteritems():
    l = {}
    label = v['sitelinks']['svwiki']['title']
    for s, sv in v['sitelinks'].iteritems():
        if not s.endswith('wiki') or s.startswith('commons'): continue
        lang = s[:-4]
        if not lang in statLanguages: continue
        dDict[lang].append(sv['title'])

#present
flog = codecs.open(outfile,'w','utf8')
flog.write('# Data to be used for statistics via\n# http://wikipediaviews.org/displayviewsformultiplemonths.php\n#\n')
for k, v in dDict.iteritems():
    txt = u'==lang:%s==\n%s\n' %(k, '\n'.join(sorted(v)))
    flog.write(u'%s\n' % txt)
    print u'lang: %s has %d articles' %(k,len(v))
flog.close()
print 'Data written to %s' %outfile

