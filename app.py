from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import numpy as np

app = Flask(__name__)

with open(f'model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Factor1")
def factorcheck1():
    return render_template("Factor1.html")

@app.route("/Factor2")
def factorcheck2():
    return render_template("Factor2.html")

@app.route("/Factor3")
def factorcheck3():
    return render_template("Factor3.html")

@app.route("/Factor4")
def factorcheck4():
    return render_template("Factor4.html")

@app.route('/calculator', methods=['GET', 'POST'])
def comparison():
    if request.method == 'GET':

        return render_template('calculator.html')
    

    if request.method == 'POST':
 
        age = request.form['age']

        if request.form['hypertension'] == "hyperYes":
            hypertension = 1
            input_hypertension = "Yes"
        else:
            hypertension = 0
            input_hypertension = "No"

        if request.form['hd'] == "HDYes":
            heart_disease = 1
            input_hd = "Yes"
        else:
            heart_disease = 0
            input_hd = "No"

        avgglucose = request.form['glucose']
        bmi = request.form['bmi']

        if request.form['gender'] == "female":
            input_gender = "Female"
            female = 1
            male = 0
            other = 0
        elif request.form['gender'] == "male":
            input_gender = "Male"
            female = 0
            male = 1
            other = 0
        else:
            input_gender = "Other"
            female = 0
            male = 0
            other = 1

        if request.form['married'] == "marriedYes":
            input_married = "Yes"
            marriedNo = 0
            marriedYes = 1
        else:
            input_married = "No"
            marriedNo = 1
            marriedYes = 0
        
        if request.form['smokestatus'] == "smokes":
            input_smokestatus = "smokes"
            smokingUnknown = 0
            smokingFormer = 0
            smokingNever = 0
            smokes = 1
        elif request.form['smokestatus'] == "formerSmoker":
            input_smokestatus = "Former Smoker"
            smokingUnknown = 0
            smokingFormer = 1
            smokingNever = 0
            smokes = 0
        elif request.form['smokestatus'] == "neverSmoked":
            input_smokestatus = "Never Smoked"
            smokingUnknown = 0
            smokingFormer = 0
            smokingNever = 1
            smokes = 0
        else:
            input_smokestatus = "Unknown"
            smokingUnknown = 1
            smokingFormer = 0
            smokingNever = 0
            smokes = 0

        inputs = pd.DataFrame([[age, hypertension, heart_disease, avgglucose, bmi, female, male, other, marriedNo, marriedYes,
            smokingUnknown, smokingFormer, smokingNever, smokes]], columns = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level',
            'bmi', 'gender_Female', 'gender_Male', 'gender_Other', 'ever_married_No', 'ever_Married_Yes', 'smoking_status_Unknown',
            'smoking_status_formerlysmoked', 'smoking_status_neversmoked', 'smoking_status_smokes'])

        prediction = model.predict_proba(inputs)[0]
        prediction1 = str(round(prediction[1]*100,2)) + "%"

    

        inputs2 = {"Age": age, "Gender": input_gender, "Ever Married": input_married, "Hypertension": input_hypertension, "Heart Disease": input_hd, "Smoking Status": input_smokestatus, "Glucose": avgglucose, "BMI": bmi}

        return render_template("calculator.html",result=prediction1, result2=inputs2)

if __name__ == '__main__':
    app.run()