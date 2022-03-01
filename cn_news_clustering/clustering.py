""" Simple clustering solution using KMeans """
from sklearn import cluster
import joblib
from params import Globals as glob
from sklearn.feature_extraction.text import TfidfVectorizer
from lexical_analysis import tokenize


def train_kmeans_model(data):
    """Given a dataset of webpages' corpus, trains and saves the kmeans
    clustering model.

    Args:
        data (list[str]): A list of webpages' corpuses
        
    Returns:
        model: An sklearn KMeans clustering model
    """
    # With assistance from https://investigate.ai/text-analysis/using-tf-idf-with-chinese/
    # The following gets us the tf_idf matrix
    vectorizer = TfidfVectorizer(use_idf=True, stop_words=glob.chinese_stopwords, tokenizer=tokenize)
    tf_idf_matrix = vectorizer.fit_transform(data)
    # We create a model and fit it based on our matrix
    km = cluster.KMeans(n_clusters=glob.n_clusters)
    km.fit(tf_idf_matrix)
    # Save our model for later use.
    joblib.dump(km, glob.model_path)
    return vectorizer, km


def cluster_pages(data):
    """Clusters a list of webpages' corpus in order to find topics.

    Args:
        data (list[str]): A list of webpages' corpuses

    Returns:
        dict: The top words from each cluster
    """
    vectorizer, model = train_kmeans_model(data)
    output = dict()
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(glob.n_clusters):
        output[f"Cluster {i}"] = [
            terms[ind] for ind in order_centroids[i, :glob.words_per_cluster]
        ]
    return output
