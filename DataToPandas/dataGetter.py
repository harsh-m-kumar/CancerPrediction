from Application_Logger.logger import App_Logger
from Data_Ingestion.DbOperation import Db_operation
import pandas as pd

class data_getter:
    def __init__(self,logger_writer,file_object):
        self.log_writer=logger_writer
        self.file_object=file_object
    def  get_data(self):
        """""
                                                   Method Name: get_data
                                                   Description: This method reads the data from sqlite3 database and put converts into pandas.
                                                   Output: None
                                                   On Failure: Raise Exception

                                                    Written By: Harsh Kumar
                                                   Version: 1.0
                                                   Revisions: None

                            """
        self.log_writer.log(self.file_object,'Entered into get_data method for getting data into pandas dataframe')
        connect=Db_operation()
        conn=connect.database_connection('cancer')
        c=conn.cursor()
        try:

            #converting Train_Text_Table
            self.log_writer.log(self.file_object, 'Converting the data of Train_Text_Table into Pandas dataframe')
            sql_query="SELECT * FROM Train_Text_Table"
            c.execute(sql_query)
            data=c.fetchall()
            headers=[header[0] for header in c.description]
            try:
                self.df_1=pd.DataFrame(data,columns=headers)
                self.log_writer.log(self.file_object, 'Train_Text_Table successfully converted to the pandas dataframe')
            except Exception as e:
                self.log_writer.log(self.file_object, 'Error %s occurred while converting Train_Text_Table into pandas dataframe ' %e)
                conn.close()

            #converting Pred_Text_Table
            self.log_writer.log(self.file_object, 'Converting the data of Pred_Text_Table into Pandas dataframe')
            sql_query = ('SELECT * FROM Pred_Text_Table')
            c.execute(sql_query)
            data = c.fetchall()
            headers = [header[0] for header in c.description]
            try:
                self.df_2 = pd.DataFrame(data, columns=headers)
                self.log_writer.log(self.file_object, 'Pred_Text_Table successfully converted to the pandas dataframe')
            except Exception as e:
                self.log_writer.log(self.file_object,'Error %s occurred while converting Pred_Text_Table into pandas dataframe ' % e)
                conn.close()

            # converting TrainGeneVarTable
            self.log_writer.log(self.file_object, 'Converting the data of TrainGeneVarTable into Pandas dataframe')
            sql_query = ('SELECT * FROM TrainGeneVarTable')
            c.execute(sql_query)
            data = c.fetchall()
            headers = [header[0] for header in c.description]
            try:
                self.df_3 = pd.DataFrame(data, columns=headers)
                self.log_writer.log(self.file_object,'TrainGeneVarTable successfully converted to the pandas dataframe')

            except Exception as e:
                    self.log_writer.log(self.file_object,'Error %s occurred while converting TrainGeneVarTable into pandas dataframe ' % e)
                    conn.close()

            # converting PredGeneVarTable
            self.log_writer.log(self.file_object,'Converting the data of PredGeneVarTable into Pandas dataframe')
            sql_query = ('SELECT * FROM PredGeneVarTable')
            c.execute(sql_query)
            data = c.fetchall()
            headers = [header[0] for header in c.description]
            try:
                self.df_4 = pd.DataFrame(data, columns=headers)
                self.log_writer.log(self.file_object,'PredGeneVarTable successfully converted to the pandas dataframe')
                return self.df_1,self.df_3,self.df_2,self.df_4
            except Exception as e:
                self.log_writer.log(self.file_object,'Error %s occurred while converting TestGeneVarTable into pandas dataframe ' % e)
                conn.close()

        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s occurred while converting the data from database to pandas dataframe'%e)
            conn.close()

    def merge_data(self,data1,data2):
        """
                                                   Method Name: merge_data
                                                   Description: This method merges two pandas dataframe
                                                   Output: Merged pandas DataFrame
                                                   On Failure: Raise Exception

                                                    Written By: Harsh Kumar
                                                   Version: 1.0
                                                   Revisions: None

                            """
        try:
            df=data2.merge(data1,how='left',on='ID')
            return df
        except Exception as e:
            self.log_writer.log(self.file_object,'Error %s  occured while trying two merge two pandas dataframe'% e)







