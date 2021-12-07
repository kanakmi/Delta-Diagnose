import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# global variable that will be used to store the interpreter
covid_interpreter = None
labels = {0: "COVID-19", 1: "Viral Pneumonia", 2: "Normal"}

def input_covid_classifier():
    # function to read the model from disk
    global covid_interpreter
    covid_interpreter = tf.lite.Interpreter(model_path=os.path.join(os.getcwd(), 'Streamlit_UI/covid_classifier.tflite'))
    covid_interpreter.allocate_tensors()

def predict(image):

    input_details = covid_interpreter.get_input_details()
    output_details = covid_interpreter.get_output_details()

    input_shape = input_details[0]['shape']
    output_shape = output_details[0]['shape']

    image = image.convert("RGB")
    image = image.resize((256, 256))
    image = np.array(image)

    img = image.astype('Float32')
    img = img/255
    img = img.reshape((1, 256, 256, 3))
    covid_interpreter.set_tensor(input_details[0]['index'], img)
    covid_interpreter.invoke()
    predictions = covid_interpreter.get_tensor(output_details[0]['index'])
    pred = np.argmax(predictions[0])
    result = {
        'class': labels[pred],
        'class_probablity': np.round(predictions[0][pred]*100,2)
    }

    return result

if __name__ == '__main__':
    st.sidebar.header("Delta Diagnose")
    st.sidebar.markdown("Delta Diagnose uses a Convolutional Neural Network to detect COVID-19 and Viral Pneumonia in Chest X-Ray Images with an accuracy of 99%.")
    st.sidebar.image('https://github.com/kanakmi/Delta-Diagnose/blob/Version-2.2/Streamlit_UI/sidebar.gif?raw=true', use_column_width=True)
    st.sidebar.subheader("Upload an image to get a diagnosis")
    st.sidebar.markdown("[Project Repository](https://github.com/kanakmi/Delta-Diagnose)")
    st.sidebar.markdown("Need some images to test on?")
    st.sidebar.markdown("Download them from [here](https://drive.google.com/drive/folders/1e8YPenE6jlBYznLDAu989Pv_8BFvOwup?usp=sharing)")
    st.image('https://github.com/kanakmi/Delta-Diagnose/blob/Version-2.2/Streamlit_UI/Header.gif?raw=true', use_column_width=True)
    file_uploaded = st.file_uploader("Choose the Image File", type=['jpg', 'jpeg', 'png'])
    
    if file_uploaded is not None:
        if covid_interpreter is None:
            input_covid_classifier()
        image = Image.open(file_uploaded)
        result = predict(image)
        col1, col2 = st.columns(2)
        col2.image(image, caption="The image is classified as "+result['class'], width=300)
        col1.header("Classification Result")
        col1.write("The image is classified as "+result['class'])
        col1.write("The class probability is "+str(result['class_probablity'])+"%")
        