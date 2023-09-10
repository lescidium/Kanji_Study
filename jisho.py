import minnie
import numpy as np
import pandas as pd
import urllib as ur

# CLS_div = minnie.scout(soup,'div',tagclass='concept_light-status')
# #This is a call for the tags and the word

# DFN_span = minnie.scout(FULL_div[0],'span',tagclass='meaning-meaning')
# #This is a call for the definitions of a single div

# LBL_span = minnie.scout(soup,'span',tagclass='label')
# #This is a direct call to the tags, DOES NOT contain the entry itself

# FULL_div = minnie.scout(soup,'div',tagclass='clearfix')
# #This tag class will also net you the definitions, tags, and the word...

def kanji_tag_count(kanji,verbose=0):
    """Counts all tags on first page results for a given kanji (sandwich asterisks).

    Specially ignores entries where the kanji is not in the main text entry.
    This is called a mistmatch.

    Verbose 1: See output for minnie's label scouting
    Verbose 2: See scouting output AND mistmatches."""

    jisho = 'https://jisho.org/search/'+ur.parse.quote(f"*{kanji}*")
    soup = minnie.scrape(jisho)
    if soup == None:
        print(f"Timeout on {kanji}")
        return None
    FULL_div = minnie.scout(soup,'div',tagclass='clearfix')
    C=N1=N2=N3=N4=N5=WK=0
    inds = {'Common word':C,'Wanikani':WK,"N5":N5,"N4":N4,"N3":N3,"N2":N2,"N1":N1}
    if verbose == 2:
        o = [True,True]
    elif verbose == 1:
        o = [True,False]
    else:
        o = [False,False]

    for cfx in FULL_div:
        entry = minnie.scout(cfx,'span',tagclass='text')
        if len(entry) > 0:
            entry = entry[0].text
            if kanji in entry:
                labels = minnie.scout(cfx,'span',tagclass='label',output=o[0])
                for l in labels:
                    for i in inds:
                        if i in l.text:
                            inds[i]+=1
                            break
            elif o[1] == True:
                print(f"{kanji} was not listed as the main kanji in {entry}")
    return inds

def kanji_readings(kanji):
    jisho = 'https://jisho.org/search/'+ur.parse.quote(f"{kanji}")
    soup = minnie.scrape(jisho)
    kun_div = minnie.scout(soup,'div',tagclass='kun readings',output=False)

    if len(kun_div) > 0:
        listy = minnie.scout(kun_div[0],'span',tagclass='japanese_gothic',output=False)
        readings=[]
        for l in listy:
            entry = l.text
            if '.' in entry:
                i=0
                for e in entry:
                    if e == '.':
                        word = entry[:i]
                    i+=1
            else:
                word = entry
            word = word.replace('-','')
            word = word.replace('、','')
            word = word.replace(' ','')
            readings.append(word)

        setty = set(readings)
        kuns=''
        for s in setty:
            kuns+=f"{s},"  
        kuns = kuns[:len(kuns)-1]
    else:
        kuns=None

    on_div = minnie.scout(soup,'div',tagclass='on readings',output=False)
    
    if len(on_div) > 0:

        ons = on_div[0].text.replace('On:','')
        ons = ons.replace('\n','')
        ons = ons.replace(' ','')
        ons = ons.replace('、',',')
    else:
        ons=None
    return (kuns,ons)

def kanji_meaning(kanji):
    """Returns a list of meanings for a given ONE kanji."""

    if len(kanji) > 1:
        raise ValueError('Please pass only one Kanji')
    jisho = 'https://jisho.org/search/'+ur.parse.quote(f"{kanji}")
    soup = minnie.scrape(jisho)
    meaning_div = minnie.scout(soup,'div',tagclass='meanings english sense',output=False)

    words=''
    for w in minnie.scout(meaning_div[0],'span',output=False):
        words += w.text.replace(', ',',')
    return words

def kanji_tag_table(listy,verbose=0):
    """Turns a list of kanji into a table with Jisho tag counts for each kanji.

    Verbose 1: Print each output of tag count"""

    if type(listy[0]) is not str:
        raise TypeError(f"'You need to pass a list of Kanji. You're giving me @@@{type(listy[0])}@@@ instead of strings.'")

    i=0
    k=0
    table=[]
    for l in listy:
        kanji = l
        inds = kanji_tag_count(kanji)
        if inds != None:
            i += 1
            score = grade(inds)
            table.append([kanji,inds['Common word'],inds['Wanikani'],
                           inds['N5'],inds['N4'],inds['N3'],inds['N2'],inds['N1'],score])
            if verbose == 1:
                print(f"Finished kanji: {kanji}, at iter {i}/{len(listy)}. Dict: {inds}")
        else:
            k+=1
            i+=1


    #table.sort(reverse=True)
    kan = np.array(table).T[0]
    col=[]
    for i in inds:
        col.append(i)
    col.append('Score')
    df = pd.DataFrame(table,index=kan)
    df.pop(0)
    df.columns=col
    df = df.sort_values('Score',ascending=False)
    print(f"{k} issues with timeouts")
    return df

def grade(inds):
    value = inds['Common word']/20+(inds['Wanikani']+
             inds['N5']*5+inds['N4']*4+inds['N3']*3+
             inds['N2']*2+inds['N1'])/10
    return round(value,2)

def tango_meaning(tango):
    """Returns list of meanings for a given word.

    Each element in list contains a list of words separated by semi-colons
    CAUTION: This method indexes the first entry on the page.
    This shouldn't be an issue because...
    Why wouldn't the dictionary return the thing you search as the first entry?"""
    jisho = 'https://jisho.org/search/'+ur.parse.quote(f"{tango}")
    soup = minnie.scrape(jisho)
    FIRST_div = minnie.scout(soup,'div',tagclass='clearfix',output=False)[0]

    meanings =[]
    for m in minnie.scout(FIRST_div,'span',tagclass='meaning-meaning',output=False):
        meanings.append(m.text)

    return meanings
