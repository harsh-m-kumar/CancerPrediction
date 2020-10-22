import zipfile
import os

class unzipp:
    def __init__(self,log_writer,file_object):
        self.log_writer=log_writer
        self.file_object=file_object
    def unzipping(self):
        """""
                                                   Method Name: zipping
                                                   Description: This method unzips the data downloaded from the S3 bucket
                                                   and store it in RawTrainData and RawTestData folder
                                                   Output: None
                                                   On Failure: Raise Exception

                                                    Written By: Harsh Kumar
                                                   Version: 1.0
                                                   Revisions: None

                            """
        self.log_writer.log(self.file_object,'Entered into Unzipping method')
        path='C:/Users/Harsh/Data science/Internship/CancerPrediction/RawTrainData/training_text'
        if os.path.isfile(path) == True:
            self.log_writer.log(self.file_object, 'Files have already been unzipped')
        else:
            try:

                with zipfile.ZipFile('C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/training_text.zip', 'r') as zip_ref:
                    zip_ref.extractall('C:/Users/Harsh/Data science/Internship/CancerPrediction/RawTrainData')

                with zipfile.ZipFile('C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/test_text.zip', 'r') as zip_ref:
                    zip_ref.extractall('C:/Users/Harsh/Data science/Internship/CancerPrediction/RawPredictionData')

                with zipfile.ZipFile('C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/training_variants.zip', 'r') as zip_ref:
                    zip_ref.extractall('C:/Users/Harsh/Data science/Internship/CancerPrediction/RawTrainData')

                with zipfile.ZipFile('C:/Users/Harsh/Data science/Internship/CancerPrediction/DataFromS3/test_variants.zip', 'r') as zip_ref:
                    zip_ref.extractall('C:/Users/Harsh/Data science/Internship/CancerPrediction/RawPredictionData')
                self.log_writer.log(self.file_object,'Exited fromm unzipping method')
            except Exception as e:
                self.log_writer.log(self.file_object,'Error : %s Occured while unzipping the files' %e)
