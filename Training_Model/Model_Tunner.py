from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import SGDClassifier
from Application_Logger.logger import App_Logger
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection
from sklearn.metrics.classification import log_loss
import numpy as np
import warnings
warnings.filterwarnings("ignore")
class Tunner:
    def __init__(self):
        self.log_writer=App_Logger()
        self.file_object=open('Training_Logs/Model_Tunning_Logs.txt','a+')
        self.path='./Save_Load/vectorizer.txt'

    def FindBestModel(self ,train_x_onehotCoding,test_x_onehotCoding,cv_x_onehotCoding,train_x_Tfidf,test_x_Tfidf,cv_x_Tfidf,y_train,y_test,y_cv):
        """                          Method Name: FindBestModel
                                     Description: this method will find the best model that gives us least log-loss
                                     Return :Best model found with least log loss
                                     Written by: Harsh Kumar
                                     Version: 1.0
                                     Revisions: None """

        try:
            loss=[]
            # training Logistic regression with balanced class and One Hot Encodded features
            try:
                self.alpha_1=[pow(10,x) for x in range(-3,3)]
                cv_log_error_array=[]
                for i in self.alpha_1:
                    print('for alpha i',i)
                    clf=SGDClassifier(class_weight='balanced',alpha=i,penalty='l2',loss='log',random_state=123)
                    clf.fit(train_x_onehotCoding,y_train)
                    sig_clf=CalibratedClassifierCV(clf,method='sigmoid')
                    sig_clf.fit(train_x_onehotCoding,y_train)
                    sig_clf_probs=sig_clf.predict_proba(cv_x_onehotCoding)
                    cv_log_error_array.append(log_loss(y_cv, sig_clf_probs, labels=clf.classes_, eps=1e-15))
                    # to avoid rounding error while multiplying probabilites we use log-probability estimates
                    print("Log Loss :", log_loss(y_cv, sig_clf_probs))

                self.best_alpha_1 = np.argmin(cv_log_error_array)
                clf = SGDClassifier(class_weight='balanced', alpha=self.alpha_1[self.best_alpha_1], penalty='l2', loss='log', random_state=123)
                clf.fit(train_x_onehotCoding, y_train)
                sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                sig_clf.fit(train_x_onehotCoding, y_train)


                predict_y = sig_clf.predict_proba(test_x_onehotCoding)
                self.log_writer.log(self.file_object,'For Logistic Reg. with balanced class and OneHot features the best alpha value is:{}, The Test loss is {}'.format(self.alpha_1[self.best_alpha_1],log_loss(y_test, predict_y, labels=clf.classes_, eps=1e-15)))

                self.loss_lr_OneHot_bal=log_loss(y_test, predict_y, labels=clf.classes_, eps=1e-15)
                loss.append(self.loss_lr_OneHot_bal)
                self.log_writer.log(self.file_object,'Logistic Reg. with balanced class and OneHot features trainied successfully!!')

            except Exception as e:
                self.log_writer.log(self.file_object,'Error %s Occurred while finding the log loss of Logistic Reg whith OneHot features and class balanced'%e)



            #training Logistic regression with clsss balanced and Tf-idf features and
            try:
                self.alpha_2 = [10 ** x for x in range(-3, 3)]
                cv_log_error_array = []
                for i in self.alpha_2:
                    print("for alpha =", i)
                    clf = SGDClassifier(class_weight='balanced', alpha=i, penalty='l2', loss='log', random_state=42)
                    clf.fit(train_x_Tfidf, y_train)
                    sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                    sig_clf.fit(train_x_Tfidf, y_train)
                    sig_clf_probs = sig_clf.predict_proba(cv_x_Tfidf)
                    cv_log_error_array.append(log_loss(y_cv, sig_clf_probs, labels=clf.classes_, eps=1e-15))
                    # to avoid rounding error while multiplying probabilites we use log-probability estimates
                    print("Log Loss :", log_loss(y_cv, sig_clf_probs))

                self.best_alpha_2 = np.argmin(cv_log_error_array)
                clf = SGDClassifier(class_weight='balanced', alpha=self.alpha_2[self.best_alpha_2], penalty='l2', loss='log', random_state=42)
                clf.fit(train_x_Tfidf, y_train)
                sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                sig_clf.fit(train_x_Tfidf, y_train)

                predict_y = sig_clf.predict_proba(test_x_Tfidf)
                self.log_writer.log(self.file_object,
                            'For Logistic Reg with balanced class and Tfidf features the best alpha value is:{}, The Test loss is {}'.format(self.alpha_2[self.best_alpha_2],
                                                                                     log_loss(y_test, predict_y,
                                                                                              labels=clf.classes_,
                                                                                              eps=1e-15)))
                self.loss_lr_Tfidf_bal = log_loss(y_test, predict_y, labels=clf.classes_, eps=1e-15)
                loss.append(self.loss_lr_Tfidf_bal)
                self.log_writer.log(self.file_object,'Logistic Reg with balanced class and Tfidf features trainined successfully')

            except Exception as e:
                self.log_writer.log(self.file_object,'Error %s occurred while training the Logistic Reg with balanced class and Tfidf features model '%e)



            #Logistic Regression with Tfidf features and without class balancing
            try:
                self.alpha_3 = [10 ** x for x in range(-3, 3)]
                cv_log_error_array = []
                for i in self.alpha_3:
                    print("for alpha =", i)
                    clf = SGDClassifier(alpha=i, penalty='l2', loss='log', random_state=42)
                    clf.fit(train_x_Tfidf, y_train)
                    sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                    sig_clf.fit(train_x_Tfidf, y_train)
                    sig_clf_probs = sig_clf.predict_proba(cv_x_Tfidf)
                    cv_log_error_array.append(log_loss(y_cv, sig_clf_probs, labels=clf.classes_, eps=1e-15))
                    # to avoid rounding error while multiplying probabilites we use log-probability estimates
                    print("Log Loss :", log_loss(y_cv, sig_clf_probs))

                self.best_alpha_3 = np.argmin(cv_log_error_array)
                clf = SGDClassifier(alpha=self.alpha_3[self.best_alpha_3], penalty='l2', loss='log', random_state=42)
                clf.fit(train_x_Tfidf, y_train)
                sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                sig_clf.fit(train_x_Tfidf, y_train)

                predict_y = sig_clf.predict_proba(test_x_Tfidf)

                self.log_writer.log(self.file_object,
                            'For Logistic Reg without balanced class and Tfidf features the best alpha value is:{}, The Test loss is {}'.format(
                                self.alpha_3[self.best_alpha_3],
                                log_loss(y_test, predict_y,
                                         labels=clf.classes_,
                                         eps=1e-15)))
                self.loss_lr_Tfidf_Notbal = log_loss(y_test, predict_y, labels=clf.classes_, eps=1e-15)
                loss.append(self.loss_lr_Tfidf_Notbal)
                self.log_writer.log(self.file_object,
                            'Logistic Reg without balanced class and Tfidf features trainined successfully')

            except Exception as e:
                self.log_writer.log(self.file_object,
                        'Error %s occurred while training the Logistic Reg without balanced class and Tfidf features model ' % e)

            #finding the best model
            least_loss_indices=np.argmin(loss)
            least_loss=loss[least_loss_indices]
            if least_loss==self.loss_lr_OneHot_bal:
                #finally training the model with best parameters
                clf = SGDClassifier(class_weight='balanced', alpha=self.alpha_1[self.best_alpha_1], penalty='l2', loss='log',
                            random_state=42)
                clf.fit(train_x_onehotCoding, y_train)
                sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                sig_clf.fit(train_x_onehotCoding, y_train)
                self.log_writer.log(self.file_object,'Best Model choosen is Logistic Reg. with balanced class and OneHot features with Log loss {}'.format(least_loss))

                path_1='./CountVectorizer/OneHotGene.pkl'
                path_2='./CountVectorizer/OneHotVariation.pkl'
                path_3='./CountVectorizer/OneHotText.pkl'

                f=open(self.path,'a+')
                f.write(path_1+"\n")
                f.write(path_2+"\n")
                f.write(path_3+"\n")
                f.close()

                return sig_clf,clf

            elif least_loss==self.loss_lr_Tfidf_bal:
                # finally training the model with best parameters
                clf = SGDClassifier(class_weight='balanced', alpha=self.alpha_2[self.best_alpha_2], penalty='l2', loss='log',
                            random_state=42)
                clf.fit(train_x_Tfidf, y_train)
                sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                sig_clf.fit(train_x_Tfidf, y_train)
                self.log_writer.log(self.file_object,
                                    'Best Model choosen is Logistic Reg with balanced class and Tfidf features with Log loss {}'.format(
                                        least_loss))
                path_1 = './CountVectorizer/TfidfGene.pkl'
                path_2 = './CountVectorizer/TfidfVariation.pkl'
                path_3 = './CountVectorizer/TfidfText.pkl'

                f = open(self.path, 'a+')
                f.write(path_1 + "\n")
                f.write(path_2 + "\n")
                f.write(path_3 + "\n")
                f.close()

                return sig_clf,clf

            else:
                clf = SGDClassifier(alpha=self.alpha_3[self.best_alpha_3], penalty='l2', loss='log', random_state=42)
                clf.fit(train_x_Tfidf, y_train)
                sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
                sig_clf.fit(train_x_Tfidf, y_train)
                self.log_writer.log(self.file_object,
                                    'Best Model choosen is Logistic Reg without balanced class and Tfidf features with Log loss {}'.format(
                                        least_loss))
                path_1 = './CountVectorizer/TfidfGene.pkl'
                path_2 = './CountVectorizer/TfidfVariation.pkl'
                path_3 = './CountVectorizer/TfidfText.pkl'

                f = open(self.path, 'a+')
                f.write(path_1 + "\n")
                f.write(path_2 + "\n")
                f.write(path_3 + "\n")
                f.close()

                return sig_clf,clf
        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s occurred while finding the best model'%e)

                
                







