'''
Utility functions for "Data Mining for Business Analytics: Concepts, Techniques, and 
Applications in Python"

(c) 2019, 2024 Galit Shmueli, Peter C. Bruce, Peter Gedeck 
'''
import urllib
import os
import pandas as pd


def printTermDocumentMatrix(count_vect, counts):
    """ Print term-document matrix created by the CountVectorizer 
    Input:
        count_vect: scikit-learn Count vectorizer
        counts: term-document matrix returned by transform method of counter vectorizer
    """
    shape = counts.shape
    columns = ['S{}'.format(i) for i in range(1, shape[0] + 1)]
    print(pd.DataFrame(data=counts.toarray().transpose(),
                       index=count_vect.get_feature_names_out(), columns=columns))


def downloadGloveModel():
    """ Download the GloVe model """
    if not os.path.exists('glove.6B.zip'):
        urllib.request.urlretrieve('http://nlp.stanford.edu/data/glove.6B.zip', 'glove.6B.zip')
