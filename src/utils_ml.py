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
        
def sort_coo(coo_matrix):
    """Sort a dict with highest score"""
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []
    
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature, score
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def get_keywords(vectorizer, feature_names, docs, TOP_K_KEYWORDS):
    """Return top k keywords for each doc in the corpus using TF-IDF method"""
    tf_idf_matrix = vectorizer.transform(docs)
    sorted_items = [sort_coo(tf_idf_vector.tocoo()) for tf_idf_vector in tf_idf_matrix]
    keywords = [extract_topn_from_vector(feature_names, sorted_items[i], TOP_K_KEYWORDS) for i in range(len(docs))]
    return keywords

def key_word_extractor(data):
    """ Fetching the dataframe ,generating the keywords column and returning it as a list"""
    vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True)
    corpora = data.to_list()
    vectorizer.fit_transform(corpora)
    feature_names = vectorizer.get_feature_names_out()

    keywords = get_keywords(vectorizer, feature_names, corpora, 10)
    result = [{'top_keywords': list(keywords[i].keys())} for i, doc in enumerate(corpora)]
    final = pd.DataFrame(result)
    return final

def categorize_headlines(headlines, tags):
    """ Function to categorize the headlines into tags """
    categories = []
    for headline in headlines:
        headline = headline.lower()
        headline_tags = []


        for tag, keywords in tags.items():
            if any(keyword in headline for keyword in keywords):
                headline_tags.append(tag)

        if not headline_tags:
            headline_tags.append("Other")

        categories.append(', '.join(headline_tags))

    return categories