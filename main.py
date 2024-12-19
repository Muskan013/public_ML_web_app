



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
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2







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
        'Multiple Disease Management System',
        ['User Dashboard', "Parkinson's Management","Exercise Recommendations","Food and Diet Recommendations", "Nearby Hospital Finder","Emergency Health Info Card" ],
        icons=['people', 'person','person-workspace', 'egg-fried',  'hospital', 'card-heading'],
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
        "name": "Oatmeal with Berries and Nuts", 
        "image": "https://joybauer.com/wp-content/uploads/2017/12/Oatmeal-with-berries2.jpg",
        "recipe": "1/2 cup oats, 1 cup water or almond milk, 1/2 cup mixed berries, 1 tablespoon chopped walnuts, a pinch of cinnamon."
    },
    {
        "name": "Avocado Toast with Poached Egg", 
        "image": "https://data.thefeedfeed.com/static/2021/04/06/1617726496606c8c20a7a82.jpg",
        "recipe": "1 slice whole-grain bread, 1/2 avocado, 1 egg, Salt, pepper, and red pepper flakes to taste"
    },
    {
        "name": "Stuffed Lauki (Bottle Gourd) Paratha", 
        "image": "https://www.livingsmartandhealthy.com/wp-content/uploads/2023/08/lauki-paratha-33.jpg",
        "recipe": "1 cup grated bottle gourd (lauki), 1 cup whole wheat flour, 1/4 teaspoon carom seeds (ajwain), Salt, cumin powder, and black pepper to taste, 1 teaspoon oil"
    },
    {
        "name": "Chia Seed Pudding with Almond Milk", 
        "image": "https://www.wellplated.com/wp-content/uploads/2020/04/Coconut-Chia-Pudding-Best-Recipe.jpg",
        "recipe": "1/4 cup chia seeds, 1 cup almond milk (unsweetened), 1 teaspoon honey (optional), Fresh fruit like berries for topping"
    },
    {
        "name": "Greek Yogurt with Honey and Berries", 
        "image": "https://cdn.apartmenttherapy.info/image/upload/v1561142436/k/Photo/Recipes/2019-07-recipe-balsamic-berries-honey-yogurt/Balsamic-Berries-Honey-Yogurt_061.jpg",
        "recipe": "1/2 cup plain Greek yogurt, 1/4 cup mixed berries, 1 teaspoon honey"
    },
    {
        "name": "Palak Dal (Spinach Lentils)", 
        "image": "https://vspiceroute.com/wp-content/uploads/2022/11/6EC9A673-81F0-4B3A-83A7-DB5B5E35707A.jpeg",
        "recipe": "1 cup split yellow moong dal (or toor dal), 2 cups spinach, chopped, 1/4 cup tomatoes, chopped, 1/2 teaspoon turmeric powder, 1/2 teaspoon cumin seeds, 1/2 teaspoon mustard seeds, 1 green chili, slit (optional), Salt and 1 tablespoon oil"
    },
    {
        "name": "Vegetable Khichdi", 
        "image": "https://www.indianveggiedelight.com/wp-content/uploads/2020/09/quinoa_khichdi_1-1152x1536.jpg",
        "recipe": "1/2 cup brown rice, 1/4 cup split yellow moong dal, 1/4 cup mixed vegetables (carrot, peas, beans),1/2 teaspoon turmeric powder, 1/2 teaspoon cumin seeds, Salt, 1 tablespoon ghee or oil"
    },
    {
        "name": "Masoor Dal and Vegetable Soup", 
        "image": "https://cdn.shopify.com/s/files/1/0144/6674/4377/articles/Masoor_Dal_Soup_5000x.jpeg?v=1568991682",
        "recipe": "1 cup split red lentils (masoor dal), 1/4 cup carrots, diced, 1/4 cup spinach, chopped, 1/4 cup tomatoes, chopped, 1/2 teaspoon cumin powder, 1/2 teaspoon black pepper, Salt, 1 tablespoon oil"
    },
    {
        "name": "Tandoori Grilled Vegetables", 
        "image": "https://th.bing.com/th/id/R.c3a532b8e25a73b24e05dcd1bdcafefd?rik=ACimudNM3X%2bDvw&riu=http%3a%2f%2fyourcookingpal.com%2fwp-content%2fuploads%2f2016%2f11%2fTandoori-Vegetables-final.jpg&ehk=Xg0fQdvcbV1pcPu7xdp76wxtxdVYlCgj4XETfdwBHAY%3d&risl=&pid=ImgRaw&r=0",
        "recipe": "1 cup cauliflower florets, 1/2 cup bell peppers, cut into chunks, 1/2 cup paneer cubes (optional), 1/2 cup yogurt, 1 teaspoon tandoori masala, 1/2 teaspoon red chili powder, Salt and 1 teaspoon oil"
    },
    {
        "name": "Leafy Green Salad with Olive Oil", 
        "image": "https://www.orchardtech.com.au/wp-content/uploads/2021/01/veg.jpg",
        "recipe": "Recipe for Leafy Green Salad with Olive Oil..."
    },
]
parkinson_disease_meals = [
    {
        "name": "Methi Thepla with Greek Yogurt", 
        "image": "https://thumbs.dreamstime.com/b/indian-parantha-stuffed-indian-bread-methi-thepla-stack-indian-flatbread-methi-paratha-fenugreek-gujarati-thepla-potato-125773599.jpg",
        "recipe": "1 cup whole wheat flour, 1/2 cup fresh fenugreek leaves (methi), chopped, 1/4 teaspoon turmeric powder, Salt and cumin seeds to taste, 1 teaspoon olive oil, Greek yogurt (for serving)"
    },
    {
        "name": "Turmeric Almond Milk", 
        "image": "https://th.bing.com/th/id/OIP.53mOf13HLAz71yys4cjQKAAAAA?w=474&h=710&rs=1&pid=ImgDetMain",
        "recipe": "1 cup almond milk (unsweetened), 1/4 teaspoon turmeric powder, 1/4 teaspoon cinnamon, Honey or maple syrup to taste (optional)"
    },
    {
        "name": "Roasted Chickpeas", 
        "image": "https://i1.wp.com/wonkywonderful.com/wp-content/uploads/2017/01/oven-toasted-chickpeas-4.jpg?fit=1285,1285&ssl=1",
        "recipe": "1 cup cooked chickpeas, drained, 1/2 teaspoon turmeric, Salt and black pepper to taste, 1 teaspoon olive oil"
    },
    {
        "name": "Avocado Toast with Pumpkin Seeds", 
        "image": "https://fitfoodiefinds.com/wp-content/uploads/2022/09/Poached-Eggs-1-550x825.jpg",
        "recipe": "1 slice whole-grain bread, toasted, 1/2 ripe avocado, Salt and pepper to taste, 1 teaspoon pumpkin seeds"
    },
    {
        "name": "Fresh Fruit Salad with Nuts", 
        "image": "https://i0.wp.com/foodbylingling.com/wp-content/uploads/2021/06/DSC_0193-scaled.jpg?resize=819%2C1024&ssl=1",
        "recipe": "1/2 cup diced apples, 1/2 cup diced oranges, 1/2 cup grapes, halved, A handful of walnuts or almonds, A sprinkle of cinnamon"
    },
    {
        "name": "Ragi (Finger Millet) Porridge", 
        "image": "https://i.ytimg.com/vi/MG4Jt8Igpmg/maxresdefault.jpg",
        "recipe": "1/4 cup ragi flour, 1 cup water, 1/2 cup milk (almond or regular milk), 1-2 teaspoons jaggery or honey (optional), A pinch of cardamom powder, Chopped nuts (almonds or walnuts)"
    },
    {
        "name": "Vegetable Sambar", 
        "image": "https://vaya.in/recipes/wp-content/uploads/2018/03/Vegetable-Sambar-.jpg",
        "recipe": "1 cup toor dal, cooked and mashed, 1 cup mixed vegetables (carrot, pumpkin, brinjal, drumstick), 1 tomato, chopped, Salt, turmeric, and sambar powder to taste, 1/2 teaspoon mustard seeds, Curry leaves, 1 tablespoon oil"
    },
    {
        "name": "Stuffed Bajra Roti with Vegetable Filling", 
        "image": "https://madhurasrecipe.com/wp-content/uploads/2022/08/mix_veg_paratha__featured-1024x683.jpg",
        "recipe": "1 cup bajra (pearl millet) flour, Warm water (to knead dough), Salt to taste, Filling: 1/2 cup grated carrots, chopped spinach, chopped onions, and seasonings (turmeric, cumin, and black pepper)"
    },
    {
        "name": "Vegetable Pulao with Brown Rice", 
        "image": "https://assets.thehansindia.com/h-upload/2022/09/19/1313036-fried.jpg",
        "recipe": "1 cup brown rice, rinsed, 1 cup mixed vegetables (beans, carrots, peas), 1 small onion, chopped, 1/2 teaspoon cumin seeds, Salt, turmeric, and garam masala to taste, 1 tablespoon olive oil"
    },
    {
        "name": "Sprouted Moong Chaat", 
        "image": "https://sinfullyspicy.com/wp-content/uploads/2022/06/1-683x1024.jpg",
        "recipe": "1 cup sprouted green gram (moong), 1 small cucumber, diced, 1 small tomato, diced, Chopped fresh coriander, Salt, black pepper, and lemon juice to taste"
    },
]

