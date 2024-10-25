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
import streamlit as st
import pytesseract
from PIL import Image
import PyPDF2
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

import librosa
import numpy as np
import streamlit as st
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

import opencv_python







# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="C:/Users/FATHIMA MUSKAN/Downloads/White and Blue Modern Health Clinic Logo/1.png")

# Getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Loading the saved models
diabetes_model = pickle.load(open(f'{working_dir}/diabetes_model.save', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/heart_disease_model.save', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/parkinsons_model.save', 'rb'))

# Streamlit interface
with st.sidebar: 
    selected = option_menu( 
        'Multiple Disease Prediction System',
        ['User Dashboard','Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction",'Food and Diet Recommendations', 'Nearby Hospital Finder','Emergency Health Info Card' ],
        icons=['people','activity', 'heart', 'person', 'egg-fried',  'hospital', 'card-heading'],
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

# Function to check if inputs are valid numbers and within the limit for given Value
def validate_inputs(inputs):
    invalid_values = []  # To store invalid input values
    valid = True
    
    for i, value in enumerate(inputs):
        try:
            float_value = float(value)  # Convert to float

            # Specific validation for "Number of pregnancies" (index 0 in inputs)
            if i == 0 and float_value > 17:
                return False, ["Pregnancies exceed the maximum limit of 17, that cannot be predictable"]
            # Specific validation for "Number of glucose level" (index 1 in inputs)
            if i == 1 and float_value > 199:
                return False, ["Glucose level exceed the maximum limit of 199, that cannot be predictable"]
            if i == 2 and float_value > 122:
                return False, ["Blood Pressure level exceed the maximum limit of 122, that cannot be predictable"]
            if i == 3 and float_value > 99:
                return False, ["Skin Thickness value exceed the maximum limit of 99, that cannot be predictable"]
            if i == 4 and float_value > 200:
                return False, ["Insulin level exceed the maximum limit of 200, means the person has Type 2 diabetes & that cannot be predictable"]
            if i == 5 and float_value > 67:
                return False, ["BMI value exceed the maximum limit of 67, that cannot be predictable"]
            if i == 6 and float_value > 2.42:
                return False, ["Diabetes Pedigree Function value exceed the maximum limit of 2.42, that cannot be predictable"]
            if i == 7 and float_value > 120:
                return False, ["Age value exceed the maximum limit of 120, that cannot be predictable"]
            
            # General validation for negative values
            if float_value < 0:
                invalid_values.append(value)
                valid = False

        except ValueError:
            invalid_values.append(value)  # Add invalid input
            valid = False
            
    return valid, invalid_values  # Return only the invalid input values





















# User Dashboard Page
if selected == 'User Dashboard':
    st.title('User Health Dashboard')

    # User input for age, weight, height
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
    with col2:
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=70.0)
    with col3:
        height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=170.0)

    if st.button('Calculate BMI', key='bmi_button'):
        # Calculate BMI
        height_m = height / 100  # Convert height to meters
        bmi = weight / (height_m ** 2)  # BMI formula

        # Display results
        st.success(f"Your BMI is: {bmi:.2f}")

        # Prepare data for visualization
        data = {
            'Metric': ['Age', 'Weight', 'Height', 'BMI'],
            'Value': [age, weight, height, bmi]
        }
        df = px.data.tips()
        fig = px.bar(data_frame=data, x='Metric', y='Value', title='User Health Metrics')
        st.plotly_chart(fig)


if selected == 'Nearby Hospital Finder':
    st.title('Nearby Hospital Finder')


    # Input for location
    location = st.text_input("Enter your location (e.g., city, address)", "New York")

    # Create a Google Maps search URL
    google_maps_url = f"https://www.google.com/maps/search/hospitals+near+{location}"

    # Provide a clickable link to open Google Maps in a new tab
    st.markdown(f"""
        <a href="{google_maps_url}" target="_blank">
        Open Google Maps to search for hospitals near {location}</a>
    """, unsafe_allow_html=True)
    
    

    
    
 



