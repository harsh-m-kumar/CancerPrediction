from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from Application_Logger.logger import App_Logger
import numpy as np

import pickle
class post_training:
    def __init__(self):
        self.log_writer=App_Logger()
        self.file_object=open('./Prediction_log/prediction.txt','a+')
        self.model_directory='./Model/'
    def save(self,calibrated_model,original_model):
        """                          Method Name: save
                                     Description: this method will save the best model that has been trained.
                                     Return :None
                                     Written by: Harsh Kumar
                                     Version: 1.0
                                     Revisions: None """
        self.best_model=calibrated_model
        self.feature_imp_model=original_model
        try:
            f=open(self.model_directory+'best_model'+'.pkl','wb')
            pickle.dump(self.best_model,f)
            f.close()
        except Exception as e:
            self.log_writer.log(self.file_object, 'Error %s occurred while saving the best model' % e)
        try:
            f=open(self.model_directory+'feature_imp_model'+'.pkl','wb')
            pickle.dump(self.feature_imp_model, f)
            f.close()
        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s occurred while saving the original model which will give the festure importance'%e)



    def load_model(self):
        """                          Method Name: load_model
                                     Description: this method will load the best model that has been trained.
                                     Return :best model
                                     Written by: Harsh Kumar
                                     Version: 1.0
                                     Revisions: None """
        self.path='./Model/'
        try:
            self.model=pickle.load(open(self.path+'best_model'+'.pkl','rb'))

        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s occurred while loading the best model'%e)

        try:
            self.feature_imp_model=pickle.load(open(self.path+'feature_imp_model'+'.pkl','rb'))
            return self.model,self.feature_imp_model
        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s occurred while loading the original model for feature importance'%e)

    def load_vectorizer(self,data):
        """                                 Method Name: load_vectorizer
                                            Description: this method will load the vectorizer required for featuring our original features
                                            Return :
                                            Written by: Harsh Kumar
                                            Version: 1.0
                                            Revisions: None """
        self.path='./Save_Load/vectorizer.txt'
        try:
            with open(self.path,encoding='utf8') as f:
                path_1=f.readline()
                path_2=f.readline()
                path_3=f.readline()
            if path_1[18:24]=='OneHot':
                try:
                    # featuring the OneHot coding for test data point

                    gene_vectorizer = CountVectorizer(vocabulary=pickle.load(open(path_1[:-1],'rb')))
                    variation_vectorizer = CountVectorizer(vocabulary=pickle.load(open(path_2[:-1],'rb')))
                    text_vectorizer = CountVectorizer(min_df=3,vocabulary=pickle.load(open(path_3[:-1],'rb')))

                    test_gene_feature_onehotCoding=gene_vectorizer.fit_transform(data['Gene']).toarray()
                    test_variation_feature_onehotCoding=variation_vectorizer.fit_transform(data['Variation']).toarray()
                    test_text_feature_onehotCoding=text_vectorizer.fit_transform(data['TEXT']).toarray()

                    #normalize the TEXT feature
                    test_text_feature_onehotCoding = normalize(test_text_feature_onehotCoding, axis=0)

                    # merging test_gene_feature_onehotCoding and test_variation_feature_onehotCoding
                    test_gene_var_onehotCoding = np.hstack(test_gene_feature_onehotCoding, test_variation_feature_onehotCoding)


                    # Finally merging and getting final test_x_onehotCoding
                    test_x_onehotCoding = np.hstack(test_gene_var_onehotCoding, test_text_feature_onehotCoding)

                    self.log_writer.log(self.file_object,'Successfully featurized ')
                    return test_x_onehotCoding
                except Exception as e:
                    self.log_writer.log(self.file_object,'Error %s occurred while featurizing OneHotEncoding for the test data point'%e)

            elif path_1[18:23]=='Tfidf':
                try:

                    # featurizing the Tfidf coding for test data point
                    gene_tfidf_vectorizer = TfidfVectorizer(vocabulary=pickle.load(open(path_1[:-1],'rb')))
                    variation_tfidf_vectorizer = TfidfVectorizer(vocabulary=pickle.load(open(path_2[:-1],'rb')))
                    text_tfidf_vectorizer = TfidfVectorizer(vocabulary=pickle.load(open(path_3[:-1],'rb')))

                    test_gene_feature_Tfidf = gene_tfidf_vectorizer.fit_transform(data['Gene'].values).toarray()
                    test_variation_feature_Tfidf = variation_tfidf_vectorizer.fit_transform(data['Variation'].values).toarray()
                    test_text_feature_Tfidf = text_tfidf_vectorizer.fit_transform(data['TEXT'].values).toarray()

                    # normalizing
                    test_text_feature_Tfidf = normalize(test_text_feature_Tfidf, axis=0)

                    # merging test_gene_feature_Tfidf and test_variation_feature_Tfidf
                    test_gene_var_Tfidf = np.hstack((test_gene_feature_Tfidf, test_variation_feature_Tfidf))

                    # Finally merging and getting test_x_Tfidf
                    test_x_Tfidf = np.hstack((test_gene_var_Tfidf, test_text_feature_Tfidf))

                    self.log_writer.log(self.file_object, 'Successfully featurized ')
                    return  test_x_Tfidf

                except Exception as e:
                    self.log_writer.log(self.file_object,'Error %s occurred while featurizing Tfidf for the test data point'%e)

        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s Occurred while preprocessing the test data point'%e)