# Feature: Food and Diet Recommendations
if selected == "Food and Diet Recommendations":
    st.header("Personalized Food and Diet Recommendations")

    # User selects their condition
    condition = st.selectbox("Select your health condition", ["Diabetes", "Heart Disease", "Parkinson's Disease", "General Health"])

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

    if condition == "Heart Disease":
        st.subheader("Diet Recommendations for Heart Disease")
        for meal in heart_disease_meals:
            col1, col2 = st.columns([1, 1])  # Create 2 columns

            with col1:  # Left side for image and name
                st.image(meal["image"], caption=meal["name"], use_column_width=True)

            with col2:  # Right side for recipe button
                if st.button(f"View Recipe for {meal['name']}", key=meal["name"]):
                    st.write(meal["recipe"])  # Display the recipe when button is clicked
                    
    if condition == "Parkinson's Disease":
        st.subheader("Diet Recommendations for Parkinson's Disease")
        for meal in parkinson_disease_meals:
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






    

    

   

    
    
    
    


            
           
    




        
        
        



    
    
    
    
 #Report analyzer for parkinson disease   
with st.sidebar:
    st.header("Report Analyzer for Parkinson's Disease")
    uploaded_file = st.file_uploader("Upload a PNG of Parkinson's Disease Risk Factors", type=["png"])

    if uploaded_file is not None:
        # Load the image using PIL
        from PIL import Image
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.image(image, caption="Uploaded Parkinson's Disease Risk Factors Report", use_column_width=True)

        # Perform analysis on the uploaded report (mock analysis for demonstration)
        analysis_results = "The analysis of the report is based on the uploaded Parkinson's disease risk factors."
        worst_thing = "The tremor severity and rigidity levels indicate a high risk."
        good_thing = "The motor function stability appears to be within a manageable range."
        suggestion = "Regular physical therapy and consult a neurologist for medication adjustments."

        # Display the analysis results
        st.subheader("Report Analysis")
        st.write(analysis_results)

        st.subheader("Worst Thing in the Report")
        st.write(worst_thing)

        st.subheader("Good Thing in the Report")
        st.write(good_thing)

        st.subheader("Suggestions for Improvement")
        st.write(suggestion)

    


