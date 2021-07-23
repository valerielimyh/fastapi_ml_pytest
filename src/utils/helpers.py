import re

def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().replace("/", " ").strip())

    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in lst_stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
#     if flg_stemm == True:
#         ps = nltk.stem.porter.PorterStemmer()
#         lst_text = [ps.stem(word) for word in lst_text]
                
#     ## Lemmatisation (convert the word into root word)
#     if flg_lemm == True:
#         lem = nltk.stem.wordnet.WordNetLemmatizer()
#         lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## back to string from list
    text = ", ".join(lst_text)
    return text



    