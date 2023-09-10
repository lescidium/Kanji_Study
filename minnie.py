"""General non-specific code."""
import re
import urllib.request as ur
from urllib.error import HTTPError
import pandas as pd
from bs4 import BeautifulSoup
from socket import timeout


def list2_DF(tier):
    "Turns messy 2D list into neat DF"

    array = np.array(tier,dtype=object).T
    df = pd.DataFrame(array[1:3][:].T,index=array[0][:],columns=['Count','List'])
    df = df.sort_values('Count',ascending=False)
    return df


def scrape(url,fancy=False):
    """Scrapes a messy soup object from any url.

    I recommend using control+F on the output of this function to find the data you are looking for.
    Then you can see what tag it's associated with. (Alternatively, code something up with RegEx)
    Then use the scout function to find the index positioning of that data.

    If you wanna work manually you can use: soup.find_all(tag) and I'm sure it will all come back to you.

    I'm thinking about implementing a potentially infinite retry loop  for the read request.
    As long as the user continues to ask Minnie to try again, she will.

    Right now it's a completely messy double-take, only included in Fancy=false"""

    if fancy == False:
        try:
            read = ur.urlopen(url,timeout=2).read()       #Reads a whole big string mess
        except timeout:
            print('Wanna try connecting again?')
            ans = input()
            if ans == 'y':
                try:
                    read = ur.urlopen(url,timeout=2).read()
                except timeout:
                    return None
            else:
                return None
        except HTTPError:
            print('HTTPError... Exiting minnie.scrape')
            return None
        soup = BeautifulSoup(read,'lxml')   #Transforms string mess intro workable object: Soup
    else:
        req = ur.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            read = ur.urlopen(req,timeout=3).read()       #Reads a whole big string mess
        except timeout:
            return None
        except HTTPError:
            print('HTTPError... Exiting minnie.scrap')
            return None
        soup = BeautifulSoup(read,'lxml')   #Transforms string mess intro workable object: Soup
    return soup

def scout(soup,tag,output=False,tagclass=None):
    """Scouts messy soup for your tag of choice and places an index by each one.

    Here a several common tags: div, td, script, tr.
    tr  --> Tables
    div --> Macroscopic resolution
    td  --> Microscopic resolution
    script --> Volatile page elements
    This function returns the results list."""
    if tagclass == None:
        result = soup.find_all(tag)
    else:
        result = soup.find_all(tag,{"class":tagclass})

    if output == True:
        i=0
        for r in result:
            print(i,len(r.text),r.text)
            i+=1
    return result
