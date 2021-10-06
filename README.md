## Delta Diagnose 2.1

## 🆕 Updates
- Used <b>Quantization Aware Training</b> to reduce the Trained Model size from 30.1 MB to 2.41 MB <b>(92% reduction in Size)</b>
- Further reduced the request serving time from 1.54 seconds earlier to less than 1 second now <b> (50% reduction in serving time) </b>
- Added a new way to interact with the API


https://user-images.githubusercontent.com/54859521/136175830-5cbb4bb1-3c20-4d79-bc6b-c52b15ce9a11.mp4



## Delta Diagnose 2.0
Every hackathon, we enjoy developing new projects, but many previously built terrific projects with the potential to become something great in the future are abandoned in the early stages of development in the process. So we decided to spend this weekend working on a new version of Delta Diagnose with lots of new features and a revamped UI. You can know more about the previous version from [here](https://devpost.com/software/delta-diagnose).

## 💡 Inspiration
The Delta variant of COVID-19 arrived in India in March 2021. It led to the deaths of 270,000 individuals in three months, more than twice the number we saw in the entire year of 2020. <br> The Delta strain has a higher affinity for lung tissues than other strains, making it more lethal. <br>
The same mutation has now been discovered in other parts of the world. We wanted to aid the people in these countries, thus we created Delta Diagnose. <br>
Viral Pneumonia, a condition with identical symptoms, has made identifying COVID patients even more challenging.

## 💻 What it does
Delta Diagnose aims to analyze Chest MRI Images and classify them as COVID-19, Viral Pneumonia, and Normal. It can not only assist doctors but can also be directly used by the patients to self-diagnose (although we suggest confirming the results with doctors).

## 🆕 Updates

### 1. Model Changes
- Added 1704 new images to the training data <b>(678% increase in training data)</b>
- Added 119 new images to the test data <b>(180% increase in test data)</b>
- Compared to the last time, <b>constructed the model from scratch</b> (was using Transfer Learning previously)
- Increased the accuracy from 97% to 99%
- Significantly reduced the saved model size from 169 MB to 30.1 MB <b>(83% reduction in Size)</b>
- To know about training procedure and model architecture, [click here](https://github.com/kanakmi/Delta-Diagnose/tree/Version-2.0/Model%20Training)

### 2. API Changes
- <b>Fixed a Bug:</b> When deployed on Heroku, the system automatically shuts down after 30 minutes of inactivity. When restarted, the app should be up and running within 60 seconds or Heroku would simply serve the request. Due to large model size, the system would not fully load and would result in an error for the first request sent after restarting the system.
- Since we reduced the model size in previous step, this bug was automatically resolved
- Used <b>FastAPI</b> instead of <b>Flask</b> 
- Significantly reduced the request serving time from 5 seconds earlier to 1.54 seconds now <b> (69.2% reduction in serving time) </b>
- To know more about API, [click here](https://github.com/kanakmi/Delta-Diagnose/tree/Version-2.0/API) or visit http://delta-diagnose-api.herokuapp.com/docs

### 3. UI changes
- Revamped the complete UI
- Added Login and Signup Page
- Integrated Twillio for OTP verification
- Elevated the User Experience

## ⚙️ How it works
- User needs to Login/Signup
- User needs to upload a Chest MRI Image <i>(Need some images to test on? Download them from [here](https://drive.google.com/drive/folders/1e8YPenE6jlBYznLDAu989Pv_8BFvOwup?usp=sharing))</i>
- We would process the image and return the result

## 🔨 Tech Stack
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/> <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white"/> <img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"/> <img alt="JavaScript" src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/> <img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white"/> <br> <img alt="Tensorflow" src="https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white"/> <img alt="Keras" src="https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white"/> <img alt="OpenCV" src="https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white"/> ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

## 🧠 Challenges we ran into
- The biggest challenge was to manage the size of the API. If the size increases by 300 MB, Heroku takes a lot of time to boot up the virtual machine which was not an ideal scenario. In the previous version, the size was 493 MB which was reduced to 318 MB after retraining the model and switching to FastAPI. At this moment we were drained of energy and couldn't think of more ways to reduce that extra 18 MB. Then the last thing we decided to try was to find a version of big libraries such as Tensorflow and OpenCV which is as small in size as possible and as recent as possible. Finally we were able to pack it up in a size of 283 MB with all the required libraries and everything.
- Another thing that we tried was Quantization Aware Training but doing that reduced the accuracy of our model to 65% so it was not really something we could put into production.

## 🏅 Accomplishments that we're proud of
This is actually the first time we have achieved an accuracy of 99% on model that we trained from scratch which is really a stat we would love to boast about.

## 📖 What we learned
- We learned how to use FastAPI and thanks to awesome documentation, that process was seamless.
- We learned how to reduce slug size of your project to increase performance.
- We learned about Quantization Aware training to reduce the size of the model and make it accessible for small devices.
- We also leared how to use Twillio for OTP Authentication

## 🚀 What's next for Delta Diagnose
All the stats we are boasting about are limited to the small amount of data we have. We would love to see how it performs on the real world data by taking this project to a specialized doctor.

## Installing and running

### Model API
Send a POST request on URL http://delta-diagnose-api.herokuapp.com/ with JSON file containing URL of image to classify as a Parameter<br>

<p align="center">
  

https://user-images.githubusercontent.com/54859521/131256477-3bf2f2f4-9512-4e3f-b922-611e2aa0474b.mp4


</p>

Sample JSON File
```
{
  "url" : "https://i.ibb.co/FBSztPS/0120.jpg"
}
```
Sample Response
```
{
  "class":"viral_pneumonia",
  "class_probability":99.93
}
```

### GUI Version
Jump over to the UI folder and run
```
pip install -r requirements.txt
python manage.py runserver
```
