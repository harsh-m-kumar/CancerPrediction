from Application_Logger.logger import App_Logger
from Save_Load.Model_file_operation import post_training
from Prediction.get_feature_names import feature_imp
import numpy as np
class prediction:
    def __init__(self):
        self.log_writer=App_Logger()
        self.file_object=open('./Prediction_log/prediction.txt','a+')

    def preprocessing_prediction(self,data):
        """                       Method Name: predict
                                  Description: this method will perform the preprocessing of test data
                                  Output:None
                                  Written by: Harsh Kumar
                                  Version: 1.0
                                  Revisions: None """
        try:
            #featurising the features of the test data
            get_features=post_training()
            data1=get_features.load_vectorizer(data)

            self.log_writer.log(self.file_object, 'Successfully fetched the data')

            return data1
        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s occurred while preprocessing the data'%e)

    def predict_values(self,test_data,data,sig_clf,clf):
        """                       Method Name: predict_values
                                  Description: this method will perform the prediction of test data
                                  Output:Returns feature importance, predicted probablities abd predicted class.
                                  Written by: Harsh Kumar
                                  Version: 1.0
                                  Revisions: None """
        self.path = './Save_Load/vectorizer.txt'


        try:

            with open(self.path, encoding='utf8') as f:
                path_1 = f.readline()
                print(path_1)
                if path_1[18:24] == 'OneHot':
                    try:

                        predicted_cls = sig_clf.predict(data.iloc[0])[0]

                        predicted_prob=np.round(sig_clf.predict_proba(data.iloc[0],4))
                        predicted_probs = [(i+1, v) for i, v in enumerate(predicted_prob[0])]

                        no_features=100
                        indices = np.argsort(-1 * abs(clf.coef_))[predicted_cls - 1][:,:no_features]

                        fea_imp=feature_imp(self.log_writer,self.file_object)
                        important_features=fea_imp.get_feature_imp(indices[0], test_data['TEXT'].iloc[0],test_data['Gene'].iloc[0].lower(),test_data['Variation'].iloc[0].lower(),no_features,predicted_cls[0])

                        return important_features,predicted_probs,predicted_cls

                    except Exception as e:
                        self.log_writer.log(self.file_object,"Error %s in computing the feature importance of one Hot Encoded features"%e)


                elif path_1[18:23]== 'Tfidf':
                    try:

                        predicted_cls = sig_clf.predict(data.reshape(1,data.shape[1]))


                        predicted_prob=np.round(sig_clf.predict_proba(data.reshape(1,data.shape[1])),4)
                        predicted_probs=[(i+1,v) for i,v in enumerate(predicted_prob[0])]

                        no_features=100


                        indices = np.argsort(-1 * abs(clf.coef_))[predicted_cls - 1][:, :no_features]


                        fea_imp = feature_imp(self.log_writer, self.file_object)
                        important_features = fea_imp.get_feature_imp(indices[0], test_data['TEXT'].iloc[0], test_data['Gene'].iloc[0].lower(),
                                                     test_data['Variation'].iloc[0].lower(), no_features, predicted_cls[0])

                        self.log_writer.log(self.file_object, 'Successfully returned the values')
                        f=open('./Prediction_log/prediction.txt','a+')
                        self.log_writer.log(f,'Successfully returned important_features,predicted_prob,predicted_cls values')
                        f.close()

                        return important_features,predicted_probs,predicted_cls

                    except Exception as e:
                        self.log_writer.log(self.file_object,'Error %s in computing the feature importance for tfidf features'%e)

        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s in computing the feature importance'%e)














