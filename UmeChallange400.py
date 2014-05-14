#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import WikiApi as wikiApi
import codecs

#input params
entities = ['Q10709194', 'Q7053360', 'Q3578460', 'Q15980608', 'Q15982300', 'Q10502451', 'Q10526701', 'Q4348256', 'Q10663150', 'Q7881526', 'Q4671458', 'Q4907651', 'Q2000141', 'Q3603778', 'Q3603782', 'Q3289', 'Q10681271', 'Q10674434', 'Q2293110', 'Q10717405', 'Q10478622', 'Q5702508', 'Q10709148', 'Q3374603', 'Q4491003', 'Q10509958', 'Q7944387', 'Q10700597', 'Q2091049', 'Q1228854', 'Q10602562', 'Q10651272', 'Q1144565', 'Q10709207', 'Q10709747', 'Q1654001', 'Q10709162', 'Q7944384', 'Q2261865', 'Q10716747']
startdate = '2014-05-01'
outfile = u'entriesByTime.csv'

#functions straight in like a dirty hack ;)
def oneRun(title, wdApi, dDict, startdate):
    '''getting revision history for a single entity'''
    jsonr = wdApi.httpPOST("query", [('prop', 'revisions'),
                            ('rvprop', 'timestamp|comment'),
                            ('rvlimit', '100'),
                            ('rvend', str(startdate)),
                            ('titles', str(title))])
    
    p = jsonr['query']['pages'].keys()[0]
    revs=jsonr['query']['pages'][p]['revisions']
    
    while 'query-continue' in jsonr.keys():
        jsonr = wdApi.httpPOST("query", [('prop', 'revisions'),
                            ('rvprop', 'timestamp|comment'),
                            ('rvlimit', '100'),
                            ('rvend', str(startdate)),
                            ('rvcontinue', str(jsonr['query-continue']['revisions']['rvcontinue']) ),
                            ('titles', str(title))])
        revs = revs +jsonr['query']['pages'][p]['revisions']
    
    for r in revs:
        if r['comment'].startswith('/* wbsetsitelink-add'):
            lang = r['comment'].split('*')[1].split('|')[1].strip()
            if not lang == 'commonswiki':
                if not r['timestamp'] in dDict.keys():
                    dDict[r['timestamp']] = {'title':title, 'lang':lang, 'time':r['timestamp']}
                else:
                    dDict[r['timestamp']+r['comment']] = {'title':title, 'lang':lang, 'time':r['timestamp']}


#setUp without login
wd_site='https://www.wikidata.org/w/api.php'
user = 'UmepediaChallenge'
reqlimit=50
separator='w'
wdApi = wikiApi.WikiDataApi(wd_site, user)

startdate = startdate+'T00:00:00Z'

dDict={}
for e in entities:
    oneRun(e, wdApi, dDict, startdate)

#print
allTimes = sorted(dDict.keys())
flog = codecs.open(outfile,'w','utf8')
for a in allTimes:
    txt = u'%s|%s|%s' %(dDict[a]['time'], dDict[a]['title'], dDict[a]['lang'])
    flog.write(u'%s\n' % txt)
print u'Totalt %d tillagda språk' % (len(allTimes))
flog.close()
print 'Data written to %s' %outfile