if selected == "Parkinson's Management":
    st.title("Parkinson's Disease Management System")
    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    parkinsons_diagnosis = ''
    health_recommendation_pd = ''

    if st.button('Parkinson\'s Test Result', key='parkinsons_button'):
        user_input_pd = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
       
        user_input_pd = np.array(user_input_pd, dtype=float)

        parkinsons_prediction = parkinsons_model.predict([user_input_pd])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = 'The person is likely to have Parkinson\'s disease'
            st.success(parkinsons_diagnosis)
            health_recommendation_pd = '''
            *Health Recommendations for Parkinsons Disease:*
            - Regular physical activity and exercise.
            - Maintain a balanced diet rich in fruits, vegetables, and whole grains.
            - Engage in activities that stimulate your brain, like puzzles or reading.
            - Ensure regular check-ups with healthcare providers.
            - Consider physical therapy to improve mobility and balance.
            '''
            st.info(health_recommendation_pd)
            # Define function to categorize risk levels based on thresholds
            def categorize_parkinson_risk(value, low_threshold, high_threshold):
                if value < low_threshold:
                    return 'Low Risk'
                elif value > high_threshold:
                    return 'High Risk'
                else: 
                    return 'Normal'

            # Define function to visualize heart disease risk factors using Plotly with categories
            def visualize_parkinson_disease_risk(factors, values, low_thresholds, high_thresholds, title="Parkinson Disease Risk Analysis"):
                # Categorize each factor based on thresholds
                categories = [categorize_parkinson_risk(value, low, high) for value, low, high in zip(values, low_thresholds, high_thresholds)]
                
                # Create a Plotly bar chart with risk categories
                fig = px.bar(
                    x=factors,
                    y=values,
                    color=categories,
                    labels={'x': 'Parkinson Disease Risk Factors', 'y': 'Values', 'color': 'Risk Category'},
                    title=title,
                    color_discrete_map={
                        'Low Risk': 'green',
                        'Normal': 'blue',
                        'High Risk': 'red'
                    }
                )
                st.plotly_chart(fig)
            # Defining risk thresholds
            risk_factors = ['mdvp:fo(hz)', 'mdvp:fhi(hz)', 'mdvp:flo(hz)', 'mdvp:jitter(%)', 'mdvp:jitter(abs)', 'mdvp:rap', 'mdvp:ppq', 'jitter:ddp', 'mdvp:shimmer','mdvp:shimmer(db)','shimmer:apq3', 'shimmer:apq5', 'mdvp:apq', 'shimmer:dda', 'nhr', 'hnr', 'rpde', 'dfa', 'spread 1', 'spread 2', 'd2', 'ppe']
            categories = [
                categorize_risk(float(fo), 88.3, 150),
                categorize_risk(float(fhi), 100, 200),
                categorize_risk(float(flo), 65.5, 100),
                categorize_risk(float(Jitter_percent), 0, 0.01),
                categorize_risk(float(Jitter_Abs), 0, 0),
                categorize_risk(float(RAP), 0, 0),
                categorize_risk(float(PPQ), 0, 0),
                categorize_risk(float(DDP), 0, 0.01 ),
                categorize_risk(float(Shimmer), 0.01, 0.04),
                categorize_risk(float(Shimmer_dB), 0.1, 0.4 ),
                categorize_risk(float(APQ3), 0.002, 0.01),
                categorize_risk(float(APQ5), 0.003, 0.02),
                categorize_risk(float(APQ), 0.006, 0.03),
                categorize_risk(float(DDA), 0.005, 0.10),
                categorize_risk(float(NHR), 0.01, 0.2 ),
                categorize_risk(float(HNR), 10, 20),
                categorize_risk(float(RPDE), 0.2, 0.4 ),
                categorize_risk(float(DFA), 0.5, 1.0),
                categorize_risk(float(spread1), 0.5, 1.0),
                categorize_risk(float(spread2), 1.0, 1.3),
                categorize_risk(float(D2), 1.0, 1.3),
                categorize_risk(float(PPE), 0.1, 0.3)
                
            ]
            
            # Visualize with risk categories
            visualize_risk_factors_with_categories(risk_factors, user_input_pd, categories, "Parkinson Disease Risk Factors")
            st.subheader("Exercise Recommendations for Parkinson Disease")
            st.write("""
            Regular physical activity is essential for Parkinson Disease Risk Factor. Below are some recommended exercises:
            """)

            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)
            col7, col8, col9 = st.columns(3)
            
            with col1:
                st.image("https://assistinghands.com/34/wp-content/uploads/sites/59/2019/10/Fotolia_78775833_Subscription_Monthly_M.jpg", caption="Big Movements Training (BIG Therapy)", use_column_width=True)
                st.write("This therapy encourages individuals to practice exaggerated movements to counter the small, shuffling steps that are typical in Parkinson’s.")
            
            with col2:
                st.image("https://i.ytimg.com/vi/jWItbongRzQ/maxresdefault.jpg", caption="Marching In Place", use_column_width=True)
                st.write("Helps improve leg strength and balance by focusing on lifting the knees and maintaining rhythm..")
            
            with col3:
                st.image("https://www.verywellfit.com/thmb/UUvsyr6XyBef085zUNQkS6OXKIY=/2182x1454/filters:fill(FFDB5D,1)/Verywell-10-2696048-CalfStretchTowel-1003-598cba640d327a0010ee067b.jpg" , caption="Seated Stretching and Flexibility Exercises", use_column_width=True)                 
                st.write("Stretching exercises can reduce stiffness and improve mobility in the joints and muscles..")
            with col4:
                st.image("https://assets.rebelmouse.io/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZSI6Imh0dHBzOi8vYXNzZXRzLnJibC5tcy8yMjA5NjkwOC9vcmlnaW4uanBnIiwiZXhwaXJlc19hdCI6MTYzODIxNDgzOH0.LcpArmK-MNSqCjjJg1uMz6K-dtGocXefwYsZfZSwT2g/img.jpg" , caption="Strength Training", use_column_width=True)                 
                st.write("Strengthening exercises can help improve balance, flexibility, and coordination.")
            with col5:
                st.image("https://fitnessvolt.com/wp-content/uploads/2020/09/mobility-exercises.jpg", caption="Mobility Exercises", use_column_width=True)  
                st.write("Improving flexibility, posture, and muscle length to help reduce stiffness and prevent falls.")
            
            with col6:
                st.image("https://media.giphy.com/media/3ov9jLcq56yBYpymsA/giphy.gif", caption="Dance Therapy", use_column_width=True)                 
                st.write("Dance movements can enhance balance and coordination. Many people with Parkinson’s Disease enjoy dancing as an enjoyable form of therapy.")
            
        else:
            parkinsons_diagnosis = "The person does not have Parkinson's disease"
            st.success(parkinsons_diagnosis)


        


    
    
    
    
    
    
    
    
    
    
    
    
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
 

