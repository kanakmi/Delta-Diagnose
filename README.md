# Delta Diagnose
Project that can classify Chest X-Ray Images as Covid, Viral Pneumonia and Normal

## 💡 Inspiration


## 💻 What it does


## ⚙️ How it works


## 🔨 Tech Stack
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/> <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white"/> <img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"/> <img alt="JavaScript" src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/> <img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white"/>  <img alt="Tensorflow" src="https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white"/> <img alt="Keras" src="https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white"/> <img alt="OpenCV" src="https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white"/>

## 🧠 Challenges we ran into
We first attempted to build the model from scratch but failed terribly reaching an accuracy of just about 39%. The accuracy was increased to roughly 59 percent when we utilized the ResNet50 model, but it was still below par, and the stored model size was around 300 MB, which could have caused problems when deploying the model on Heroku. Finally, we settled on the VGG16 model, which had an initial accuracy of 84 percent (later improved to 97 percent) while still keeping the size in check.

## 🏅 Accomplishments that we're proud of


## 📖 What we learned


## 🚀 What's next for StreetCode


## Installing and running

```
pip install -r requirements.txt
python manage.py runserver
```
