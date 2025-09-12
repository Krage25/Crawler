import re
def remove_hashtags(text):
    return re.sub(r'#', '',text)