# Title of the app
        st.title("Parkinson's Disease Visualization")

# Adding an image
# Replace "path_to_your_image.jpg" with the actual image file path
        st.image("C:/Users/FATHIMA MUSKAN/Downloads/detect_parkinsons_dataset.webp",
         caption="Visualization of Healthy vs Parkinson's Drawings", 
         use_container_width=True)
        
# Define example exercise lists
diabetes_exercises = [
    {"name": "Walking", "image": "https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Walk for 30 minutes daily at a moderate pace."},
    {"name": "Yoga", "image": "https://th.bing.com/th/id/OIP.tZUiikH4avRMzaqvI3hJHwHaFj?w=285&h=214&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Perform gentle yoga poses focusing on flexibility and breathing."},
    {"name": "Cycling", "image": "https://th.bing.com/th/id/OIP.4Bm7Duuhp5BsN95fl6-sfAAAAA?rs=1&pid=ImgDetMain", "instructions": "Ride a bike for 20-30 minutes to boost cardiovascular health."},
    {"name": "Step Aerobics", "image": "https://th.bing.com/th/id/OIP.Ol1CPHgk2gnjb7iLZM9I4QHaHa?rs=1&pid=ImgDetMain", "instructions": "Step one foot onto the platform, then bring the other up; step down one foot at a time."},
    {"name": "Jump Rope", "image": "https://everydaypower.com/wp-content/uploads/2016/11/Benefits-of-Jumping-Rope-During-Your-Morning-Routine.jpg", "instructions": "Hold the rope handles at hip height, elbows close to your sides, and swing the rope overhead."},
    {"name": "Stair Climbing", "image": "https://www.fitnesseducation.edu.au/wp-content/uploads/2020/10/Walking-stairs-e1587693663738.jpg", "instructions": "Step up onto each stair with one foot, followed by the other, then step back down."},
    # Add more exercises as needed
]

