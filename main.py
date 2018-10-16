# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:25:07 2018

@author: j.klen
"""

import pymongo

from myscraper import scrape_useragents, scrape_proxies, scrape_topreality_links, TopRealityAd
from proxypool import proxy_pool_test, proxyPool

myclient = pymongo.MongoClient('mongodb://localhost:27017')
scrapedb = myclient['scrapedb']
adcollection = scrapedb['ads']
adcollection_rmetrics = scrapedb['rmetrics']
adcollection_poolmetrics = scrapedb['poolmetrics']

# explore/exploit proxies

#   do not sample worst proxies
#   change epsilon-greedy, weighted exploration
#   thompson sampling
#   adapt wait() to proxies speed
#   why some responses have higher time than specified timeout???

#   streaming plots, some dashboard
#       histogram of all proxies response times within all bandits
#       bar chart 
#       mean change of proxies position within pool, overall, in some intervals
#       ratio successful request nr./all requests nr, overall, in some intervals
#       number of successful, unsuccesfull, total requests overall
#       number of links and pictures successfuly scraped
#       % of not usable proxies
#       proxy performance on map by countries, webs

#   minimum example af axes reset bug

#   nr. of links scraped, also %
#   nr. of deleted (not scraped) links
#   nr. of pictures scraped (saved) if any
#   map of which property triggers which callbacks
#   when I change a property with one callback will it trigger another?
#   limit amount of data and put it to hidden div, only few charts will query all data

#   bandits
#       bandit means ok, medians - line chart
#       how many times each bandit was chosen - bar chart ok
#       see the means of proxies inside each bandit - grouped barchart
#       click on proxy bar - stat for clicked proxy (need to get also country, type- elite, transparent, ..., declared speed of proxy, server from which it was scraped)

#   one column with prompts: button to start/stop refresh, moving average as inputbox, X axis type checkbox
#       which will be generated dynamically depending on which tab is clicked

#   link to rmetrics collection

if __name__ == '__main__':
    
    browser_list = scrape_useragents()
    proxy_list = scrape_proxies()
    proxy_pool = proxyPool(proxy_list, 10, 0.4)
    #pp = proxy_pool_test(proxy_pool, browser_list, 10)
    links = scrape_topreality_links(region = 'bratislavsky kraj', pages_to_scrape = 5)
    for i, link in enumerate(links):
        print('Scraping link %d of %d' %(i, len(links)))
        ad = TopRealityAd(link, proxy_pool, browser_list)
        ad.scrape_all(savepics = False)
        proxy_pool = ad.proxy_pool
        proxy_pool.writetodb_poolmetrics(adcollection_poolmetrics, sum(ad.attempts))
        ad.writetodb(adcollection)
        ad.writetodb_rmetrics(adcollection_rmetrics)