import minnie
import re


# nhk.name = 'nhk'
# yomiuri.name = 'yomiuri'
# mainichi.name = 'mainichi'

def asahi():
    """Reads front page of Asahi and returns list of article IDs"""
    asahi.name = 'asahi'
    link = 'https://www.asahi.com/'
    afinder = re.compile("articles\/(A\w+|D\w+)\.html")

    soup = minnie.scrape(link,fancy=True)
    alinks = afinder.findall(str(soup)) #Regex capture article codes
    aset = set(alinks) #Reduce to unique set
    articles = list(aset) #Convert back to a list
    # for i in range(len(articles)):
    #     articles[i] = link + articles[i]
    #MAYBE SOMEDAY I can generate links at this level rather than in uniform...
    return articles


def nhk():
    """Reads front page of NHK and returns list of article LINKS"""
    link = 'https://www3.nhk.or.jp/news/'
    afinder = re.compile("\/news\/(html.+html)")

    soup = minnie.scrape(link,fancy=True)
    alinks = afinder.findall(str(soup)) #Regex capture article codes
    aset = set(alinks) #Reduce to unique set
    articles = list(aset) #Convert back to a list
    for i in range(len(articles)):
        articles[i] = link + articles[i]
    return articles

def yomiuri():
    """Reads front page of Yomiuri and returns list of article LINKS"""
    links=[]
    soup = minnie.scrape('https://www.yomiuri.co.jp')
    hs = minnie.scout(soup,'h3',output=False)
    for h in hs:
        atag = h.find_all('a')
        if len(atag) == 1:
            link = atag[0]['href']
            if 'OYT' in link and 'www.yomiuri' in link:
                links.append(link)
    lset = set(links)
    articles = list(lset)
    return articles

def mainichi():
    """Reads front page of Mainichi and returns list of article IDs"""
    soup = minnie.scrape('https://mainichi.jp')
    links=[]
    atag = minnie.scout(soup,'a',output=False)
    for a in atag:
        if 'article' in a['href']:
            links.append(a['href'])
    for i in range(len(links)):
        if 'https' not in links[i]:
            links[i] = 'https:'+links[i]
    return links
