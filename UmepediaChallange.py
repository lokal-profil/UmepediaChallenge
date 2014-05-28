#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# By: André Costa, Wikimedia Sverige
# License: MIT
# 2014
import WikiApi as wikiApi
import codecs

#input params
entities = ['Q10709194', 'Q7053360', 'Q3578460', 'Q15980608', 'Q15982300', 'Q10502451', 'Q10526701', 'Q4348256', 'Q10663150', 'Q7881526', 'Q4671458', 'Q4907651', 'Q2000141', 'Q3603778', 'Q3603782', 'Q3289', 'Q10681271', 'Q10674434', 'Q2293110', 'Q10717405', 'Q10478622', 'Q5702508', 'Q10709148', 'Q3374603', 'Q4491003', 'Q10509958', 'Q7944387', 'Q10700597', 'Q2091049', 'Q1228854', 'Q10602562', 'Q10651272', 'Q1144565', 'Q10709207', 'Q10709747', 'Q1654001', 'Q10709162', 'Q7944384', 'Q2261865', 'Q10716747']
outfile = u'statistik.csv'

#setUp without login
wd_site='https://www.wikidata.org/w/api.php'
user = 'UmepediaChallenge'
scriptidentify = 'UmepediaChallenge/1.0'
reqlimit=50
separator='w'
wdApi = wikiApi.WikiDataApi(wd_site, user, scriptidentify)

jsonr = wdApi.httpPOST("wbgetentities", [('props', 'sitelinks/urls'),
                            ('ids', '|'.join(entities).encode('utf-8'))])
#deal with problems
if not jsonr['success'] == 1:
    print 'Some went wrong'

dDict = {}

#all is good
pages = jsonr['entities'] #a dict
total = 0
allLang = []
for k, v in pages.iteritems():
    l = {}
    label = v['sitelinks']['svwiki']['title']
    for s, sv in v['sitelinks'].iteritems():
        if not s.endswith('wiki') or s.startswith('commons'): continue
        l[s[:-4]] = sv['url']
        allLang.append(s[:-4])
        total += 1
    dDict[k] = {'num':len(l), 'label':label, 'sites':l.copy()}

allLang = list(set(allLang))
#present
flog = codecs.open(outfile,'w','utf8')
for k, v in dDict.iteritems():
    txt = u'%s|%s|%d|%s' %(k, v['label'], v['num'], '|'.join(sorted(v['sites'].keys())))
    flog.write(u'%s\n' % txt)
print u'Totalt %d artiklar på %d språk' % (total, len(allLang))
flog.write(u'%s' % '|'.join(sorted(allLang)))
flog.close()
print 'Data written to %s' %outfile

