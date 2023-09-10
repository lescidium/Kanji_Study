import minnie
import re
import numpy as np
import pandas as pd

JITEN = 'https://kanjitisiki.com/busyu/yomi.html'

def get_all():
    """Compiles a list of webpages for all Japanese radicals."""

    listy=[]
    href = re.compile('href=\"(.*?)\"')
    soup = minnie.scrape(JITEN)
    bushu = minnie.scout(soup,'li',output=False)
    for b in bushu:
        if '-' in b.text:
            listy.append([b.text,href.findall(str(b))[0]])

    Lray = np.array(listy).T
    links = pd.DataFrame(Lray[1],index=Lray[0],columns=['Links'])
    links = links.drop_duplicates()
    return links


def get_joyo(link,verbose=0):
    """Returns a list of all Joyo kanji for a given Bushu.

    Verbose 1: Returns Bushu name and number of Joyo
    Verbose 2: Additionally returns each Joyo and their link"""
    soup = minnie.scrape(link)
    joyo = minnie.scout(soup,'li',tagclass='zyouyou',output=False)
    if verbose == 1:
        jibun = minnie.scout(soup,'h1',output=False)[0]
        print(jibun.text,f"Number of Joyo: {len(joyo)}")
    if verbose ==2:
        jibun = minnie.scout(soup,'h1',output=False)[0]
        print(jibun.text,f"Number of Joyo: {len(joyo)}")
        href = re.compile('href=\"(.*?)\"')
        for j in joyo:
            print(j.text,href.findall(str(j))[0])
#Convert to a list cause the Jiten links for kanji aren't that useful.
    for j in range(len(joyo)):
        joyo[j] = joyo[j].text
    return joyo
