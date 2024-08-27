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
    
def find_words_from_list(text, word_list,pattern):
    ''' 
    a function to extract words from a list 
    '''

    word_list = [str(word) for word in word_list]
    
    # Find all matches in the text using the pattern
    matches = re.findall(pattern, text)
    
    return ",".join(matches) if len(matches) != 0 else np.nan

def creating_region(country,region_list):
    '''
    a function that can be used to identify the region for the specified country
    '''
    for key,value in region_list.items():
        if country in value:
            return key
    return "other"

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

def barchart(x_axis, y_axis,  x_label,y_label, title,orientation,figsize=(18,6)):
    ''' 
    a function to attain the barchart for dataframes that don't need to 
    be grouped before plotting
    '''
    plt.figure(figsize=figsize)
    plt.title(title)
    
    if orientation == 'vertical':
        sns_plot = sns.barplot(x=x_axis, y=y_axis)
        sns_plot.set_xticklabels(sns_plot.get_xticklabels(), rotation=45, horizontalalignment="right")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    elif orientation == 'horizontal':
        plt.barh(x_axis, y_axis)
        plt.xlabel(y_label)
        plt.ylabel(x_label)
        plt.yticks(x_axis)
    else:
        raise ValueError("Invalid orientation. Choose 'vertical' or 'horizontal'.")

def barchart_with_grouping(df, x_axis, y_axis, title,  x_label, y_label,orientation, top=10, ascending=True, grouping="", figsize=(18,6)):
    ''' 
    a function to attain the barchart for dataframes that need to 
    be grouped before plotting
    '''
    
    if grouping == "":
        grouped = df.groupby(x_axis).count()
        sorted_df = grouped.sort_values(by=y_axis,ascending=ascending)
        
        barchart(x_axis=sorted_df.index[:top], y_axis=sorted_df[y_axis][:top], figsize=figsize ,  x_label=x_label,y_label=y_label, title=title,orientation=orientation)
    else:
        grouped = df.groupby(x_axis).agg(Count=(grouping, 'count')).reset_index()
        sorted_df = grouped.sort_values(by="Count",ascending=ascending)
    
        barchart(x_axis=sorted_df[x_axis][:top], y_axis=sorted_df[y_axis][:top], figsize=figsize ,  x_label=x_label,y_label=y_label, title=title,orientation=orientation)

def grouped_barchart(df, legend,title, x_label,y_label,orientation, figsize=(18,6)):
    ''' 
    a function to attain the group barchart for dataframes that don't need to 
    be grouped before plotting
    '''
    
    if orientation == 'vertical':
        df.plot(kind='bar', stacked=False, colormap='viridis', ax=plt.gca())
    elif orientation == 'horizontal':
        df.plot(kind='barh', stacked=False, colormap='viridis', ax=plt.gca())
    else:
        raise ValueError("Invalid orientation. Choose 'vertical' or 'horizontal'.")

    plt.title(title)

    plt.ylabel(y_label)
    plt.xlabel(x_label)

    plt.legend(title=legend)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout();

def line_graph(x_axis,y_axis,x_label,y_label,title):
    plt.plot(x_axis, y_axis, marker='o')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()