# Sample meal recommendation data with images and recipes for Diabetes and Heart Disease
diabetes_meals = [
    
    {
        "name": "Quinoa Salad with Avocado", 
        "image": "https://bing.com/th?id=OSK.7cb5856af4eb17306e31b0d2ddecf4ea",
        "recipe": "To make a quinoa salad with avocado, you can cook 1 cup of quinoa according to package instructions. Allow it to cool, then mix it with diced avocado, chopped cucumber, cherry tomatoes, red onion, and cilantro. For dressing, whisk together olive oil, lime juice, salt, and pepper, and pour it over the salad. Toss gently and serve chilled."
    },
    {
        "name": "Greek Yogurt with Berries", 
        "image": "https://bing.com/th?id=OSK.2b59d06bd70e8e1925ea7baad2c23ff4",
        "recipe": "In a bowl, add the Greek yogurt, Top it with the mixed berries, Drizzle with honey or maple syrup if desired, Add granola or nuts for crunch (optional), Mix gently and enjoy!"
    },
    {
     "name": "Chickpea and Spinach Curry",
     "image": "https://www.wearesovegan.com/wp-content/uploads/2019/03/veganspinachchickpeacurryrecipe-t1.jpg",
     "recipe": """1 can chickpeas (rinsed and drained),2 cups fresh spinach, 1 onion, diced, 2 garlic cloves, minced, 1 teaspoon curry powder, 1 can diced tomatoes (no added sugar), Olive oil"""
     },
    {
     "name": "Stuffed Bell Peppers",
     "image": "https://bellyfull.net/wp-content/uploads/2021/01/Stuffed-Peppers-blog-768x1024.jpg",
     "recipe": """4 bell peppers (any color), 1 cup cooked brown rice or quinoa, 1 can black beans (rinsed and drained), 1 cup diced tomatoes (fresh or canned, no added sugar), 1 teaspoon cumin, ½ teaspoon chili powder, ½ cup shredded low-fat cheese (optional)"""
     },
    {
     "name": "Cauliflower Fried Rice",
     "image": "https://detoxinista.com/wp-content/uploads/2019/07/cauliflower-fried-rice-recipe.jpg",
     "recipe": """1 head cauliflower, grated or processed into rice, 2 eggs (optional, can omit for vegan), 1 cup mixed vegetables (such as peas, carrots, and bell peppers), 3 green onions, chopped, 2 tablespoons low-sodium soy sauce or tamari, 1 tablespoon sesame oil"""
     },
    {
     "name": "Almond Butter and Apple Slices",
     "image": "https://th.bing.com/th/id/R.68b13925e592ca1a4c751d0b15a3b8ca?rik=4LNicLhGt6C%2bvw&riu=http%3a%2f%2fcdn.shopify.com%2fs%2ffiles%2f1%2f0573%2f6526%2f6626%2farticles%2fApple_Slices_with_Almond_Butter.jpg%3fv%3d1674858298&ehk=NhBnaqmb2x8A9oNhHMJoowivU9TiY0EOZfaZAISBqPs%3d&risl=&pid=ImgRaw&r=0",
     "recipe": """1 medium apple (sliced), 2 tablespoons natural almond butter (no added sugar)"""
     },
    {
     "name": "Egg and Spinach Breakfast Muffins",
     "image": "https://i.pinimg.com/originals/4a/ed/4a/4aed4ab547b388bd253fd5469b69bd42.jpg",
     "recipe": """6 large eggs, 1 cup fresh spinach, chopped, ½ cup diced bell peppers, ¼ cup feta cheese (optional), Salt and pepper to taste"""
     },
    {
     "name": "Cabbage and Sausage Stir-Fry",
     "image": "https://www.wholesomeyum.com/wp-content/uploads/2020/12/wholesomeyum-fried-cabbage-and-sausage-recipe-12.jpg",
     "recipe": """1 small head of green cabbage, sliced, 1 onion, sliced, 2 sausages (turkey or chicken for lower fat), 2 tablespoons olive oil, Salt and pepper to taste"""
     },
    {
     "name": "Berry Chia Seed Pudding",
     "image": "https://plantyou.com/wp-content/uploads/2023/01/DSC03586-2-1400x1864.jpg",
     "recipe": """1 cup unsweetened almond milk, ¼ cup chia seeds, 1 teaspoon vanilla extract, 1 cup mixed berries (strawberries, blueberries, raspberries), Stevia or erythritol for sweetness (optional)"""
     },
    {
     "name": "Roasted Vegetable Medley",
     "image": "https://www.allrecipes.com/thmb/rrplCGJkonMYNIkhRtw1NrXKEww=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/165649roasted-vegetable-medley-DDMFS-001-4x3-f9c51738278e4c92aa53d51250f4ed10.jpg",
     "recipe": """1 zucchini, chopped, 1 bell pepper, chopped, 1 cup broccoli florets, 1 tablespoon olive oil, 1 teaspoon Italian seasoning, Salt and pepper to taste"""
     },
    {
        "name": "Grilled Salmon with Vegetables", 
        "image": "https://bing.com/th?id=OSK.d1d049c30a65f799c99c1c1e098de16e",
        "recipe": """1 medium zucchini, halved lengthwise, 2 red, orange and/or yellow bell peppers, trimmed, halved and seeded, 1 medium red onion, cut into 1-inch wedges, 1 tablespoon extra-virgin olive oil, ½ teaspoon salt, divided, ½ teaspoon ground pepper, 1 ¼ pounds salmon fillet, cut into 4 portions, ¼ cup thinly sliced fresh basil, 1 lemon, cut into 4 wedges"""
    },
    
    
]

