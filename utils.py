import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def process(transcript: str) -> list:
    """
    Intorior processing of the text
    """
    trans = [x.strip().replace('\t',' ') for x in transcript.split('\n')]
    trans = [x.strip() for x in trans]
    trans = [x for x in trans if x != '' and not x.isdigit() and len(x)>=8 and not x[0].isdigit()]
    trans = [re.sub(r'\((.*?)\)','',x) for x in trans]
    trans = [re.sub('Prof. Dawkins', 'Prof. Richard Dawkins', x) for x in trans]
    trans = [re.sub('Professor', 'Prof.', x) for x in trans]
    trans = [x for x in trans if not re.findall('thesis:', x.lower())]
    return trans

def clean(tekst: str) -> list:
    """
    Remove thrashes from text
    """
    temp = re.sub("\s{2,}", " ", tekst)
    temp = re.sub("(\r\n|\r|\n)", " ", temp) 
    temp = temp.lower() 
    temp = re.sub("&amp", "", temp) 
    temp = re.sub("#[a-z,A-Z]*", "", temp)
    temp = re.sub("@\w+", "", temp) 
    temp = re.sub("(f|ht)(tp)([^ ]*)", "", temp) 
    temp = re.sub("http(s?)([^ ]*)", "", temp)
    temp = re.sub("[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", " ", temp) 
    temp = re.sub("\d", "", temp) 
    temp = re.sub("\s{2,}", " ", temp) 
    temp = re.sub("”|‘|“|’|''",'',temp)
    temp = temp.replace('"', "")
    temp = temp.replace('doesnt', "does not")
    temp = temp.strip()
    return temp

def gather(word_list: list, start_with: str, end_with: list) -> list:
    """
    Extract proper statements
    """
    Gather: list = []
    allowed: bool = False
    
    for sentence in word_list:
        
        if sentence == start_with:
            allowed = True
            
        if sentence in end_with:
            allowed = False
            
        if allowed:
            Gather.append(sentence)
            
    return [x for x in Gather if x != start_with]


def get_bag(pairs: list, limit: int = None) -> dict:
    """
    Get clean bag of words
    """
    tmp = clean(' '.join( pairs))
    
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    tmp =  tmp.split(' ')
    
    tmp = [x for x in tmp if x not in stop_words]
    tmp = [lemmatizer.lemmatize(x, ) for x in tmp]
    tmp = [x for x in tmp if len(x)>2]
    
    additional_stop_words = ['would','say','cannot','doesnt']
    
    tmp = [x for x in tmp if x not in additional_stop_words]
    
    bow = {term: tmp.count(term) for term in set(tmp)}
    
    if limit is None:
        bow_sort = {unikat: liczba for unikat, liczba in sorted(bow.items(), key=lambda el: el[1])} 
    elif isinstance(limit, int):
        bow_sort = {unikat: liczba for unikat, liczba in sorted(bow.items(), key=lambda el: el[1])[-limit:]} 
    else:
        raise ValueError('limit not in [None, int]')
        
    return bow_sort