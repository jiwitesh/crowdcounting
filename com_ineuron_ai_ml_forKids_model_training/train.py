# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import warnings
from sklearn.feature_extraction.text import CountVectorizer
import gensim
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Training:

    '''def __init__(self, fileLocation, fileName):
        # train = pd.read_csv(r'data\test.csv')
        self.filelocname = "..//"+fileLocation + "/" + fileName
        self.dataFrame = pd.read_csv(self.filelocname)
        print("Inside Training init")
        print(self.dataFrame)'''

    def data_pre_processing (self, dataFrame, feature):
        print("Inside data_pre_processing")
        print("dataFrame[feature]", dataFrame[feature])
        dataFrame[feature] = dataFrame[feature].str.replace("[^a-zA-Z#]", " ")
        self.tokenized_lName = dataFrame[feature].apply(lambda x: x.split())  # tokenizing
        self.bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
        self.bow = self.bow_vectorizer.fit_transform(dataFrame[feature])
        print(self.bow.shape)
        print(self.bow)
        train_bow = self.bow[:, :]

        return self.tokenized_lName, train_bow

    def model_w2v_training(self, tokenized_lName, dataframe, feature):
        print("Inside model_w2v_training")
        self.model_w2v = gensim.models.Word2Vec(
        tokenized_lName,
        size=200,  # desired no. of features/independent variables
        window=5,  # context window size
        min_count=2,
        sg=2,  # 1 for skip-gram model
        hs=0,
        negative=10,  # for negative sampling
        workers=2,  # no.of cores
        seed=34)

        self.model_w2v.train(tokenized_lName, total_examples=len(dataframe[feature]), epochs=20)

        return self.model_w2v

    def word_vector(self, tokens, size, model_w2v):
        print("Inside word_vector")
        vec = np.zeros(size).reshape((1, size))
        count = 0.
        for word in tokens:
            try:
                vec += model_w2v[word].reshape((1, size))
                count += 1.
            except KeyError:  # handling the case where the token is not in vocabulary

                continue
        if count != 0:
            vec = count
        return vec


    def model_training(self, train_bow, dataframe, tokenized_tweet, bow, model_w2v, label, modelName):
        print("Inside model_training")
        xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(train_bow, dataframe[label],random_state=42,test_size=0.3)
        wordvec_arrays = np.zeros((len(tokenized_tweet), 200))

        for i in range(len(tokenized_tweet)):
            wordvec_arrays[i, :] = self.word_vector(tokenized_tweet[i], 200, model_w2v)

        wordvec_df = pd.DataFrame(wordvec_arrays)
        wordvec_df.shape
        train_bow = bow[:, :]

        train_w2v = wordvec_df.iloc[:, :]
        test_w2v = wordvec_df.iloc[:, :]

        xtrain_w2v = train_w2v.iloc[ytrain.index, :]
        xvalid_w2v = test_w2v.iloc[yvalid.index, :]

        lreg = LogisticRegression()
        lreg.fit(xtrain_w2v, ytrain)
        filename = 'models/'+modelName
        pickle.dump(lreg, open(filename, 'wb'))

    def execute(self, dataFrame, feature, label, modelName):
        self.tokenized_lName, train_bow = self.data_pre_processing(dataFrame, feature)
        self.model_w2v = self.model_w2v_training(self.tokenized_lName, dataFrame, feature)
        self.model_training(train_bow, dataFrame, self.tokenized_lName, train_bow, self.model_w2v, label, modelName)



