from Training_Model.preprocessing import preprocess
from Application_Logger.logger import App_Logger
from tabulate import tabulate
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from Save_Load.Model_file_operation import post_training
from flask import Flask
from Prediction.model_prediction import prediction
import pickle
import pandas as pd
from flask import request,render_template
import re

app = Flask(__name__)

@app.route("/",methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():

    load_model=post_training()
    best_model,feature_imp_model=load_model.load_model()

    if request.method == 'POST':
            Gene=str(request.form['Gene'])
            Variation=str(request.form['Variation'])
            TEXT=str(request.form['TEXT'])

            stop_words = set(stopwords.words('english'))
            stop_words.remove('not')
            string = ""
            TEXT=re.sub('[^a-zA-Z0-9\n]', ' ',TEXT)
            TEXT=re.sub('\s+', ' ', TEXT)
            for word in TEXT.split():
                # if the word is not a stop word then retain the data in the dataframe
                if not word in stop_words:
                    string += word + " "
            TEXT = string

            raw_data=pd.DataFrame(data=[[Gene,Variation,TEXT]],columns=['Gene','Variation','TEXT'])

            #preprocessing the data before prediction
            pred1=prediction()
            data=pred1.preprocessing_prediction(raw_data)

            pred2 = prediction()

            important_features,predicted_prob,predicted_cls=pred2.predict_values(raw_data,data,best_model,feature_imp_model)

            return render_template('prediction.html', Predicted_class="Predicted class is {}".format(predicted_cls),
                               Predicted_prob="Predicted Probabilities are {} ".format(predicted_prob),
                               feature_imp=tabulate(important_features,tablefmt="fancy_grid"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
    #app.run(debug=True)# for running in local







