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

def pie_chart(title,labels,count):
    ''' 
    a function to create a piechart
    '''
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    print(count)
    print(labels)
    plt.pie(x=count, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.show()
    
def histogram(data,x_axis,title,x_label,y_label,figsize=(8,6),bins=50):
    plt.figure(figsize=figsize)
    sns.histplot(data=data,bins=bins,x=x_axis)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()