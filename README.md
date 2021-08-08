## Delta Diagnose

## 💡 Inspiration
The Delta variant of COVID-19 arrived in India in March 2021. It led to the deaths of 270,000 individuals in three months, more than twice the number we saw in the entire year of 2020. <br> The Delta strain has a higher affinity for lung tissues than other strains, making it more lethal. <br>
The same mutation has now been discovered in other parts of the world. We wanted to aid the people in these countries, thus we created Delta Diagnose. <br>
Viral Pneumonia, a condition with identical symptoms, has made identifying COVID patients even more challenging.

## 💻 What it does
Delta Diagnose aims to classify Chest MRI Images as COVID-19, Viral Pneumonia, and Normal.  It can not only assist doctors but can also be directly used by the patients to self-diagnose (although we suggest confirming the results with doctors).

## 👷‍♂️ How we Built it
Data related to the healthcare industry is not openly accessible. We were fortunate enough to find a relevant dataset on Kaggle [(Link)](https://www.kaggle.com/pranavraikokte/covid19-image-dataset). <br>
The Dataset consists of 251 Chest MRI Train images (111 - COVID, 70 - Viral Pneumonia, 70 - Normal) and 66 Test Images (26 - COVID, 20 - Viral Pneumonia, 20 - Normal).
<p align = 'center'>
  <img alt="Sample" height=40% src="https://i.ibb.co/Hrp0YyL/Screenshot-2021-08-08-105409.png" width="40%"/>
</p>
Then we did some image augmentation (Horizontal Flip) and obtained 502 total samples out of which 15% (76 samples) formed the Validation Set and rest (426 samples) formed the training set.<br>
Leveraging the power of Transfer Learning, we used <b>VGG16 model</b> pre-trained on imagenet dataset as our basemodel with it's weights freezed. We then flattened the output from the basemodel and passed it to a Dense Layer consisting of 3 neurons (1 for each class). Finally, we saved the model with least Validation Loss for future predictions.

## ⚙️ How it works


## 🔨 Tech Stack
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/> <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white"/> <img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"/> <img alt="JavaScript" src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/> <img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white"/> <br> <img alt="Tensorflow" src="https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white"/> <img alt="Keras" src="https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white"/> <img alt="OpenCV" src="https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white"/>

## 🧠 Challenges we ran into
We first attempted to build the model from scratch but failed terribly (due to lack of training data) reaching an accuracy of just about 39%. The accuracy was increased to roughly 59 percent when we utilized the ResNet50 model, but it was still below par, and the stored model size was around 300 MB, which could have caused problems when deploying the model on Heroku. Finally, we settled on the VGG16 model, which had an initial accuracy of 84 percent (later improved to 97 percent) while still keeping the size in check.

## 🏅 Accomplishments that we're proud of


## 📖 What we learned


## 🚀 What's next for Delta Diagnose


## Installing and running

```
pip install -r requirements.txt
python manage.py runserver
```
