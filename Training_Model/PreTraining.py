
from DataFromS3.unzipping import unzipp

from Data_Ingestion.DbOperation import Db_operation

class Pretrain:
    def __init__(self,log_writer,file_object):
        self.log_writer=log_writer
        self.file_object=file_object
    def Pre_training(self):
        """                  Method Name: Pre_training
                             Description: this method will perform unzipping of the files downloaded from S3 bucket,creating tables for the data.
                             Written by: Harsh Kumar
                             Version: 1.0
                             Revisions: None """

        try:
            column_names_1={'ID':'INTEGER','Gene':'TEXT','Variation':'TEXT','Class':'INTEGER'}
            column_names_2={'ID':'INTEGER','TEXT':'TEXT'}


            #unzipping thte data dowloaded from the S3 bucket
            unzipped=unzipp(self.log_writer,self.file_object)
            unzipped.unzipping()
            self.log_writer.log(self.file_object,'Finished unzipping all the files')


            #creating Train_Text_Table table.
            self.log_writer.log(self.file_object,'Entering into Table creation for Train_Text_Table')
            DbOperation=Db_operation()
            DbOperation.createTrainTextTable('cancer',column_names_2)
            self.log_writer.log(self.file_object,'Created Train_Text_Table successfully')

            #creating TrainGeneVarTable table.
            self.log_writer.log(self.file_object,'Entering into createTrainGeneVarTable method for Table creation for TrainGeneVarTable')
            DbOperation.createTrainGeneVarTable('cancer',column_names_1)
            self.log_writer.log(self.file_object,'Created TrainGeneVarTable table Successfully!!')

            #creating Pred_Text_Table
            self.log_writer.log(self.file_object,'Entering into createPredTextTable method for Table creation of Pred_Text_Table')
            DbOperation.createPredTextTable('cancer',column_names_2)
            self.log_writer.log(self.file_object,'Created Test_Text_Table table successfully!!')

            #creating PredGeneVarTable Table
            self.log_writer.log(self.file_object,'Entering into createPredGeneVarTable method for table creation for PredGeneVarTable Table')
            DbOperation.createPredGeneVarTable('cancer',column_names_1)
            self.log_writer.log(self.file_object,'Created PredGeneVarTable table Successfully!!')

            #Inserting values in Train_Text_Table  and Pred_Text_Table
            self.log_writer.log(self.file_object,'Entering into method insertDataIntoTextTable for inserting data in Train_Text_Table  and Pred_Text_Table')
            DbOperation.insertDataIntoTextTable('cancer','train')
            DbOperation.insertDataIntoTextTable('cancer', 'Pred')
            self.log_writer.log(self.file_object,'Data inserted into Train_Text_Table and Test_Text_Table Successfully!!')

            #Inserting values in TrainGeneVarTable and PredGeneVarTable
            self.log_writer.log(self.file_object,'Entering into insertDataIntoGenVarTable method for inserting data into TrainGeneVarTable and PredGeneVarTable table')
            DbOperation.insertDataIntoGenVarTable('cancer','train')
            DbOperation.insertDataIntoGenVarTable('cancer', 'Pred')
            self.log_writer.log(self.file_object,'Data inserted into TrainGeneVarTable and PredGeneVarTable Successfully!!')

        except Exception as e:
            self.log_writer.log(self.file_object,'Error "%s "occurred while training the model' %e)