heart_disease_exercises = [
    {"name": "Light Jogging", "image": "https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Jog lightly for 20-30 minutes, avoiding excessive exertion."},
    {"name": "Stretching", "image": "https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Stretch major muscle groups to maintain flexibility and improve circulation."},
    {"name": "Swimming", "image": "https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Swim at a gentle pace to reduce strain on the joints and heart."},
    # Add more exercises as needed
]

parkinson_disease_exercises = [
    {"name": "Tai Chi", "image": "https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Practice Tai Chi for balance and coordination."},
    {"name": "Strength Training", "image": "https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Use light weights to strengthen muscles and improve mobility."},
    {"name": "Dance Therapy", "image": "https://th.bing.com/th/id/OIP.GP-Ayzw6dlN_X1zsVL_6xQHaE7?w=251&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", "instructions": "Engage in dancing to enhance motor skills and flexibility."},
    # Add more exercises as needed
]

# Feature: Exercise Recommendations
if selected == "Exercise Recommendations":
    st.header("Personalized Exercise Recommendations")

    # User selects their condition
    condition = st.selectbox("Select your health condition", ["Diabetes", "Heart Disease", "Parkinson's Disease", "General Health"])

    # Display exercise recommendations with images in a 3x3 grid
    if condition == "Diabetes":
        st.subheader("Exercise Recommendations for Diabetes")
        cols = [st.columns(3) for _ in range(3)]  # Create 3 rows with 3 columns each

        # Loop through the exercises and display them in the 3x3 grid
        for idx, exercise in enumerate(diabetes_exercises):
            row = idx // 3
            col = idx % 3
            with cols[row][col]:  # Select the appropriate cell in the grid
                st.image(exercise["image"], caption=exercise["name"], use_column_width=True)
                if st.button(f"View Instructions for {exercise['name']}", key=f"{exercise['name']}_{idx}"):
                    st.write(exercise["instructions"])  # Display the instructions when button is clicked

    elif condition == "Heart Disease":
        st.subheader("Exercise Recommendations for Heart Disease")
        cols = [st.columns(3) for _ in range(3)]  # Create 3 rows with 3 columns each

        for idx, exercise in enumerate(heart_disease_exercises):
            row = idx // 3
            col = idx % 3
            with cols[row][col]:
                st.image(exercise["image"], caption=exercise["name"], use_column_width=True)
                if st.button(f"View Instructions for {exercise['name']}", key=f"{exercise['name']}_{idx}"):
                    st.write(exercise["instructions"])

    elif condition == "Parkinson's Disease":
        st.subheader("Exercise Recommendations for Parkinson's Disease")
        cols = [st.columns(3) for _ in range(3)]  # Create 3 rows with 3 columns each

        for idx, exercise in enumerate(parkinson_disease_exercises):
            row = idx // 3
            col = idx % 3
            with cols[row][col]:
                st.image(exercise["image"], caption=exercise["name"], use_column_width=True)
                if st.button(f"View Instructions for {exercise['name']}", key=f"{exercise['name']}_{idx}"):
                    st.write(exercise["instructions"])

    else:
        st.subheader("Exercise Recommendations")
        st.write("Engage in regular physical activity, including aerobic exercises, strength training, and flexibility exercises.")



