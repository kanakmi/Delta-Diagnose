## Delta Diagnose 2.0
Every hackathon, we enjoy developing new projects, but many previously built terrific projects with the potential to become something great in the future are abandoned in the early stages of development in the process. So we decided to spend this weekend working on a new version of Delta Diagnose with lots of new features and a revamped UI.

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
- Significantly reduced the saved model size from 169 MB to 28.7 MB <b>(83% reduction in Size)</b>
- To know about training procedure and model architecture, [click here](https://github.com/kanakmi/Delta-Diagnose/tree/Version-2.0/Model%20Training)

### 2. API Changes
- <b>Fixed a Bug:</b> When deployed on Heroku, the system automatically shuts down after 30 minutes of inactivity. When restarted, the app should be up and running within 60 seconds or Heroku would simply serve the request. Due to large model size, the system would not fully load and would result in an error for the first request sent after restarting the system.
- Since we reduced the model size in previous step, this bug was automatically resolved
- Used <b>FastAPI</b> instead of <b>Flask</b> 
- Significantly reduced the request serving time from 5 seconds earlier to 1.54 seconds now <b> (69.2% reduction in serving time) </b>
- To know more about API, [click here](https://github.com/kanakmi/Delta-Diagnose/tree/Version-2.0/API) or visit http://delta-diagnose-api.herokuapp.com/docs

### 3. UI changes

## ⚙️ How it works
- User needs to upload a Chest MRI Image <i>(Need some images to test on? Download them from [here](https://drive.google.com/drive/folders/1e8YPenE6jlBYznLDAu989Pv_8BFvOwup?usp=sharing))</i>
- We would process the image and return the result

## 🔨 Tech Stack
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/> <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white"/> <img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"/> <img alt="JavaScript" src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/> <img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white"/> <br> <img alt="Tensorflow" src="https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white"/> <img alt="Keras" src="https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white"/> <img alt="OpenCV" src="https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white"/> ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

## 🧠 Challenges we ran into
We first attempted to build the model from scratch but failed terribly (due to lack of training data) reaching an accuracy of just about 39%. The accuracy was increased to roughly 59 percent when we utilized the ResNet50 model, but it was still below par, and the stored model size was around 300 MB, which could have caused problems when deploying the model on Heroku. Finally, we settled on the VGG16 model, which had an initial accuracy of 84 percent (later improved to 97 percent) while still keeping the size in check. Another challange was to integrate Twilio OTP while login. We tried to use twilio but the request was not apporved for the phone number so we were not able to integrate in our project.

## 🏅 Accomplishments that we're proud of
When we started, we never thought we would be able to achieve an accuracy of 97%. We are really proud of that. <br>
Secondly our aim was to deploy this project so that anyone in the world can really use it and we are extremly happy for reaching our goal.

## 📖 What we learned
We learned how to make an API and also how to deploy the ML part seperately and the UI seperately to enhance performance of the website.

## 🚀 What's next for Delta Diagnose
We tested the model on only 66 images and those are not enough to get the real picture. We would love to test it on more images and improve the model accordingly.

## Installing and running

### Model API
Send a POST request on URL http://delta-diagnose-api.herokuapp.com/ with JSON file containing URL of image to classify as a Parameter<br>
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
```
pip install -r requirements.txt
python manage.py runserver
```

## Some glimps of the site

Home  
![home1](https://user-images.githubusercontent.com/64153988/128633936-d0f75f36-87b0-417f-a87a-5a8fd4596ccf.png)
Upload and Test
![upload1](https://user-images.githubusercontent.com/64153988/128633942-28742d18-27ac-4cab-a4ce-38e29ef06baa.png)
Result
![result1](https://user-images.githubusercontent.com/64153988/128633952-53fb306b-50fa-4ded-8674-e175542f983b.png)

