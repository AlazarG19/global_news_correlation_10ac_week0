from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import pandas as pd

def pre_process(text):
    
    stopwords_set = set(stopwords.words('english'))
    stop = stopwords_set
    
    exclude = set(string.punctuation)
    
    lemma = WordNetLemmatizer()
    
    stop_free = " ".join([i for i in text.lower().split() if i not in stop])
    punc_free = "".join([l for l in stop_free if l not in string.punctuation]) 
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def extract_similarity(df,feature_1,feature_2,new_feature,ngram_range=(1,2),min_df=0.0,analyzer="word"):
    tf = TfidfVectorizer(analyzer=analyzer, ngram_range=ngram_range, min_df=min_df, stop_words='english')
    for index,row in df[[feature_1,feature_2]].iterrows():
        feature_1_feature_2 = pd.DataFrame([row[feature_1],row[feature_2]])
        
        tf_feature_1_feature_2_matrix = tf.fit_transform(feature_1_feature_2[0])
        
        feature_1_feature_2_keywords = tf.get_feature_names_out()
        
        sim = cosine_similarity(tf_feature_1_feature_2_matrix, tf_feature_1_feature_2_matrix)
        
        df.loc[index, new_feature] = sim[0][1] 