heart_disease_meals = [
    {
        "name": "Leafy Green Salad with Olive Oil", 
        "image": "path_to_images/heart_meal1.jpg",
        "recipe": "Recipe for Leafy Green Salad with Olive Oil..."
    },
    {
        "name": "Oats with Fresh Fruits", 
        "image": "path_to_images/heart_meal2.jpg",
        "recipe": "Recipe for Oats with Fresh Fruits..."
    },
    {
        "name": "Baked Chicken with Asparagus", 
        "image": "path_to_images/heart_meal3.jpg",
        "recipe": "Recipe for Baked Chicken with Asparagus..."
    }
]

# Feature: Food and Diet Recommendations
if selected == "Food and Diet Recommendations":
    st.header("Personalized Food and Diet Recommendations")

    # User selects their condition
    condition = st.selectbox("Select your health condition", ["Diabetes", "Heart Disease", "Parkinson's", "General Health"])

    # Display meal recommendations with images in 2 columns (Left: food name + image, Right: View Recipe button)
    if condition == "Diabetes":
        st.subheader("Diet Recommendations for Diabetes")
        for meal in diabetes_meals:
            col1, col2 = st.columns([1, 1])  # Create 2 columns

            with col1:  # Left side for image and name
                st.image(meal["image"], caption=meal["name"], use_column_width=True)

            with col2:  # Right side for recipe button
                if st.button(f"View Recipe for {meal['name']}", key=meal["name"]):
                    st.write(meal["recipe"])  # Display the recipe when button is clicked

    elif condition == "Heart Disease":
        st.subheader("Diet Recommendations for Heart Disease")
        for meal in heart_disease_meals:
            col1, col2 = st.columns([1, 1])  # Create 2 columns

            with col1:  # Left side for image and name
                st.image(meal["image"], caption=meal["name"], use_column_width=True)

            with col2:  # Right side for recipe button
                if st.button(f"View Recipe for {meal['name']}", key=meal["name"]):
                    st.write(meal["recipe"])  # Display the recipe when button is clicked

    else:
        st.subheader("General Health Recommendations")
        st.write("Maintain a balanced diet rich in fruits, vegetables, lean protein, and whole grains.")
 
    
    
    
    
    
    
    
    
    
    
    
    


        
        
        
      




