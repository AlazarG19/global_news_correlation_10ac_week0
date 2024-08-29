from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import pandas as pd

def pre_process(text):
    """
    Pre-processes a given text by removing stopwords, punctuation, and lemmatizing the words.

    Args:
        text (str): The input text to be pre-processed.

    Returns:
        str: The pre-processed text.
    """
    stopwords_set = set(stopwords.words('english'))
    stop = stopwords_set
    
    exclude = set(string.punctuation)
    
    lemma = WordNetLemmatizer()
    
    stop_free = " ".join([i for i in text.lower().split() if i not in stop])
    punc_free = "".join([l for l in stop_free if l not in string.punctuation]) 
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


def extract_similarity(df, feature_1, feature_2, new_feature, ngram_range=(1,2), min_df=0.0, analyzer="word"):
    """
    Extracts the cosine similarity between two features in a pandas DataFrame.

    Parameters:
    df (pandas DataFrame): The input DataFrame containing the features.
    feature_1 (str): The name of the first feature column.
    feature_2 (str): The name of the second feature column.
    new_feature (str): The name of the new feature column to store the similarity scores.
    ngram_range (tuple, optional): The range of n-grams to consider for TF-IDF vectorization. Defaults to (1,2).
    min_df (float, optional): The minimum document frequency for TF-IDF vectorization. Defaults to 0.0.
    analyzer (str, optional): The analyzer to use for TF-IDF vectorization. Defaults to "word".

    Returns:
    None

    Notes:
    This function iterates over each row in the input DataFrame, extracts the feature values, computes the TF-IDF matrix, and calculates the cosine similarity between the two features. The similarity scores are stored in a new feature column in the original DataFrame.
    """
    tf = TfidfVectorizer(analyzer=analyzer, ngram_range=ngram_range, min_df=min_df, stop_words='english')
    for index,row in df[[feature_1,feature_2]].iterrows():
        feature_1_feature_2 = pd.DataFrame([row[feature_1],row[feature_2]])
        
        tf_feature_1_feature_2_matrix = tf.fit_transform(feature_1_feature_2[0])
        
        feature_1_feature_2_keywords = tf.get_feature_names_out()
        
        sim = cosine_similarity(tf_feature_1_feature_2_matrix, tf_feature_1_feature_2_matrix)
        
        df.loc[index, new_feature] = sim[0][1]
        
def sort_coo(coo_matrix):
    """
    Sorts a Coordinate (COO) matrix by its values in descending order.

    Parameters:
    coo_matrix (scipy.sparse.coo_matrix): The input COO matrix.

    Returns:
    list: A list of tuples, where each tuple contains a column index and its corresponding value, sorted by the values in descending order.

    Notes:
    The sorting is stable, meaning that when multiple records have the same value, their original order is preserved.
    """
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """
    Extract the top N feature names and their corresponding TF-IDF scores from a sorted vector.

    Parameters:
    feature_names (list): A list of feature names
    sorted_items (list): A list of tuples containing the word index and corresponding TF-IDF score, sorted in descending order
    topn (int, optional): The number of top features to extract (default is 10)

    Returns:
    dict: A dictionary where each key is a feature name and each value is the corresponding TF-IDF score

    """
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
    """
    Return top k keywords for each document in the corpus using TF-IDF method.

    Parameters:
    vectorizer (object): A fitted TF-IDF vectorizer object.
    feature_names (list): A list of feature names (i.e., words in the vocabulary).
    docs (list): A list of documents (i.e., text data).
    TOP_K_KEYWORDS (int): The number of top keywords to extract for each document.

    Returns:
    list: A list of lists, where each inner list contains the top k keywords for a document.
    """
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

def topic_modelling_tfidf(content,max_features=1000, max_df = 0.5,n_components=10,n_iter=100,random_state=122):
    topic_tfidf = TfidfVectorizer( max_features= max_features, max_df =  max_df , smooth_idf=True)
    topic_vector = topic_tfidf.fit_transform(content)
    topic_vector_array= topic_vector.toarray()
    svd_model = TruncatedSVD(n_components=n_components, algorithm='randomized', n_iter=n_iter, random_state=random_state)
    svd_model.fit(topic_vector_array)
    topic_vector_array_reduced = svd_model.transform(topic_vector_array)

    terms = topic_tfidf.get_feature_names_out()
    topics = {}

    for i, comp in enumerate(svd_model.components_):
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key= lambda x:x[1], reverse=True)[:7]
        topics_list = []
        for t in sorted_terms:
            topics_list.append(t[0])
        topics["Topic "+str(i)] = topics_list
    return topics

