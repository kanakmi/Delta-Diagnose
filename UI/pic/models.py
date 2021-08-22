from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

class Picture(models.Model):
    image = CloudinaryField('image')

class model_image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField()
    symptom = models.CharField(max_length=20,null=True)
    accuracy = models.CharField(max_length=20,null=True)
    date = models.DateField(auto_now_add=True,null=True)