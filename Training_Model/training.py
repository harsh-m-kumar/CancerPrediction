from Training_Model.PreTraining import Pretrain
from Application_Logger.logger import App_Logger
from DataToPandas.dataGetter import data_getter
from Training_Model.preprocessing import preprocess
from Training_Model.Model_Tunner import Tunner
from Save_Load.Model_file_operation import post_training
class training:
    def __init__(self):
        self.log_writer=App_Logger()
        self.file_object=open('Training_Logs/Training_Main_Log.txt','a+')

    def training_model(self):
        """                          Method Name: training
                                     Description: this method will get all the training operations required.
                                     This is the Entry point for Machine Learning Model
                                     Output: None
                                     Written by: Harsh Kumar
                                     Version: 1.0
                                     Revisions: None """
        try:
            self.log_writer.log(self.file_object, 'start of training')

            #calling the Pre_Training method for all table creation, table insertion and unzipping all the files
            self.log_writer.log(self.file_object,'Entering the Pre_Training Method for all the unzipping and database operations')
            pre_training=Pretrain(self.log_writer,self.file_object)
            pre_training.Pre_training()
            self.log_writer.log(self.file_object,'All Pre_training task completed successfully')

            #getting the data into pandas dataframe format from database
            self.log_writer.log(self.file_object,'Entering into get_data method for retrieving data into dataFrame')
            get_data=data_getter(self.log_writer,self.file_object)
            self.train_text, self.train_Gene_Var, self.Pred_text, self.Pred_Gene_Var=get_data.get_data()
            self.log_writer.log(self.file_object,'Got the data into Pandas Dataframe')

            # Merging the text data and the GeneVar data.
            self.log_writer.log(self.file_object,'Entering into    method for merging Text table and GeneVarTable')
            get_data=data_getter(self.log_writer,self.file_object)
            self.data=get_data.merge_data(self.train_Gene_Var,self.train_text)
            self.log_writer.log(self.file_object,'Merged Two pandas dataframe successfully')

            # Drop the null rows
            self.log_writer.log(self.file_object,'Entering into drop_null method')
            pre=preprocess(self.log_writer,self.file_object)
            self.data=pre.drop_null(self.data)
            self.log_writer.log(self.file_object,'Dropped all the null values rows succesfully')

            # Removing all the Stop words and special characters from the TEXT feature
            self.log_writer.log(self.file_object,'Entering into text_preprocessing method')
            pre=preprocess(self.log_writer,self.file_object)
            self.data=pre.text_preprocessing(self.data)
            self.log_writer.log(self.file_object,'Preprocessing of the TEXT feature completed successfully')

            # Splitting data for Training ,Cross validation and Test
            self.log_writer.log(self.file_object,'Entering into splitData method for splitting data into train,Cv,Test')
            pre=preprocess(self.log_writer,self.file_object)
            train_df,test_df,cv_df,y_train,y_test,y_cv=pre.splitData(self.data)
            self.log_writer.log(self.file_object,'Splitted data successfully!!')

            # Generating the One Hot Encoding features
            self.log_writer.log(self.file_object,'Entering into OneHot method for generating the one Hot encodded features and  saving the respective objects')
            pre=preprocess(self.log_writer,self.file_object)
            train_x_onehotCoding,test_x_onehotCoding,cv_x_onehotCoding=pre.OneHot(train_df,cv_df,test_df)
            self.log_writer.log(self.file_object,'Generated One Hot Encoded Features for train,test and cv successfullyy!!')

            #Generating the Tf-idf Encoding features
            self.log_writer.log(self.file_object,'Entering into the TfIdf method for generating the Tf-idf encodded feature and saving the respective objectcs')
            pre=preprocess(self.log_writer,self.file_object)
            train_x_Tfidf,test_x_Tfidf,cv_x_Tfidf=pre.TfIdf(train_df,cv_df,test_df)

            #finding the best model
            self.log_writer.log(self.file_object,'Entering into the FindBestModel method for finding the best model')
            tune=Tunner()
            self.best_model,self.feature_imp_model=tune.FindBestModel(train_x_onehotCoding,test_x_onehotCoding,cv_x_onehotCoding,train_x_Tfidf,test_x_Tfidf,cv_x_Tfidf,y_train,y_test,y_cv)
            self.log_writer.log(self.file_object,'Found the best Model and the original model for feature importance ')

            #saving the mdoel
            self.log_writer.log(self.file_object,'Entering the saving method for saving the model')
            save_model=post_training()
            save_model.save(self.best_model,self.feature_imp_model)
            self.log_writer.log(self.file_object,'Best Model and the model for feature importance saved successfully!!')

        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s occurred while training the model'%e)











