import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import warnings
warnings.filterwarnings("ignore")



class preprocess:
    def __init__(self,log_writer,file_object):
        self.logger=log_writer
        self.file_object=file_object

    def drop_null(self,data):
        """                          Method Name: drop_null
                                     Description: this method will drop all the null values present

                                     Written by: Harsh Kumar
                                     Version: 1.0
                                     Revisions: None"""
        try:
            df=data.drop(list(data[data.TEXT.isna()].index),axis=0)
            return df
        except Exception as e:
            self.logger.log(self.file_object,'Error %s Occured while trying to drop the null valued rows' %e)

    def text_preprocessing(self, data):
        """                                  Method Name: text_preprocessing
                                             Description: this method will perform text preprocessing on the TEXT feature like removal of
                                             stop words, removing special characters,converting multiple white spcaes to single whitespaces

                                             Written by: Harsh Kumar
                                             Version: 1.0
                                             Revisions: None"""
        stop_words=set(stopwords.words('english'))
        stop_words.remove('not')
        try:

            for index, row in data.iterrows():
                string = ""
                # replace every special character with space
                row['TEXT'] = re.sub('[^a-zA-Z0-9\n]', ' ', row['TEXT'])
                # replace multiple spcaes with single space
                row['TEXT'] = re.sub('\s+', ' ', row['TEXT'])
                # converting all the upper case letters to lower case letters
                row['TEXT'] = row['TEXT'].lower()
                for word in row['TEXT'].split():
                    # if the word is not a stop word then retain the data in the dataframe
                    if not word in stop_words:
                        string += word + " "
                data['TEXT'][index] = string
            return data
        except Exception as e:
            self.logger.log(self.file_object,'Error %s occurred while preprocessing the text' %e)

    def splitData(self,data):
        """                                  Method Name: splitData
                                             Description: this method will split the data into train, cross validation and test dataframe
                                             Returns: train_df,test_df,cv_df,y_train,y_test,y_cv
                                             Written by: Harsh Kumar
                                             Version: 1.0
                                             Revisions: None"""

        y_true=data['Class']
        try:

            # split the data into test and train by maintaining same distribution of output varaible 'y_true' [stratify=y_true]

            X_train,test_df,y_train,y_test=train_test_split(data,y_true,stratify=y_true,test_size=0.2)

            # split the train data into train and cross validation by maintaining same distribution of output varaible 'y_train' [stratify=y_train]

            train_df,cv_df,y_train,y_cv=train_test_split(X_train,y_train,stratify=y_train,test_size=0.2)

            return train_df,test_df,cv_df,y_train,y_test,y_cv

        except Exception as e:
            self.logger.log(self.file_object,'Error %s Occurred while splitting the data' %e)

    def OneHot(self,train_df,cv_df,test_df):
        """                          Method Name: OneHot
                                     Description: this method Generates One Hot Encoded feature for training, cross validation and test dataset.
                                                    Also this method saves the OneHotEncoded Object and perform merging of all the OneHot encoded features
                                     Returns: train_x_onehotCoding, test_x_onehotCoding, cv_x_onehotCoding
                                     Written by: Harsh Kumar
                                     Version: 1.0
                                     Revisions: None"""


        gene_vectorizer=CountVectorizer()
        variation_vectorizer = CountVectorizer()
        text_vectorizer = CountVectorizer(min_df=3) # building a CountVectorizer with all the words that occured minimum 3 times in train data
        try:
            #generating One Hot encoding  for Gene feature
            train_gene_feature_onehotCoding = gene_vectorizer.fit_transform(train_df['Gene']).toarray()
            test_gene_feature_onehotCoding = gene_vectorizer.transform(test_df['Gene']).toarray()
            cv_gene_feature_onehotCoding = gene_vectorizer.transform(cv_df['Gene']).toarray()

            try:
                #saving the gene_vectorizer
                pickle.dump(gene_vectorizer.vocabulary_,open('./CountVectorizer/OneHotGene.pkl','wb'))
                self.logger.log(self.file_object,'OneHotGene.pkl file saved successfully!!')
            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while saving OneHotGene.pkl file' %e)

            # generating One Hot encoding for Variation feature
            train_variation_feature_onehotCoding = variation_vectorizer.fit_transform(train_df['Variation']).toarray()
            test_variation_feature_onehotCoding = variation_vectorizer.transform(test_df['Variation']).toarray()
            cv_variation_feature_onehotCoding = variation_vectorizer.transform(cv_df['Variation']).toarray()

            try:
                # saving the variation_vectorizer
                pickle.dump(variation_vectorizer.vocabulary_,open('./CountVectorizer/OneHotVariation.pkl','wb'))
                self.logger.log(self.file_object,'OneHotVariation.pkl file saved successfully!!')
            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while saving OneHotVariation.pkl '%e)

            train_text_feature_onehotCoding = text_vectorizer.fit_transform(train_df['TEXT']).toarray()

            #normalizing
            train_text_feature_onehotCoding = normalize(train_text_feature_onehotCoding, axis=0)

            test_text_feature_onehotCoding = text_vectorizer.transform(test_df['TEXT']).toarray()

            # normalizing
            test_text_feature_onehotCoding = normalize(test_text_feature_onehotCoding, axis=0)

            cv_text_feature_onehotCoding = text_vectorizer.transform(cv_df['TEXT']).toarray()

            #normalizing
            cv_text_feature_onehotCoding = normalize(cv_text_feature_onehotCoding, axis=0)

            try:
                #saving the text_vectorizer
                pickle.dump(text_vectorizer.vocabulary_,open('./CountVectorizer/OneHotText.pkl','wb'))
                self.logger.log(self.file_object,'OneHotText.pkl file saved successfully')
            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while saving the OneHotText.pkl model'%e)

            try:

                #merging train_gene_feature_onehotCoding and train_variation_feature_onehotCoding
                train_gene_var_onehotCoding = np.hstack((train_gene_feature_onehotCoding, train_variation_feature_onehotCoding))

                #merging test_gene_feature_onehotCoding and test_variation_feature_onehotCoding
                test_gene_var_onehotCoding = np.hstack((test_gene_feature_onehotCoding, test_variation_feature_onehotCoding))

                #merging cv_gene_feature_onehotCoding and cv_variation_feature_onehotCoding
                cv_gene_var_onehotCoding = np.hstack((cv_gene_feature_onehotCoding, cv_variation_feature_onehotCoding))

                # Finally merging and getting final train_x_onehotCoding
                train_x_onehotCoding = np.hstack((train_gene_var_onehotCoding, train_text_feature_onehotCoding))

                # Finally merging and getting final test_x_onehotCoding
                test_x_onehotCoding = np.hstack((test_gene_var_onehotCoding, test_text_feature_onehotCoding))

                # Finally merging and getting final
                cv_x_onehotCoding = np.hstack((cv_gene_var_onehotCoding, cv_text_feature_onehotCoding))

                return train_x_onehotCoding, test_x_onehotCoding, cv_x_onehotCoding

            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while merging all the OneHotEncodded features together'%e)

        except Exception as e:
            self.logger.log(self.file_object,'Error %s occurred while creating OneHot encoded features'%e)


    def TfIdf(self,train_df,cv_df,test_df):
        """                          Method Name: TfIdf
                                     Description:This method Generates Tf-idf Encoded feature for training, cross validation and test dataset.
                                                 Also this method saves the Tfidf Object
                                     Returns: train_x_Tfidf,test_x_Tfidf,cv_x_Tfidf
                                     Written by: Harsh Kumar
                                     Version: 1.0
                                     Revisions: None"""
        gene_tfidf_vectorizer=TfidfVectorizer()
        variation_tfidf_vectorizer=TfidfVectorizer()
        text_tfidf_vectorizer=TfidfVectorizer()
        try:
            # Generating Tfidf features for Gene
            train_gene_feature_Tfidf = gene_tfidf_vectorizer.fit_transform(train_df['Gene'].values).toarray()
            test_gene_feature_Tfidf = gene_tfidf_vectorizer.transform(test_df['Gene'].values).toarray()
            cv_gene_feature_Tfidf = gene_tfidf_vectorizer.transform(cv_df['Gene'].values).toarray()

            try:
                # Saving the gene_tfidf_vectorizer object
                pickle.dump(gene_tfidf_vectorizer.vocabulary_,open('./CountVectorizer/TfidfGene.pkl','wb'))
                self.logger.log(self.file_object,'TfidfGene.pkl file saved successfully!!')

            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while saving the TfidfGene.pkl file'%e)

            #Generating Tfidf features for Variation
            train_variation_feature_Tfidf = variation_tfidf_vectorizer.fit_transform(train_df['Variation'].values).toarray()
            test_variation_feature_Tfidf = variation_tfidf_vectorizer.transform(test_df['Variation'].values).toarray()
            cv_variation_feature_Tfidf = variation_tfidf_vectorizer.transform(cv_df['Variation'].values).toarray()

            try:
                #saving the variation_tfidf_vectorizer object
                pickle.dump(variation_tfidf_vectorizer.vocabulary_,open('./CountVectorizer/TfidfVariation.pkl','wb'))
                self.logger.log(self.file_object,'TfidfVariation.pkl file saved successfully')
            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while saving TfidfVariation.pkl file'%e)

            #Generating Tfidf features for TEXT
            train_text_feature_Tfidf = text_tfidf_vectorizer.fit_transform(train_df['TEXT'].values).toarray()

            # normalizing
            train_text_feature_Tfidf = normalize(train_text_feature_Tfidf, axis=0)


            test_text_feature_Tfidf = text_tfidf_vectorizer.transform(test_df['TEXT'].values).toarray()

            # normalizing
            test_text_feature_Tfidf = normalize(test_text_feature_Tfidf, axis=0)

            cv_text_feature_Tfidf = text_tfidf_vectorizer.transform(cv_df['TEXT'].values).toarray()

            # normalizing
            cv_text_feature_Tfidf = normalize(cv_text_feature_Tfidf, axis=0)
            try:
                #saving the text_tfidf_vectorizer object
                pickle.dump(text_tfidf_vectorizer.vocabulary_,open('./CountVectorizer/TfidfText.pkl','wb'))
                self.logger.log(self.file_object,'TfidfText.pkl file saved successfully')
            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while saving the TfidfText.pkl file' %e)

            try:

                #merging train_gene_feature_Tfidf and train_variation_feature_Tfidf
                train_gene_var_Tfidf = np.hstack((train_gene_feature_Tfidf, train_variation_feature_Tfidf))

                #merging test_gene_feature_Tfidf and test_variation_feature_Tfidf
                test_gene_var_Tfidf = np.hstack((test_gene_feature_Tfidf, test_variation_feature_Tfidf))

                #merging cv_gene_feature_Tfidf and cv_variation_feature_Tfidf
                cv_gene_var_Tfidf = np.hstack((cv_gene_feature_Tfidf, cv_variation_feature_Tfidf))

                # Finally merging and getting final train_x_Tfidf
                train_x_Tfidf = np.hstack((train_gene_var_Tfidf, train_text_feature_Tfidf))

                # Finally merging and getting test_x_Tfidf
                test_x_Tfidf = np.hstack((test_gene_var_Tfidf, test_text_feature_Tfidf))

                # Finally merging and getting cv_x_Tfidf
                cv_x_Tfidf = np.hstack((cv_gene_var_Tfidf, cv_text_feature_Tfidf))

                return train_x_Tfidf,test_x_Tfidf,cv_x_Tfidf

            except Exception as e:
                self.logger.log(self.file_object,'Error %s occurred while merging the Tfidf features together'%e)

        except Exception as e:
            self.logger.log(self.file_object,'Error %s Occurred while creating Tfidf features' %e)




