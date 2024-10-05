# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:16:50 2024

@author: FATHIMA MUSKAN
"""
import pickle
import os
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# Load saved models
working_dir = os.path.dirname(os.path.abspath(__file__))

diabetes_model = pickle.load(open(f'{working_dir}/diabetes_model.save', 'rb'))

heart_disease_model = pickle.load(open(f'{working_dir}/heart_disease_model.save', 'rb'))

parkinsons_model = pickle.load(open(f'{working_dir}/parkinsons_model.save', 'rb'))

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"],
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

# Function to categorize risk levels based on thresholds
def categorize_risk(value, low_threshold, high_threshold):
    if value < low_threshold:
        return 'Low Risk'
    elif value > high_threshold:
        return 'High Risk'
    else:
        return 'Normal'

# Function to visualize risk factors using Plotly with categories
def visualize_risk_factors_with_categories(factors, values, categories, title):
    fig = px.bar(
        x=factors, 
        y=values, 
        color=categories, 
        labels={'x': 'Risk Factors', 'y': 'Values', 'color': 'Risk Category'}, 
        title=title,
        color_discrete_map={
            'Low Risk': 'green', 
            'Normal': 'blue', 
            'High Risk': 'red'
        }
    )
    st.plotly_chart(fig)

# Function to check if inputs are valid numbers and within the two-digit limit
# Function to check if inputs are valid numbers and within the two-digit limit
def validate_inputs(inputs):
    invalid_values = []  # To store invalid input values
    valid = True
    
    for value in inputs:
        # Check if input is a number and if it exceeds two digits
        try:
            float_value = float(value)  # Convert to float
            if float_value < 0:
                invalid_values.append(value)
                valid = False
            elif abs(float_value) >= 100:  # Check if absolute value exceeds two digits
                invalid_values.append(value)
                valid = False
        except ValueError:
            invalid_values.append(value)  # Add invalid input
            valid = False
            
    return valid, invalid_values  # Return only the invalid input values

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction Using ML')

    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.text_input("Number of pregnancies")
    with col2:
        Glucose = st.text_input("Glucose level")
    with col3:
        BloodPressure = st.text_input("Blood pressure value")
    with col1:
        SkinThickness = st.text_input("Skin thickness value")
    with col2:
        Insulin = st.text_input("Insulin level")
    with col3:
        BMI = st.text_input("BMI value")
    with col1:
        DiabetesPedigreeFunction = st.text_input("Diabetes pedigree function value")
    with col2:
        Age = st.text_input("Age of the person")

    diab_diagnosis = ''
    health_recommendation = ''

    if st.button('Diabetes Test Result', key='diabetes_button'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        
        # Validate the inputs
        valid, feedback = validate_inputs(user_input)
        
        if valid:
            diab_prediction = diabetes_model.predict([user_input])

            if diab_prediction[0] == 1:
                diab_diagnosis = 'The person is diabetic'
                health_recommendation = '''
                **Health Recommendations for Diabetes:**
                - Maintain a balanced diet with low sugar and high fiber.
                - Regular physical activity, such as 30 minutes of moderate exercise daily.
                - Monitor blood glucose levels regularly.
                - Stay hydrated and avoid sugary drinks.
                - Consult a doctor for a personalized medication plan.
                '''
                
                # Defining risk thresholds
                risk_factors = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
                categories = [
                    categorize_risk(float(Pregnancies), 0, 4),
                    categorize_risk(float(Glucose), 70, 120),
                    categorize_risk(float(BloodPressure), 60, 80),
                    categorize_risk(float(SkinThickness), 10, 30),
                    categorize_risk(float(Insulin), 30, 200),
                    categorize_risk(float(BMI), 18.5, 24.9),
                    categorize_risk(float(DiabetesPedigreeFunction), 0.1, 1.0),
                    categorize_risk(float(Age), 20, 50)
                ]
                
                # Visualize with risk categories
                visualize_risk_factors_with_categories(risk_factors, user_input, categories, "Diabetes Risk Factors")
            else:
                diab_diagnosis = 'The person is not diabetic'
        else:
            diab_diagnosis = 'The entered values are invalid: ' + ', '.join(feedback)

    st.success(diab_diagnosis)
    st.info(health_recommendation)

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input('Age')
    with col2:
        sex = st.text_input('Sex')
    with col3:
        cp = st.text_input('Chest Pain types')
    with col1:
        trestbps = st.text_input('Resting Blood Pressure')
    with col2:
        chol = st.text_input('Serum Cholesterol in mg/dl')
    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')
    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')
    with col3:
        exang = st.text_input('Exercise Induced Angina')
    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')
    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')
    with col3:
        ca = st.text_input('Major vessels colored by fluoroscopy')
    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')

    heart_diagnosis = ''
    heart_recommendation = ''

    if st.button('Heart Disease Test Result', key='heart_button'):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        
        # Validate the inputs
        valid, feedback = validate_inputs(user_input)
        
        if valid:
            heart_prediction = heart_disease_model.predict([user_input])

            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person is having heart disease'
                heart_recommendation = '''
                **Health Recommendations for Heart Disease:**
                - Reduce salt intake and avoid fatty, fried foods.
                - Engage in regular cardiovascular exercise like walking, jogging, or swimming.
                - Quit smoking and limit alcohol consumption.
                - Monitor blood pressure regularly and manage stress.
                - Follow a heart-healthy diet rich in fruits, vegetables, and whole grains.
                '''

                # Risk factor thresholds and visualization
                risk_factors = ['Age', 'Sex', 'Chest Pain', 'Resting BP', 'Cholesterol', 'Fasting Blood Sugar', 'ECG Results', 'Max Heart Rate', 'Angina', 'ST Depression', 'Slope', 'Vessels', 'Thalassemia']
                categories = [
                    categorize_risk(float(age), 20, 60),
                    categorize_risk(float(sex), 0, 1),
                    categorize_risk(float(cp), 0, 2),
                    categorize_risk(float(trestbps), 100, 140),
                    categorize_risk(float(chol), 150, 240),
                    categorize_risk(float(fbs), 70, 120),
                    categorize_risk(float(restecg), 0, 1),
                    categorize_risk(float(thalach), 100, 200),
                    categorize_risk(float(exang), 0, 1),
                    categorize_risk(float(oldpeak), 0, 2),
                    categorize_risk(float(slope), 0, 2),
                    categorize_risk(float(ca), 0, 3),
                    categorize_risk(float(thal), 0, 2)
                ]

                # Visualize with risk categories
                visualize_risk_factors_with_categories(risk_factors, user_input, categories, "Heart Disease Risk Factors")
            else:
                heart_diagnosis = 'The person is not having heart disease'
        else:
            heart_diagnosis = 'The entered values are invalid: ' + ', '.join(feedback)

    st.success(heart_diagnosis)
    st.info(heart_recommendation)

# Parkinson's Prediction Page
if selected == "Parkinson's Prediction":
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Enter your name")
    with col2:
        age = st.text_input("Enter your age")
    with col1:
        sex = st.selectbox("Select your sex", ["Male", "Female"])
    with col2:
        test_time = st.text_input("Enter the test time")
    with col1:
        Jitter = st.text_input("Enter Jitter value")
    with col2:
        Jitter_percent = st.text_input("Enter Jitter percentage")
    with col1:
        RAP = st.text_input("Enter RAP value")
    with col2:
        DDA = st.text_input("Enter DDA value")
    with col1:
        SHIM = st.text_input("Enter SHIM value")
    with col2:
        NHR = st.text_input("Enter NHR value")
    with col1:
        HNR = st.text_input("Enter HNR value")
    with col2:
        RPDE = st.text_input("Enter RPDE value")
    with col1:
        DFA = st.text_input("Enter DFA value")
    with col2:
        PPE = st.text_input("Enter PPE value")

    parkinsons_diagnosis = ''
    parkinsons_recommendation = ''

    if st.button("Parkinson's Test Result", key='parkinsons_button'):
        user_input = [age, sex, test_time, Jitter, Jitter_percent, RAP, DDA, SHIM, NHR, HNR, RPDE, DFA, PPE]
        
        # Validate the inputs
        valid, feedback = validate_inputs(user_input)
        
        if valid:
            parkinsons_prediction = parkinsons_model.predict([user_input])

            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "The person has Parkinson's disease"
                parkinsons_recommendation = '''
                **Health Recommendations for Parkinson's Disease:**
                - Consult a neurologist for tailored treatment and therapy.
                - Engage in regular physical activity to improve mobility.
                - Maintain a balanced diet rich in antioxidants.
                - Stay socially active to combat depression.
                - Explore speech therapy if communication becomes difficult.
                '''
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"
        else:
            parkinsons_diagnosis = 'The entered values are invalid: ' + ', '.join(feedback)

    st.success(parkinsons_diagnosis)
    st.info(parkinsons_recommendation)
    