# Function to create the PDF for the health info card
def create_health_info_card_pdf(name, allergies, medications, emergency_contact):
    # Define card size (adjust dimensions if necessary)
    card_width = 200  # width of the card
    card_height = 125  # height of the card

    buffer = io.BytesIO()

    # Create PDF object
    c = canvas.Canvas(buffer, pagesize=letter)

    # Set position for text
    text_x = 50
    text_y = 700

    # Add content to the PDF
    c.drawString(text_x, text_y, f"Name: {name}")
    c.drawString(text_x, text_y - 20, f"Allergies: {allergies}")
    c.drawString(text_x, text_y - 40, f"Medications: {medications}")
    c.drawString(text_x, text_y - 60, f"Emergency Contact: {emergency_contact}")

    # Finalize the PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer








# Function to create the PDF for the health info card
def create_health_info_card_pdf(name, condition, medications, emergency_contact, specific_instructions):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add Health Assistant name and logo at the top
    text_x = 50
    top_y = 750  # Y position for top content
    c.drawString(text_x, top_y, "Generated by Health Assistant")

    # Adding logo (replace 'logo_path' with the path to your logo image)
    logo_path = "C:/Users/FATHIMA MUSKAN/Downloads/White and Blue Modern Health Clinic Logo/1.png"  # Make sure to have the correct path to the logo file
    logo = ImageReader(logo_path)
    c.drawImage(logo, text_x + 250, top_y - 20, width=1 * inch, height=1 * inch)

    # Add user content to the PDF
    text_y = top_y - 100  # Starting position below the logo
    c.drawString(text_x, text_y, f"Name: {name}")
    c.drawString(text_x, text_y - 20, f"Condition: {condition}")
    c.drawString(text_x, text_y - 40, f"Medications: {medications}")
    c.drawString(text_x, text_y - 60, f"Emergency Contact: {emergency_contact}")
    c.drawString(text_x, text_y - 80, f"Specific Emergency Instructions: {specific_instructions}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer



# Main content based on selection
if selected == 'Emergency Health Info Card':
    st.title("Emergency Health Info Card")

    # Input fields for the health info card
    name = st.text_input("Name")
    condition = st.selectbox("Select Condition", ["Diabetes", "Heart Disease", "Parkinson's Disease"])
    medications = st.text_input("Medications")
    emergency_contact = st.text_input("Emergency Contact")

    # Disease-specific emergency instructions
    if condition == "Diabetes":
        specific_instructions = st.text_area("Specific Instructions", 
            "Monitor blood sugar levels. If unconscious, provide emergency glucose gel or glucagon.")
    elif condition == "Heart Disease":
        specific_instructions = st.text_area("Specific Instructions", 
            "Call 911 for chest pain. Administer aspirin and nitroglycerin if prescribed.")
    elif condition == "Parkinson's Disease":
        specific_instructions = st.text_area("Specific Instructions", 
            "Help maintain mobility and avoid falls. Administer medications on time.")

    # Generate PDF when button is clicked
    if st.button("Generate Health Info Card"):
        if name and emergency_contact and condition:
            pdf_buffer = create_health_info_card_pdf(name, condition, medications, emergency_contact, specific_instructions)
            st.download_button(
                label="Download Health Info Card",
                data=pdf_buffer,
                file_name="health_info_card.pdf",
                mime="application/pdf",
            )
        else:
            st.error("Please fill out the required fields.")







    

    

   

    
    
    
    


            
           
    




        
        
        
        
# Report Analyzer in the Sidebar
with st.sidebar:
    st.header("Report Analyzer for Diabetes")
    uploaded_file = st.file_uploader("Upload a PNG of Diabetes Risk Factors", type=["png"])

    if uploaded_file is not None:
        # Load the image using PIL
        from PIL import Image
        image = Image.open(uploaded_file)

        # Perform analysis on the uploaded report (mock analysis for demonstration)
        st.image(image, caption='Uploaded Diabetes Risk Factors Report', use_column_width=True)
        
        # Analyze the report (dummy analysis for demonstration purposes)
        analysis_results = "The analysis of the report is based on the uploaded diabetes risk factors."
        worst_thing = "The highest glucose level recorded is concerning."
        good_thing = "The BMI level is within a normal range."
        suggestion = "Consider consulting a healthcare professional for personalized advice."

        # Display the analysis results
        st.subheader("Report Analysis")
        st.write(analysis_results)
        
        st.subheader("Worst Thing in the Report")
        st.write(worst_thing)
        
        st.subheader("Good Thing in the Report")
        st.write(good_thing)

        st.subheader("Suggestions for Improvement")
        st.write(suggestion)
    
 
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

            # Step 1: Diabetes prediction result
            if diab_prediction[0] == 1:
                diab_diagnosis = 'The person is diabetic'
                st.success(diab_diagnosis)

                # Step 2: Health Recommendations (if diabetic)
                health_recommendation = '''
                *Health Recommendations for Diabetes:*
                - Maintain a balanced diet with low sugar and high fiber.
                - Regular physical activity, such as 30 minutes of moderate exercise daily.
                - Monitor blood glucose levels regularly.
                - Stay hydrated and avoid sugary drinks.
                - Consult a doctor for a personalized medication plan.
                '''
                st.info(health_recommendation)
                
                # Defining risk thresholds
                risk_factors = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
                categories = [
                    categorize_risk(float(Pregnancies), 0, 6),
                    categorize_risk(float(Glucose), 99, 141),
                    categorize_risk(float(BloodPressure), 60, 80),
                    categorize_risk(float(SkinThickness), 0, 32),
                    categorize_risk(float(Insulin), 0, 129),
                    categorize_risk(float(BMI), 27.3, 36.6),
                    categorize_risk(float(DiabetesPedigreeFunction), 0.24, 0.63),
                    categorize_risk(float(Age), 24, 50)
                ]
                
                # Visualize with risk categories
                visualize_risk_factors_with_categories(risk_factors, user_input, categories, "Diabetes Risk Factors")

                # Step 3: Exercise Recommendations with pictures (if diabetic)
                st.subheader("Exercise Recommendations for Diabetes")
                st.write("""
                Regular physical activity is essential for managing diabetes. Below are some recommended exercises:
                """)

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.image("https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", caption="Walking", use_column_width=True)
                    st.write("A simple exercise, 30 minutes of brisk walking daily can help improve blood sugar control.")
                
                with col2:
                    st.image("https://th.bing.com/th/id/OIP.tZUiikH4avRMzaqvI3hJHwHaFj?w=285&h=214&c=7&r=0&o=5&dpr=2&pid=1.7", caption="Yoga", use_column_width=True)
                    st.write("Yoga improves flexibility, reduces stress, and enhances overall health for diabetes management.")
                
                with col3:
                    st.image("data:image/jpeg;base64,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", caption="Strength Training", use_column_width=True)
                    st.write("Incorporating weight training can help build muscle and improve insulin sensitivity.")

            else:
                diab_diagnosis = 'The person is not diabetic'
                st.success(diab_diagnosis)
        else:
            diab_diagnosis = 'The entered values are invalid: ' + ', '.join(feedback)
            st.error(diab_diagnosis)
            
            
import streamlit as st

# Inject CSS for background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/006/712/981/original/abstract-health-medical-science-healthcare-icon-digital-technology-science-concept-modern-innovation-treatment-medicine-on-hi-tech-future-blue-background-for-wallpaper-template-web-design-vector.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Report Analyzer in the Sidebar
with st.sidebar:
    st.header("Report Analyzer for Heart Disease")
    uploaded_file = st.file_uploader("Upload a PNG of Heart Disease Risk Factors", type=["png"])

    if uploaded_file is not None:
        # Load the image using PIL
        from PIL import Image
        image = Image.open(uploaded_file)

        # Perform analysis on the uploaded report (mock analysis for demonstration)
        st.image(image, caption='Uploaded Heart Disaese Risk Factors Report', use_column_width=True)
        
        # Analyze the report (dummy analysis for demonstration purposes)
        analysis_results = "The analysis of the report is based on the uploaded diabetes risk factors."
        worst_thing = "The highest glucose level recorded is concerning."
        good_thing = "The BMI level is within a normal range."
        suggestion = "Consider consulting a healthcare professional for personalized advice."

        # Display the analysis results
        st.subheader("Report Analysis")
        st.write(analysis_results)
        
        st.subheader("Worst Thing in the Report")
        st.write(worst_thing)
        
        st.subheader("Good Thing in the Report")
        st.write(good_thing)

        st.subheader("Suggestions for Improvement")
        st.write(suggestion)


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
        thalach = st.text_input('Maximum Heart Rate Achieved')
    with col3:
        exang = st.text_input('Exercise Induced Angina (1 = yes; 0 = no)')
    with col1:
        oldpeak = st.text_input('ST depression induced by exercise relative to rest')
    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')
    with col3:
        ca = st.text_input('Number of major vessels (0-3) colored by fluoroscopy')
    with col1:
        thal = st.text_input('Thalassemia (1 = normal; 2 = fixed defect; 3 = reversable defect)')
    
    heart_diagnosis = ''
    health_recommendation_hd = ''

    if st.button('Heart Disease Test Result', key='heart_button'):
        user_input_hd = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        # Validate the inputs
        valid_hd, feedback_hd = validate_inputs(user_input_hd)

        if valid_hd:
            heart_prediction = heart_disease_model.predict([user_input_hd])

            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person is at risk of heart disease'
                health_recommendation_hd = '''
                *Health Recommendations for Heart Disease:*
                - Follow a heart-healthy diet low in saturated fat and cholesterol.
                - Engage in regular physical activity.
                - Avoid tobacco and limit alcohol consumption.
                - Manage stress effectively.
                - Regular health check-ups and blood pressure monitoring.
                '''
            else:
                heart_diagnosis = 'The person is not at risk of heart disease'
        else:
            heart_diagnosis = 'The entered values are invalid: ' + ', '.join(feedback_hd)

    st.success(heart_diagnosis)
    st.info(health_recommendation_hd)
    
    
    
# Report Analyzer in the Sidebar
with st.sidebar:
    st.header("Report Analyzer for Parkinsons")
    uploaded_file = st.file_uploader("Upload a PNG of Parkinson's Risk Factors", type=["png"])

    if uploaded_file is not None:
        # Load the image using PIL
        from PIL import Image
        image = Image.open(uploaded_file)

        # Perform analysis on the uploaded report (mock analysis for demonstration)
        st.image(image, caption='Uploaded Parkinsons Risk Factors Report', use_column_width=True)
        
        # Analyze the report (dummy analysis for demonstration purposes)
        analysis_results = "The analysis of the report is based on the uploaded diabetes risk factors."
        worst_thing = "The highest glucose level recorded is concerning."
        good_thing = "The BMI level is within a normal range."
        suggestion = "Consider consulting a healthcare professional for personalized advice."

        # Display the analysis results
        st.subheader("Report Analysis")
        st.write(analysis_results)
        
        st.subheader("Worst Thing in the Report")
        st.write(worst_thing)
        
        st.subheader("Good Thing in the Report")
        st.write(good_thing)

        st.subheader("Suggestions for Improvement")
        st.write(suggestion)

# Parkinson's Prediction Page
if selected == "Parkinson's Prediction":
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2 = st.columns(2)
    with col1:
        fo = st.text_input("MDVP: Fo (Hz)")
    with col2:
        fhi = st.text_input("MDVP: Fhi (Hz)")
    with col1:
        flo = st.text_input("MDVP: Flo (Hz)")
    with col2:
        Jitter = st.text_input("MDVP: Jitter (%)")
    with col1:
        JitterAbs = st.text_input("MDVP: Jitter (Abs)")
    with col2:
        RAP = st.text_input("MDVP: RAP")
    with col1:
        PPQ = st.text_input("MDVP: PPQ")
    with col2:
        DDP = st.text_input("MDVP: DDP")
    with col1:
        Shimmer = st.text_input("MDVP: Shimmer")
    with col2:
        ShimmerDB = st.text_input("MDVP: Shimmer (dB)")
    with col1:
        APQ3 = st.text_input("Shimmer: APQ3")
    with col2:
        APQ5 = st.text_input("Shimmer: APQ5")
    with col1:
        APQ = st.text_input("Shimmer: APQ")
    with col2:
        DDA = st.text_input("Shimmer: DDA")
    with col1:
        NHR = st.text_input("NHR")
    with col2:
        HNR = st.text_input("HNR")
    with col1:
        RPDE = st.text_input("RPDE")
    with col2:
        DFA = st.text_input("DFA")
    with col1:
        spread1 = st.text_input("Spread1")
    with col2:
        spread2 = st.text_input("Spread2")
    with col1:
        D2 = st.text_input("D2")
    with col2:
        Epsilon = st.text_input("Epsilon")

    parkinsons_diagnosis = ''
    health_recommendation_pd = ''

    if st.button('Parkinson\'s Test Result', key='parkinsons_button'):
        user_input_pd = [fo, fhi, flo, Jitter, JitterAbs, RAP, PPQ, DDP, Shimmer, ShimmerDB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, Epsilon]

        # Validate the inputs
        valid_pd, feedback_pd = validate_inputs(user_input_pd)

        if valid_pd:
            parkinsons_prediction = parkinsons_model.predict([user_input_pd])

            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = 'The person is likely to have Parkinson\'s disease'
                health_recommendation_pd = '''
                *Health Recommendations for Parkinson's Disease:*
                - Regular physical activity and exercise.
                - Maintain a balanced diet rich in fruits, vegetables, and whole grains.
                - Engage in activities that stimulate your brain, like puzzles or reading.
                - Ensure regular check-ups with healthcare providers.
                - Consider physical therapy to improve mobility and balance.
                '''
                st.title("Non-Motor Symptom Tracking")

                # Mood and Anxiety Monitoring Section
                st.header("Mood and Anxiety Monitoring")
                mood = st.radio("How have you been feeling lately?", ("Very Bad", "Bad", "Neutral", "Good", "Very Good"))
                anxiety_level = st.slider("Rate your anxiety level (1-10)", 1, 10)

                if st.button("Submit Mood and Anxiety Data"):
                    st.success("Thank you for your input! Your mood and anxiety levels have been recorded.")
                    
                    # Suggestions based on mood
                    mood_suggestions = {
                        "Very Bad": "Consider talking to a healthcare professional. Engage in calming activities like meditation.",
                        "Bad": "Try to reach out to friends or family. Gentle exercises or walking may help.",
                        "Neutral": "Maintain your current routine, and consider journaling your thoughts.",
                        "Good": "Great to hear! Keep up the positive activities. Perhaps try something new for excitement.",
                        "Very Good": "Fantastic! Share your positivity with others and continue your good habits."
                    }
                    
                    # Suggestions based on anxiety level
                    if anxiety_level <= 3:
                        anxiety_suggestion = "Your anxiety levels seem low. Keep practicing relaxation techniques!"
                    elif anxiety_level <= 7:
                        anxiety_suggestion = "Consider deep breathing exercises or light physical activity to manage anxiety."
                    else:
                        anxiety_suggestion = "It might be helpful to consult with a mental health professional."

                    st.write("### Suggestions")
                    st.write("**Mood Suggestion:** " + mood_suggestions[mood])
                    st.write("**Anxiety Suggestion:** " + anxiety_suggestion)

                # Autonomic Symptoms Tracking Section
                st.header("Autonomic Symptoms Tracking")
                sweating = st.checkbox("Do you experience excessive sweating?")
                constipation = st.checkbox("Do you experience constipation?")
                urinary_problems = st.checkbox("Do you have urinary problems?")

                if st.button("Submit Autonomic Symptoms Data"):
                    symptoms = []
                    if sweating:
                        symptoms.append("Excessive sweating")
                    if constipation:
                        symptoms.append("Constipation")
                    if urinary_problems:
                        symptoms.append("Urinary problems")

                    st.success("Thank you! Your autonomic symptoms have been recorded.")
                    if symptoms:
                        st.write("You reported: " + ", ".join(symptoms))
                        
                        # Suggestions based on symptoms
                        suggestions = []
                        if sweating:
                            suggestions.append("Try to stay cool, wear breathable fabrics, and consider speaking to your doctor.")
                        if constipation:
                            suggestions.append("Increase fiber intake, drink plenty of water, and try regular exercise.")
                        if urinary_problems:
                            suggestions.append("Consult with a healthcare provider for appropriate advice and management strategies.")

                        st.write("### Suggestions for Autonomic Symptoms:")
                        for suggestion in suggestions:
                            st.write("- " + suggestion)
                # Set up the canvas
                st.title("Handwriting Analysis (Micrographia Detection)")

                # Create a drawing canvas
                canvas_result = st_canvas(
                    fill_color="rgba(255, 165, 0, 0.3)",  # Color for the drawing
                    stroke_width=2,  # Pen width
                    stroke_color="black",  # Pen color
                    background_color="white",  # Background color
                    width=500,  # Canvas width
                    height=200,  # Canvas height
                    drawing_mode="freedraw",  # Drawing mode
                    key="canvas",
                )

                # Analysis function for Micrographia detection
                def analyze_handwriting(image_data):
                    # Convert to grayscale
                    img_gray = cv2.cvtColor(image_data, cv2.COLOR_RGBA2GRAY)
                    
                    # Thresholding to get a binary image (black/white)
                    _, img_thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
                    
                    # Find contours of the handwriting
                    contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    # Get bounding boxes and analyze
                    total_area = 0
                    total_stroke_length = 0
                    stroke_areas = []
                    for contour in contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        stroke_area = w * h
                        stroke_areas.append(stroke_area)
                        total_area += stroke_area
                        total_stroke_length += w  # Use width as stroke length approximation
                    
                    # Results
                    num_strokes = len(contours)
                    avg_stroke_area = total_area / num_strokes if num_strokes > 0 else 0
                    avg_stroke_length = total_stroke_length / num_strokes if num_strokes > 0 else 0

                    return {
                        "num_strokes": num_strokes,
                        "total_area": total_area,
                        "avg_stroke_area": avg_stroke_area,
                        "avg_stroke_length": avg_stroke_length,
                        "min_stroke_area": min(stroke_areas) if stroke_areas else 0,
                        "max_stroke_area": max(stroke_areas) if stroke_areas else 0
                    }

                # Process the handwriting after drawing
                if canvas_result.image_data is not None:
                    st.image(canvas_result.image_data, caption="Your handwriting", use_column_width=True)

                    # Convert to numpy array
                    img_data = np.array(canvas_result.image_data, dtype=np.uint8)

                    # Analyze the handwriting size and stroke width
                    results = analyze_handwriting(img_data)

                    # Display analysis results
                    st.subheader("Handwriting Analysis Results:")
                    st.write(f"Number of Strokes: {results['num_strokes']}")
                    st.write(f"Total Handwriting Area: {results['total_area']} pixels")
                    st.write(f"Average Stroke Area: {results['avg_stroke_area']} pixels")
                    st.write(f"Average Stroke Length: {results['avg_stroke_length']} pixels")
                    st.write(f"Smallest Stroke Area: {results['min_stroke_area']} pixels")
                    st.write(f"Largest Stroke Area: {results['max_stroke_area']} pixels")
                
            else:
                parkinsons_diagnosis = 'The person is not likely to have Parkinson\'s disease'
        else:
            parkinsons_diagnosis = 'The entered values are invalid: ' + ', '.join(feedback_pd)

    st.success(parkinsons_diagnosis)
    st.info(health_recommendation_pd)
    


    



    












       










     
    


    
    
    
    




