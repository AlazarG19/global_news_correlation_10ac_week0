import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def extract_keywords(word,pattern):
    '''
    a function that can be used to extract domain name from urls
    '''

    matches = re.findall(pattern,word)
    if matches:
        return matches[0]
    else:
        return None 


    ''' 
    a function to extract words from a list 
    '''

    word_list = [str(word) for word in word_list]
    
    # Find all matches in the text using the pattern
    matches = re.findall(pattern, text)
    
    return ",".join(matches) if len(matches) != 0 else np.nan