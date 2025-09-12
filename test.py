from utilities.LanguageTranslator import languageTranslator

def translateKeyword(keyword_):
    try:
       received_keyword = languageTranslator(keyword_)
       return received_keyword
    except:
        return keyword_
    

translateKeyword("রাহুল গান্ধী")