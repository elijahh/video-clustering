from processing import *
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def kmeansCluster(k, algo, fileList):
    data = []
    for video in fileList:
        data += [processVideo(video, algo)]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(data)
    km = KMeans(copy_x=True, init='k-means++', max_iter=100,
                n_clusters=k, n_init=1, n_jobs=1,
                precompute_distances=True, random_state=None,
                tol=0.0001, verbose=False)
    km.fit(tfidf)
    return km.labels_
