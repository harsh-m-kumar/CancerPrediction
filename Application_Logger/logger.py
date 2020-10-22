from datetime import datetime

class App_Logger:
    """This class shall be used to read current time and date in certain format and writing the log message,
     and provide file_object:where to write the log message."""
    def __init__(self):
        pass
    def log(self,file_object,log_message):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        file_object.write(
            str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message + "\n")

