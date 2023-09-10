def writeNtrim(freq,name):
    freq.to_excel(f"bushu_freq/{name}.xlsx")
    i=0
    for f in freq.index:
        if freq.loc[f]['Score'] < 1:
            break
        i+=1
    freq = freq[:i]
    return freq

def tier_grader(tier):
    """This is a really weird and specific function that took a pd.DataFrame that had kanji lists for every bushu.

    OOP:
    1) It feeds those list into the Jisho grader
    2) Writes the raw output to excel
    3) Trims low scoring kanji from the list
    4) Calculates statistics for that bushu list
    5) Append stastics as new columns

    This takes like 10 minutes to run...
    Honestly. For a small like of Kanji...
    You should just keep the total count data somewhere and process from there.
    Trying to get a url req each time so so stupid.

    If you are ever worried about re-writing the formula for grading, just put those changes into kanji_tag_table
    """

    scores=[]
    counts=[]
    listy =[]
    i=0
    for t in tier.index:
        print(f"Working on {t}")
        df = jisho.kanji_tag_table(tier.loc[t]['List'],verbose=0) #Generate kanji table for a given bushu
        df_trunc = writeNtrim(df,t) #trim kanji with score less than 1
        scores.append(sum(df_trunc['Score'])) #sum scores of truncated list
        listy.append(list(df_trunc.index))    #trunc ordered list of kanji (order based on individual frequency scores)
        counts.append(df_trunc.shape[0])      #truncated counts after grading truncation
    tier.insert(tier.shape[1],'Summed Score (Trunc)',scores)
    tier.insert(tier.shape[1],'Ordered List',listy)
    tier.insert(tier.shape[1],'Truncated Count',counts)
    eff = tier['Summed Score (Trunc)']/tier['Truncated Count']
    tier.insert(tier.shape[1],'Efficiency',eff)
    tier = tier.sort_values('Summed Score (Trunc)',ascending=False)
    return tier



def pingJisho(kanji):
    """This was used for getting readings for each kanji. Could be repurposed later"""
    link = 'https://jisho.org/search/'+ur.parse.quote(f"{kanji}")

    try:
        soup = minnie.scrape(link)
    except ur.error.URlError:
        print('Wanna try connecting again?')
        ans = input()
        if ans == 'y':
            soup = minnie.scrape(link)
        else:
            return 0,0

    try:
        kun_div = minnie.scout(soup,'div',tagclass='kun readings')
        fstkun = minnie.scout(kun_div[0],'span')[1].text.replace('、 ','')
    except IndexError:
        fstkun = ''
    try:
        on_div = minnie.scout(soup,'div',tagclass='on readings')
        fston = minnie.scout(on_div[0],'span')[1].text.replace('、 ','')
    except IndexError:
        fston = ''
    return (fston, fstkun)
