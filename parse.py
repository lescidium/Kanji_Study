import kanji_lists

KANJI = kanji_lists.JLPT

def jukugo(gomi,listy,prefixs,suffixs):
    """Compiles a list of jukugo from a messy string (gomi) and appends to three categories.

    Make sure there is no kanji sticking together from the webscrape process.
    If you don't scrape and clean properly you will have such things happen."""
    i=0 #Characters
    j=0 #Kanji
    k=0 #Words
    while i < len(gomi):
        if gomi[i] in KANJI:
            j+=1
            kotoba = gomi[i]
            while gomi[i+1] in KANJI:
                kotoba = kotoba + gomi[i+1] #grab leading kanji until the chain stops
                i+=1
            if len(kotoba) > 1:
                j+=(len(kotoba)-1) #count each kanji you inlcuded in the word for the kanji counter
                k+=1
                if len(kotoba) == 2:
                    listy.append(kotoba)
                elif len(kotoba) == 3:
                    prefixs.append(kotoba[0]) #Take leading and following kanji for pre/suf research
                    suffixs.append(kotoba[2])
                    #These are 99% true suf/pre (you might have a weird kunyomi suffix like 接種済み)
#CAUTION: This (below) is sketchy. You might be splitting up real idioms possibly...
                elif len(kotoba) == 4:
                    listy.append(kotoba[:2])
                    listy.append(kotoba[2:])
                    k+=1 #count an extra word cause you split a 四字熟語 into two 熟語
###################################################################################
                elif len(kotoba) == 5:
                    prefixs.append(kotoba[0]) #Again taking for pre/suf research
                    suffixs.append(kotoba[4])
                    #From a random sample of 10, 60% were true pre/suf (other 4 had pre/suf in the middle)
        i+=1
    return ((i,j,k),listy,prefixs,suffixs)
