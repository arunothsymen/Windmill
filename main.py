import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import pickle
from datetime import datetime

#Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_plant_disease_model.keras")
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) #convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions) #return index of max element

#Sidebar
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page",["Home","About","Input Prediction","Output Prediction"])

#Main Page
if(app_mode=="Home"):
    st.header("IoT-Driven Wind Energy Solutions")
    image_path = "wind.jpg"
    st.image(image_path,use_column_width=True)
    st.markdown("""
    Welcome to the IoT-Driven Wind Energy Solutions Platform! 🌬️⚡
    
    Our mission is to optimize wind energy generation and utilization through cutting-edge IoT and machine learning technologies. By predicting energy production and consumption, we help ensure a more efficient and reliable energy supply. Join us in revolutionizing renewable energy management!
    
    ### How It Works
    ###### How It Works
    Our system collects real-time data from wind turbines, including energy generation, consumption patterns, and environmental factors.
    
    ###### How It Works
    Our system collects real-time data from wind turbines, including energy generation, consumption patterns, and environmental factors.

    ###### How It Works
    Our system collects real-time data from wind turbines, including energy generation, consumption patterns, and environmental factors.

    ###### How It Works
    Our system collects real-time data from wind turbines, including energy generation, consumption patterns, and environmental factors.
            
                
    ### Why Choose Us?
    - **Accuracy:** Our system utilizes state-of-the-art machine learning techniques for accurate disease detection.
    - **User-Friendly:** Simple and intuitive interface for seamless user experience.
    - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

    ### Get Started
    Click on the **Disease Recognition** page in the sidebar to upload an image and experience the power of our Plant Disease Recognition System!

    ### About Us
    Learn more about the creator, on the **About** page.
    """)

#About Project
elif(app_mode=="About"):
    st.header("About Creator")
    image_path = "Final_Pic.JPG"
    st.image(image_path,width=250)
    st.markdown("""
                #### Dhillipkumar M
                Christ University, Bangalore
                #### Contact Details
                Phone Number : 7639902361\n
                Email : dhillipkumar2001@gmail.com\n
                Linkedin : www.linkedin.com/in/dhillipkumar-m-893854193\n
                GitHub : https://github.com/Dhillipkumar

                """)

#Prediction Page
elif(app_mode=="Input Prediction"):
    def load_model():
        with open('arima_model.pkl', 'rb') as file:
            model_fit = pickle.load(file)
        return model_fit

    model_fit = load_model()

# Load the data and prepare for prediction
    data = pd.read_csv('windmill_data.csv')
    data['input_time'] = pd.to_datetime(data['input_time'])
    daily_generation = data.resample('D', on='input_time').sum()['input_voltage']
    daily_generation = daily_generation.asfreq('D').fillna(0)

# Streamlit app
    st.title("Windmill Power Generation Prediction")

# User input for target date
    target_date = st.date_input("Select a date to predict power generation", datetime(2024, 1, 31))

# Convert target date to a timestamp and find the forecast index
    forecast_date = (pd.Timestamp(target_date) - daily_generation.index[-1]).days
    forecast_steps = 30
    forecast = model_fit.forecast(steps=forecast_steps)

# Predict and display the result
    if 0 <= forecast_date < forecast_steps:
        predicted_value = forecast[forecast_date]
        st.write(f"Predicted power generation on {target_date}: {predicted_value:.4f} V")
    else:
        st.write("The selected date is out of the forecast range. Please select a closer date.")

elif(app_mode=="Output Prediction"):
    def load_model():
        with open('arima_model_output.pkl', 'rb') as file:
            model_fit = pickle.load(file)
        return model_fit

    model_fit = load_model()

# Load the data and prepare for prediction
    data = pd.read_csv('windmill_data.csv')
    data['output_time'] = pd.to_datetime(data['output_time'])
    daily_generation = data.resample('D', on='output_time').sum()['output_voltage']
    daily_generation = daily_generation.asfreq('D').fillna(0)

# Streamlit app
    st.title("Windmill Power Utilization Prediction")

# User input for target date
    target_date = st.date_input("Select a date to predict power utilization", datetime(2024, 1, 31))

# Convert target date to a timestamp and find the forecast index
    forecast_date = (pd.Timestamp(target_date) - daily_generation.index[-1]).days
    forecast_steps = 30
    forecast = model_fit.forecast(steps=forecast_steps)

# Predict and display the result
    if 0 <= forecast_date < forecast_steps:
        predicted_value = forecast[forecast_date]
        st.write(f"Predicted power utilization on {target_date}: {predicted_value:.4f} V")
    else:
        st.write("The selected date is out of the forecast range. Please select a closer date.")