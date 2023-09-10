import minnie
import kanjify
#At some point I would like to implement kanjiy.do here instead of these specific loops for each.


def asahi(article):
    """Reads article pages of Asahi and formats into standard gomi."""

    soup = minnie.scrape(f"https://www.asahi.com/articles/{article}.html",fancy='True')
    if soup == None:
        return None
    para = minnie.scout(soup,'p',output=False)

    gomi = ''
    for p in para:
        gomi = gomi + p.text + 'A' #A is a placeholder character so that kanji don't stick together

    gomi = gomi.replace('\u3000','A')
    return gomi

def nhk(link):
    """Reads article pages of NHK and formats into standard gomi."""
    gomi=''
    soup = minnie.scrape(link,fancy=True)
    para = minnie.scout(soup,'p')
    body = minnie.scout(soup,'div',tagclass='body-text')

    for p in para:
        if 'summary' in p.attrs['class'][0]:
            gomi = gomi + p.text
    for b in body:
        gomi = gomi + b.text
    gomi = gomi.replace('\u3000','A')
    return gomi

def yomiuri(link):
    """Reads article pages of Yomiuri and formats into standard gomi."""
    gomi =''
    soup = minnie.scrape(link)
    para = minnie.scout(soup,'p')
    for p in para:
        if 'class' in p.attrs:
            if 'par' in p.attrs['class'][0]:
                gomi = gomi + p.text
    gomi = gomi.replace('\u3000','A')
    return gomi

def mainichi(link):
    """Reads article pages of Mainichi and formats into standard gomi."""
    gomi = ''
    soup = minnie.scrape(link)
    para = minnie.scout(soup,'p')
    for p in para:
        if len(p.attrs) == 0:
            gomi = gomi + p.text
    gomi = gomi.replace('\u3000','A')
    return gomi
