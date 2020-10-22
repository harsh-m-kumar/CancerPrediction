import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
class feature_imp:
    def __init__(self,log_writer,file_object):
        self.log_writer=log_writer
        self.file_object=file_object

    def get_feature_imp(self,indices, text, gene, var, no_features, predicted_cls):
        """                       Method Name: get_feature_imp
                                  Description: this method will get the feature importance of the prediction data
                                  Output:feature importance
                                  Written by: Harsh Kumar
                                  Version: 1.0
                                 Revisions: None """
        self.path = './Save_Load/vectorizer.txt'
        important_features=[]

        try:
            with open(self.path, encoding='utf8') as f:
                path_1 = f.readline()
                path_2 = f.readline()
                path_3 = f.readline()


            if path_1[18:24] == 'OneHot':
                try:
                    # featuring the OneHot coding for test data point

                    gene_vectorizer = CountVectorizer(vocabulary=pickle.load(open(path_1[:-1], 'rb')))
                    variation_vectorizer = CountVectorizer(vocabulary=pickle.load(open(path_2[:-1], 'rb')))
                    text_vectorizer = CountVectorizer(min_df=3, vocabulary=pickle.load(open(path_3[:-1], 'rb')))

                    fea1_len = len(gene_vectorizer.get_feature_names())
                    fea2_len = len(variation_vectorizer.get_feature_names())

                    word_present = 0
                    for i, v in enumerate(indices):
                        if (v < fea1_len):
                            word = gene_vectorizer.get_feature_names()[v]
                            yes_no = True if word == gene else False
                            if yes_no:
                                word_present += 1

                                important_features.append("----------------In predicting class {} -- {}th  most important Gene feature [{}] present in test data point [{}]".format(predicted_cls,i,word, yes_no))
                        elif (v < fea1_len + fea2_len):
                            word = variation_vectorizer.get_feature_names()[v - (fea1_len)]
                            yes_no = True if word == var else False
                            if yes_no:
                                word_present += 1

                                important_features.append("----------------In predicting class {} -- {}th most important variation feature [{}] present in test data point [{}]".format(predicted_cls,i,word, yes_no))
                        else:
                            word = text_vectorizer.get_feature_names()[v - (fea1_len + fea2_len)]
                            yes_no = True if word in text.split() else False
                            if yes_no:
                                word_present += 1

                                important_features.append(["----------------In predicting class {} -- {}th most important Text feature [{}] present in test data point [{}]".format(predicted_cls,i,word, yes_no)])

                    important_features.append("----------------Out of the top {} features {} are present in query point".format( no_features, word_present))
                    #important_features = pd.Series(important_features, name='Feature Importance')
                    return important_features
                except Exception as e:
                    self.log_writer.log(self.file_object,'Error %s occurred in getting the feature importance'%e)



            elif path_1[18:23] == 'Tfidf':
                try:

                    # featurizing the Tfidf coding for test data point
                    gene_tfidf_vectorizer = TfidfVectorizer(vocabulary=pickle.load(open(path_1[:-1], 'rb')))
                    variation_tfidf_vectorizer = TfidfVectorizer(vocabulary=pickle.load(open(path_2[:-1], 'rb')))
                    text_tfidf_vectorizer = TfidfVectorizer(vocabulary=pickle.load(open(path_3[:-1], 'rb')))

                    fea1_len = len(gene_tfidf_vectorizer.get_feature_names())
                    fea2_len = len(variation_tfidf_vectorizer.get_feature_names())

                    word_present = 0
                    for i, v in enumerate(indices):
                        if (v < fea1_len):
                            word = gene_tfidf_vectorizer.get_feature_names()[v]
                            yes_no = True if word == gene else False
                            if yes_no:
                                word_present += 1

                                important_features.append(["----------------In Predicting class {} -- {}th most important Gene feature [{}] present in test data point [{}]".format(predicted_cls,i,word, yes_no)])

                        elif (v < fea1_len + fea2_len):
                            word = variation_tfidf_vectorizer.get_feature_names()[v - (fea1_len)]
                            yes_no = True if word == var else False
                            if yes_no:
                                word_present += 1

                                important_features.append(["----------------In predicting class {} -->> {}th most  important variation feature [{}] present in test data point [{}]".format(predicted_cls,i,word, yes_no)])
                        else:
                            word = text_tfidf_vectorizer.get_feature_names()[v - (fea1_len + fea2_len)]
                            yes_no = True if word in text.split() else False
                            if yes_no:
                                word_present += 1

                                important_features.append(["----------------In prediciting class {} -- {}th most important Text feature [{}] present in test data point [{}]".format(predicted_cls,i,word, yes_no)])


                    important_features.append(["----------------Out of the top {}  features {} are present in query point".format(no_features,word_present)])
                    #important_features=pd.Series(important_features,name='Feature Importance')
                    return important_features

                except Exception as e:
                    self.log_writer.log(self.file_object, 'Error %s occurred in getting the feature importance' % e)
        except Exception as e:
            self.log_writer.log(self.file_object,'Getting feature importance unsuccessful!!')