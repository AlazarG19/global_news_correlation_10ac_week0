from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
from wordcloud import WordCloud

import matplotlib.pyplot as plt
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
    """
    Extracts top keywords from a given dataframe.

    Parameters:
    data (pandas.DataFrame): Input dataframe containing text data.

    Returns:
    pandas.DataFrame: A dataframe with a single column 'top_keywords' containing a list of top keywords for each document.

    Notes:
    - The function uses TF-IDF vectorization to generate keywords.
    - The number of top keywords to extract is set to 10, but can be adjusted by modifying the `get_keywords` function.
    """
    vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True)
    corpora = data.to_list()
    vectorizer.fit_transform(corpora)
    feature_names = vectorizer.get_feature_names_out()

    keywords = get_keywords(vectorizer, feature_names, corpora, 10)
    result = [{'top_keywords': list(keywords[i].keys())} for i, doc in enumerate(corpora)]
    final = pd.DataFrame(result)
    return final

def categorize_headlines(headlines, tags):
    """
    Categorize headlines into tags based on keyword matching.

    Parameters:
    headlines (list[str]): A list of headlines to be categorized.
    tags (dict[str, list[str]]): A dictionary where each key is a tag and each value is a list of keywords associated with that tag.

    Returns:
    list[str]: A list of categorized headlines, where each headline is a comma-separated string of tags.

    Notes:
    If a headline does not match any keywords, it will be categorized as "Other".
    """
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

def extract_topic_vectors(content, max_features=1000, max_df=0.5, n_components=10, n_iter=100, random_state=122):
    """
    Extract the reduced topic vectors using TF-IDF vectorization and truncated SVD.

    Parameters:
    content (list of str): The list of text documents to perform topic modeling on.
    max_features (int, optional): The maximum number of features to extract from the text data. Defaults to 1000.
    max_df (float, optional): The maximum document frequency for features to be considered. Defaults to 0.5.
    n_components (int, optional): The number of topics to extract. Defaults to 10.
    n_iter (int, optional): The number of iterations for the truncated SVD algorithm. Defaults to 100.
    random_state (int, optional): The random seed for reproducibility. Defaults to 122.

    Returns:
    tuple: A tuple containing the reduced topic vector array and the feature names.
    """
    topic_tfidf = TfidfVectorizer(max_features=max_features, max_df=max_df, smooth_idf=True)
    topic_vector = topic_tfidf.fit_transform(content)
    topic_vector_array = topic_vector.toarray()

    svd_model = TruncatedSVD(n_components=n_components, algorithm='randomized', n_iter=n_iter, random_state=random_state)
    svd_model.fit(topic_vector_array)
    topic_vector_array_reduced = svd_model.transform(topic_vector_array)

    terms = topic_tfidf.get_feature_names_out()
    
    return topic_vector_array_reduced, svd_model, terms

def topic_modelling_tfidf(svd_model, terms, n_components=10):
    """
    Complete the topic modeling process by extracting the top terms for each topic.

    Parameters:
    svd_model: The trained SVD model containing the components.
    terms (list of str): The list of feature names (terms).
    n_components (int, optional): The number of topics to extract. Defaults to 10.

    Returns:
    dict: A dictionary where each key is a topic label (e.g., "Topic 0") and each value is a list of the top 7 terms associated with that topic.
    """
    topics = {}
    
    for i, comp in enumerate(svd_model.components_):
        terms_comp = zip(terms, comp)
        sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:7]
        topics_list = [t[0] for t in sorted_terms]
        topics["Topic " + str(i)] = topics_list

    return topics

def topic_modelling_lda(data, num_topics, min_df=10, token_pattern='[a-zA-Z0-9]{3,}', max_features=50000, max_iter=10, batch_size=128):
    """
    Perform topic modeling using Latent Dirichlet Allocation (LDA) on a given dataset.

    Parameters:
    - data (list of str): List of documents to perform topic modeling on.
    - num_topics (int): Number of topics to extract from the data.
    - min_df (int, optional): Minimum frequency of words to be considered. Defaults to 10.
    - token_pattern (str, optional): Regular expression pattern to tokenize words. Defaults to '[a-zA-Z0-9]{3,}'.
    - max_features (int, optional): Maximum number of features (words) to extract. Defaults to 50000.
    - max_iter (int, optional): Maximum number of iterations for the LDA model. Defaults to 10.
    - batch_size (int, optional): Batch size for the LDA model. Defaults to 128.

    Returns:
    - lda_output (array): The Trained LDA Model.
    - lda_output (array): Document-topic matrix where each row represents a document and each column represents a topic.
    - vectorizer: Countvectorizer used to create features for lsa.
    - output (dict): Dictionary where each key is a topic and the value is a list of the top 10 words associated with that topic.

    Notes:
    - This function uses the CountVectorizer from scikit-learn to convert the text data into a numerical representation.
    - The LDA model is then applied to this representation to extract the topics.
    """
    vectorizer = CountVectorizer(analyzer='word', min_df=min_df, lowercase=True, token_pattern=token_pattern, max_features=max_features)
    vectorized_feature = vectorizer.fit_transform(data)
    # Create the LDA model
    lda_model = LatentDirichletAllocation(n_components=num_topics, max_iter=max_iter, learning_method='online', random_state=100, batch_size=batch_size, evaluate_every=-1, n_jobs=-1)
    lda_output = lda_model.fit_transform(vectorized_feature)
    output = {}
    for index, topic in enumerate(lda_model.components_):
        output[f"Topic {index}"] = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]]
    return lda_model, lda_output,vectorizer, output

def plot_word_cloud(topics,num_cols=2):
# Plotting the word clouds for each topic
    n_topics = len(topics)
    rows = (n_topics + num_cols - 1) // num_cols  # Calculate the number of rows needed

    fig, axes = plt.subplots(rows, num_cols, figsize=(15, 5 * rows))

    for i, (topic_idx, word_freq) in enumerate(topics.items()):
        row = i // num_cols
        col = i % num_cols
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        
        axes[row, col].imshow(wordcloud, interpolation="bilinear")
        axes[row, col].axis("off")
        axes[row, col].set_title(f"Topic #{topic_idx}")
    fig.savefig('word_cloud.png')
        
