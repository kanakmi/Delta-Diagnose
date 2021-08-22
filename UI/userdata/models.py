from django.db import models
from django.contrib.auth.models import User

class CBC(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wbc = models.CharField(max_length=20, blank=True,null=True)
    rbc = models.CharField(max_length=20, blank=True,null=True)
    hgb = models.CharField(max_length=20, blank=True,null=True)
    hematocrit = models.CharField(max_length=20, blank=True,null=True)
    platlets = models.CharField(max_length=20, blank=True,null=True)
    polys = models.CharField(max_length=20, blank=True,null=True)
    lymphs = models.CharField(max_length=20, blank=True,null=True)
    monocytes = models.CharField(max_length=20, blank=True,null=True)
    eos = models.CharField(max_length=20, blank=True,null=True)
    basos = models.CharField(max_length=20, blank=True,null=True)
    lymphs = models.CharField(max_length=20, blank=True,null=True)
    data = models.DateField(auto_now_add=True)

class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='profile_pictures')
    email = models.EmailField()

    def __str__(self):
        return str(self.user)

class sendotp(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)