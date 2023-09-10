import pandas as pd

JOYO = pd.read_excel('graded_joyo.xlsx',index_col=0)
MAX = max(JOYO['Score'])

def grade(setty,invert=False):
    """Collects scores for a given set of kanji.
    
    If a kanji in the set is not present in the scoring database, it will be assumed max difficulty/rarity.
    """
    for s in setty:
        try:
            if invert == True:
                scores.append(kanji_list.loc[k]['Score'])
            else:
                scores.append(MAX-kanji_list.loc[k]['Score'])
        except KeyError:
            if invert == True:
                print(f'{k} not in Kanji list, assigning frequency score of zero.')
                scores.append(0)
            else:
                print(f'{k} not in Kanji list, assigning frequency score of Max={MAX}.')
                scores.append(MAX)
    return scores


#I would love to modify this to consider partial scoring for partially difficult kanji...
#Like something in the seen category would only get reduced partially in its contribution to the difficulty of a set
#But we don't have the structure of that yet, so this is fine as is. It just subtracts sets and runs grade.
def personal(kset,pset,inv=False):
    """Only collects scores for kanji not in one's personal set."""
    for k in kset:
        if k not in pset:
            setty.append(k)
    scores = grade(setty,invert=inv)
    return scores