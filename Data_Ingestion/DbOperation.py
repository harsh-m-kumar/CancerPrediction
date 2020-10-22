import shutil
import sqlite3
from Application_Logger.logger import App_Logger
import csv
import os

class Db_operation:
    """
              This class shall be used for handling all the SQL operations.

              Written By: Harsh Kumar
              Version: 1.0
              Revisions: Nonse

              """
    def __init__(self):
        self.path='Training_Database/'
        self.logger=App_Logger()

    def database_connection(self,DatabaseName):
        """
                                Method Name: dataBaseConnection
                                Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
                                Output: Connection to the DB
                                On Failure: Raise ConnectionError

                                 Written By: Harsh Kumar
                                Version: 1.0
                                Revisions: None

                """
        try:
            conn=sqlite3.connect(self.path+DatabaseName+'.db')
            file=open('Training_Logs/DataBaseConnectionLog.txt','a+')
            self.logger.log(file,"Opened %s database successfully" % DatabaseName)
            file.close()
        except ConnectionError:
            file=open('Training_Logs/DataBaseConnectionLog.txt','a+')
            self.logger.log(file,'Error while openening %s database' % DatabaseName)
            file.close()
            raise ConnectionError
        return conn
    def createTrainTextTable(self,DatabaseName,column_names):
        """
                                        Method Name: createTextTable
                                        Description: This method creates a table for text data in the given database which will be used to insert training data.
                                        Output: None
                                        On Failure: Raise Exception

                                         Written By: Harsh Kumar
                                        Version: 1.0
                                        Revisions: None

                """
        try:
            file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
            self.logger.log(file, 'Entered into createTrainTextTable table')
            file.close()
            conn=self.database_connection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Train_Text_Table'")
            if c.fetchone()[0]==1:
                conn.close()
                file=open('Training_Logs/DbTableCreateLog.txt','a+')
                self.logger.log(file,'Table already exist!!')
                file.close()
            else:
                for key in column_names.keys():
                    type=column_names[key]
                    try:
                        # in try block we check if the table exists, if yes then add columns to the table
                        # else in catch block we will create the table

                        c.execute('ALTER TABLE Train_Text_Table ADD COLUMN {column_name} {dataType}'.format(column_name=key,dataType=type))
                    except:
                        c.execute('CREATE TABLE Train_Text_Table({column_name} {dataType})'.format(column_name=key,dataType=type))

                conn.close()
                file=open("Training_Logs/DbTableCreateLog.txt",'a+')
                self.logger.log(file,'Table created successfully')
                file.close()

                file=open("Training_Logs/DatabaseConnectionLog.txt",'a+')
                self.logger.log(file,'Closed %s database successfully' %DatabaseName)
                file.close()

        except Exception as e:
            file=open('Training_Logs/DbTableCreateLog.txt','a+')
            self.logger.log(file,'Error while creating the table %s' %e)
            file.close()
            file=open('Training_Logs/DatabaseConnectionLog.txt','a+')
            self.logger.log(file,'Closed %s database successfully' %DatabaseName)
            file.close()
            raise e


    def createPredTextTable(self,DatabaseName,column_names):
        """
                                        Method Name: createPredTextTable
                                        Description: This method creates a table for prediction text data in the given database which will be used to insert Prediction data.
                                        Output: None
                                        On Failure: Raise Exception

                                         Written By: Harsh Kumar
                                        Version: 1.0
                                        Revisions: None

                """
        try:
            file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
            self.logger.log(file, 'Entered into createPredTextTable table')
            file.close()
            conn=self.database_connection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Pred_Text_Table'")
            if c.fetchone()[0]==1:
                conn.close()
                file=open('Training_Logs/DbTableCreateLog.txt','a+')
                self.logger.log(file,'Table already exist!!')
                file.close()
            else:
                for key in column_names.keys():
                    type=column_names[key]
                    try:
                        # in try block we check if the table exists, if yes then add columns to the table
                        # else in catch block we will create the table

                        c.execute('ALTER TABLE Pred_Text_Table ADD COLUMN {column_name} {dataType}'.format(column_name=key,dataType=type))
                    except:
                        c.execute('CREATE TABLE Pred_Text_Table({column_name} {dataType})'.format(column_name=key,dataType=type))

                conn.close()
                file=open("Training_Logs/DbTableCreateLog.txt",'a+')
                self.logger.log(file,'Table created successfully')
                file.close()

                file=open("Training_Logs/DatabaseConnectionLog.txt",'a+')
                self.logger.log(file,'Closed %s database successfully' %DatabaseName)
                file.close()

        except Exception as e:
            file=open('Training_Logs/DbTableCreateLog.txt','a+')
            self.logger.log(file,'Error while creating the table %s' %e)
            file.close()
            file=open('Training_Logs/DatabaseConnectionLog.txt','a+')
            self.logger.log(file,'Closed %s database successfully' %DatabaseName)
            file.close()
            raise e



    def createTrainGeneVarTable(self,DatabaseName,column_names):
        """
                                                Method Name: createTrainGeneVarTable
                                                Description: This method creates a table gor gene and variation features in the given database which will be used to insert training data.
                                                Output: None
                                                On Failure: Raise Exception

                                                 Written By: Harsh Kumar
                                                Version: 1.0
                                                Revisions: None

                        """
        try:
            file=open('Training_Logs/DbTableCreateLog.txt','a+')
            self.logger.log(file,'Entered in createTrainGeneVarTable function')
            conn = self.database_connection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT COUNT(name) from sqlite_master where type='table' AND name='TrainGeneVarTable'")
            if c.fetchone()[0]==1:
                conn.close()
                file = open('Training_Logs/DbTableCreateLog.txt', 'a+')

                self.logger.log(file,'TrainGeneVarTable table already exists!!!')

            else:
                for key in column_names.keys():
                    type=column_names[key]
                    try:

                        c.execute('ALTER TABLE TrainGeneVarTable ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))

                    except:
                        c.execute('CREATE TABLE TrainGeneVarTable({column_name} {datatype})'.format(column_name=key,datatype=type))

                self.logger.log(file,'TrainGeneVarTable created successfully!!')
                file.close()
                conn.close()
        except Exception as e:
            file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
            self.logger.log(file, 'Error while creating the table %s' % e)
            file.close()
            file = open('Training_Logs/DatabaseConnectionLog.txt', 'a+')
            self.logger.log(file, 'Closed %s database successfully' % DatabaseName)
            file.close()
            raise e


    def createPredGeneVarTable(self,DatabaseName,column_names):
        """
                                                Method Name: createPredGeneVarTable
                                                Description: This method creates a table for gene and variation features in the given database which will be used to insert Prediction data.
                                                Output: None
                                                On Failure: Raise Exception

                                                 Written By: Harsh Kumar
                                                Version: 1.0
                                                Revisions: None

                        """
        try:

            file=open('Training_Logs/DbTableCreateLog.txt','a+')
            self.logger.log(file,'Entered in createPredGeneVarTable function')
            conn = self.database_connection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT COUNT(name) from sqlite_master where type='table' AND name='PredGeneVarTable'")
            if c.fetchone()[0]==1:
                conn.close()
                file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
                self.logger.log(file,'PredGeneVarTable table already exists')

            else:
                for key in column_names.keys():
                    type=column_names[key]
                    if key == 'Class':
                        continue
                    else:
                        try:
                            c.execute('ALTER TABLE PredGeneVarTable ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))

                        except:
                            c.execute('CREATE TABLE PredGeneVarTable({column_name} {datatype})'.format(column_name=key,datatype=type))
                self.logger.log(file,'PredGeneVarTable table created Successfully!!')
                conn.close()
        except Exception as e:
            file = open('Training_Logs/DbTableCreateLog.txt', 'a+')
            self.logger.log(file, 'Error while creating the table %s' % e)
            file.close()
            file = open('Training_Logs/DatabaseConnectionLog.txt', 'a+')
            self.logger.log(file, 'Closed %s database successfully' % DatabaseName)
            file.close()
            raise e

    def insertDataIntoTextTable(self,DatabaseName,name):


        """
                                                   Method Name: insertDataIntoTrainTable
                                                   Description: This method inserts the text data  into the
                                                                above created table.
                                                   Output: None
                                                   On Failure: Raise Exception

                                                    Written By: Harsh Kumar
                                                   Version: 1.0
                                                   Revisions: None

                            """
        file=open('Training_Logs/DbInsertLog.txt','a+')
        if name=='train':
            self.logger.log(file,'Entered into insertDataIntoTrainTable for inserting data')
            conn=self.database_connection(DatabaseName)
            c=conn.cursor()
            for i in c.execute('SELECT COUNT(*) FROM Train_Text_Table'):
                if i[0] >=1:
                    self.logger.log(file,'Values already inserted')
                    file.close()
                else:
                    sql_insert= ''' INSERT INTO Train_Text_Table(ID,TEXT) VALUES (?,?)'''
                    with open('RawTrainData/training_text', encoding='utf8') as f:
                        for line in f.readlines():
                            if line == 'ID,Text\n':
                                continue
                            else:
                                try:
                                    line=line.split('||')
                                    c.execute(sql_insert,(int(line[0]),line[1]))
                                    conn.commit()
                                except Exception as e:
                                    self.logger.log(file, "Error while inserting into table: %s " % e)
                                    file.close()

                    self.logger.log(file,'Data inserted successfully')
        elif name =='Pred':
            self.logger.log(file,'Entered into insertDataIntoPredTable for inserting data')
            conn=self.database_connection((DatabaseName))
            c=conn.cursor()
            for i in c.execute(('SELECT COUNT(*) FROM Pred_Text_Table')):
                if i[0]>=1:
                    self.logger.log(file,'Values are already inserted')
                    file.close()
                else:
                    sql_insert = ''' INSERT INTO Pred_Text_Table(ID,TEXT) VALUES (?,?)'''
                    with open('RawPredictionData/test_text', encoding='utf8') as f:
                        for line in f.readlines():
                            if line == 'ID,Text\n':
                                continue
                            else:
                                try:
                                    line = line.split('||')
                                    c.execute(sql_insert, (int(line[0]), line[1]))
                                    conn.commit()
                                except Exception as e:
                                    self.logger.log(file, "Error while inserting into table: %s " % e)
                                    file.close()
                    self.logger.log(file,'Data inserted successfully')
                    file.close()

    def insertDataIntoGenVarTable(self, DatabaseName, name):
        """""
                                                   Method Name: insertDataIntoGenVarTable
                                                   Description: This method inserts the data files  into the
                                                                above created table.
                                                   Output: None
                                                   On Failure: Raise Exception

                                                    Written By: Harsh Kumar
                                                   Version: 1.0
                                                   Revisions: None

                            """
        file = open('Training_Logs/DbInsertLog.txt', 'a+')
        if name == 'train':
            self.logger.log(file, 'Entered into TrainGeneVarTable table for inserting data')
            conn = self.database_connection(DatabaseName)
            c = conn.cursor()
            for i in c.execute(('SELECT COUNT(*) FROM TrainGeneVarTable')):
                if i[0]>=1:
                    self.logger.log(file,'Values are already inserted')
                    file.close()
                else:
                    sql_insert='''INSERT INTO TrainGeneVarTable(ID,Gene,Variation,Class) VALUES (?,?,?,?)'''
                    with open('RawTrainData/training_variants', encoding='utf8') as f:
                        for line in f.readlines():
                            if line == 'ID,Gene,Variation,Class\n':
                                continue
                            else:
                                try:
                                    c.execute(sql_insert,(int(line.split(',')[0]),line.split(',')[1],line.split(',')[2],int(line.split(',')[3][0])))
                                    conn.commit()
                                except Exception as e:
                                    self.logger.log(file, "Error while inserting into table: %s " % e)
                                    file.close()
                    self.logger.log(file,'Data Entered into TrainGeneVarTable successfully !!')
                    file.close()

        elif name == 'Pred':
            self.logger.log(file, 'Entered into PredGeneVarTable table for inserting data')
            conn = self.database_connection(DatabaseName)
            c = conn.cursor()
            for i in c.execute(('SELECT COUNT(*) FROM PredGeneVarTable')):
                if i[0]>=1:
                    self.logger.log(file,'Values are already inserted')
                    file.close()
                else:
                    sql_insert = '''INSERT INTO PredGeneVarTable(ID,Gene,Variation) VALUES (?,?,?)'''
                    with open('RawPredictionData/test_variants', encoding='utf8') as f:
                        for line in f.readlines():
                            if line == 'ID,Gene,Variation\n':
                                continue
                            else:
                                try:
                                    c.execute(sql_insert,(int(line.split(',')[0]),line.split(',')[1],line.split(',')[2]))
                                    conn.commit()
                                except Exception as e:
                                    self.logger.log(file, "Error while inserting into table: %s " % e)
                                    file.close()
                    self.logger.log(file,'Data Entered into PredGeneVarTable successfully !!')
                    file.close()












