import pandas as pd
import numpy as np

# data preprocessing
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import Word

import unidecode  # """ to remove accented characters from text, e.g. café"""

from num2words import num2words  # converting numbers to words

# import contractions
# import NLP libries
import re
import nltk
import string
from nltk.corpus import stopwords

# import spacy


import string

# for model-building
from sklearn.model_selection import train_test_split  # importing train and test
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVR, SVC  # importing SVr
from xgboost import XGBClassifier
from sklearn import metrics
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix  # import metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score, precision_recall_curve  # import metrics
from sklearn.model_selection import GridSearchCV, cross_validate  # importing gridsearch
from sklearn.model_selection import RandomizedSearchCV  # importing Randomsearch
from sklearn.base import BaseEstimator, TransformerMixin
import swifter  # Speed up your Pandas Processing with Swifter

# bag of words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# for word embedding
import gensim
from gensim.parsing.preprocessing import preprocess_string

from gensim.models import Word2Vec
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

from tqdm import tqdm  # for pregress bar

from sklearn import utils
from sklearn.pipeline import FeatureUnion, Pipeline

import multiprocessing
# in doc2vec:-use these many worker threads to train the model (=faster training with multicore machines)

import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from collections import Counter
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer
import warnings

import torch
import transformers as ppb  # pytorch transformers

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
np.random.seed(2018)
tqdm.pandas(desc="progress-bar")

pd.set_option('display.max_columns', 999)
pd.set_option('display.max_rows', 999)
pd.set_option('display.width', 1000)
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore')
cores = multiprocessing.cpu_count()
wl = WordNetLemmatizer()


class NlpPreprocessing:
    def preprocess(text):
        text = text.lower()
        text = text.strip()
        text = re.compile('<.*?>').sub('', text)
        text = re.compile('[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+').sub('', text)
        text = re.compile('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}').sub('', text)
        text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
        text = re.sub('\s+', ' ', text)
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        # text = re.sub(r'\b\w\b', '',text)
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
        # text = re.sub(r'\d',' ',text)
        text = re.sub(r'\s+', ' ', text)

        return text

    # STOPWORD REMOVAL
    def stopword(string):
        a = [i for i in string.split() if i not in stopwords.words('english')]
        return ' '.join(a)

    # remove accented characters
    def remove_accented_chars(text):
        """remove accented characters from text, e.g. café"""
        text = unidecode.unidecode(text)
        return text

    # remove single character
    def single_characters(text):
        text = re.sub(r'\b\w\b', '', text)
        return text

    # function to convert numbers to words
    def num_to_words(text):
        """
        Return :- text which have all numbers or integers in the form of words
        Input :- string
        Output :- string
        """
        # splitting text into words with space
        after_spliting = text.split()

        for index in range(len(after_spliting)):
            if after_spliting[index].isdigit():
                after_spliting[index] = num2words(after_spliting[index])

        # joining list into string with space
        numbers_to_words = ' '.join(after_spliting)
        return numbers_to_words

    ## Remove single characters

    def remove_single_char(text):
        """
        Return :- string after removing single characters

        """
        single_char_pattern = r'\s+[a-zA-Z]\s+'
        without_sc = re.sub(pattern=single_char_pattern, repl=" ", string=text)
        return without_sc

    def remov_duplicates(input):

        # split input string separated by space
        input = input.split(" ")

        # joins two adjacent elements in iterable way
        for i in range(0, len(input)):
            input[i] = "".join(input[i])

        # now create dictionary using counter method
        # which will have strings as key and their
        # frequencies as value
        UniqW = Counter(input)

        # joins two adjacent elements in iterable way
        s = " ".join(UniqW.keys())
        return s

    def get_wordnet_pos(tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # Tokenize the sentence
    def lemmatizer(string):
        word_pos_tags = nltk.pos_tag(word_tokenize(string))  # Get position tags
        a = [wl.lemmatize(tag[0], get_wordnet_pos(tag[1])) for idx, tag in
             enumerate(word_pos_tags)]  # Map the position tag and lemmatize the word/token
        return " ".join(a)

    def pipelinize(function, active=True):
        def list_comprehend_a_function(list_or_series, active=True):
            if active:
                return [function(i) for i in list_or_series]
            else:  # if it's not active, just pass it right back
                return list_or_series

        return FunctionTransformer(list_comprehend_a_function, validate=False, kw_args={'active': active})

    def create_preprocessing_pipeline():

        estimators = [('preprocess', pipelinize(preprocess)),
                      ('stopword', pipelinize(stopword)),
                      ('remove_accented_chars', pipelinize(remove_accented_chars)),
                      ('single_characters', pipelinize(single_characters)),
                      ('num_to_words', pipelinize(num_to_words)),
                      ('remove_single_char', pipelinize(remove_single_char)),
                      ('remov_duplicates', pipelinize(remov_duplicates)),
                      ('lemmatizer', pipelinize(lemmatizer))]

        pipe = Pipeline(estimators)
        return pipe