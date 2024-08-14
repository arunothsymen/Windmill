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
    
    Our mission is to optimize wind energy generation and utilization through cutting-edge IoT, machine learning, and cloud technologies. By predicting energy production and consumption, we aim to enhance energy efficiency and reliability, contributing to a more sustainable future. Join us in revolutionizing renewable energy management!
    
    ### Technologies used:
    - **Internet of Things (IoT)**
    - **Machine Learning Models**
    - **Streamlit - Frontend**
    
                
    ### How It Works
    ###### Data Collection:
    Our system collects real-time data from wind turbines, including key metrics such as energy generated, energy consumed, input voltages, and output voltages, along with environmental factors.
    
    ###### Analyze Data:
    Navigate to the Input Prediction or Output Prediction page and select a date for prediction. The system will process the data using advanced algorithms to predict future energy generation and utilization.
    
    ###### Predictive Analysis:
    Our machine learning models analyze historical data to forecast wind energy production and consumption on specific dates, helping you make informed decisions about energy management.

    ###### Results and Recommendations:
    View detailed predictions and actionable insights that allow you to optimize wind energy usage, reduce waste, and ensure a reliable energy supply.

    ### Components and Flow
    ##### Components Used:
    - **Windmill**
    - **2 Channel 5V Relay Module**
    - **Two-way USB Type-C Cable**
    - **TP4056**
    - **Resistors 7 kΩ ±5% (J)**
    - **Lithium-Ion Battery - 4000mAh*2 (8000mAh)**
    - **Battery Holders**
    - **Connecting Wires**
    - **Multiplexer**
    - **Voltage Sensor**
    - **ESP 8266**
    - **Type B Data Sharing Cable**
    - **12cm×18cm PCB Board (3 nos)**
    """)
    image_path = "Cheat-Sheet.jpg"
    st.image(image_path,use_column_width=True)
    st.markdown("""                    
    ### Why Choose Us?
    - **Advanced Technology:** Our platform leverages the latest in IoT, machine learning, and cloud computing to deliver precise and reliable predictions.
    - **User-Friendly:** Simple and intuitive interface for seamless user experience.
    - **Fast and Efficient:** Receive results in seconds, allowing for quick decision-making.

    ### Get Started
    Click on the **Input Prediction** or **Output Prediction** page in the sidebar and select a date for prediction, and experience the power of our IoT-Driven Wind Energy Solutions!

    ### About Us
    Learn more about the creator and the inspiration behind this innovative project on the **About** page.
    """)

#About Project
elif(app_mode=="About"):
    st.header("About Creator")
    col1, col2, col3 = st.columns(3)
    with col1:
        image_path = "Final_Pic.JPG"
        st.image(image_path,width=200)
        st.markdown("""
                #### Dhillipkumar M
                Christ University, Bangalore
                #### Contact Details
                Phone Number : 7639902361\n
                Email : dhillipkumar2001@gmail.com\n
                Linkedin : [Dhillipkumar](www.linkedin.com/in/dhillipkumar-m-893854193)\n
                GitHub : [Dhillipkumar](https://github.com/Dhillipkumar)

                """)
    with col2:
        image_path = "SYMEN.jpg" 
        st.image(image_path, width=200)
        st.markdown("""
                #### Arunoth Symen A
                Christ University, Bangalore
                #### Contact Details
                - **Phone:** 9150418081\n
                - **Email:** arunothsymen1@gmail.com\n
                - **LinkedIn:** [Arunoth Symen](https://www.linkedin.com/in/arunothsymen)\n
                - **GitHub:** [Arunoth Symen](https://github.com/arunothsymen)
                """)

    with col3:
        image_path = "2347148.JPG"  
        st.image(image_path, width=200)
        st.markdown("""
                #### P Santhosh Kumar
                Christ University, Bangalore
                #### Contact Details
                - **Phone:** 6379314514\n
                - **Email:** santhoshkumar150822@gmail.com\n
                - **LinkedIn:** [Santhosh Kumar](https://www.linkedin.com/in/santhosh-kumar-150822-p)\n
                - **GitHub:** [Santhosh Kumar](https://github.com/SanthoshKumar150822)
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
    target_date = st.date_input("Select a date to predict power generation", datetime(2024, 8, 16))

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
    target_date = st.date_input("Select a date to predict power utilization", datetime(2024, 8, 16))

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