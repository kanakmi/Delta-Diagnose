from django.urls import path
from .views import signin,signup,signout,verify

urlpatterns = [
    path('login/',signin),
    path('signup/',signup),
    path('signout/', signout),
    path('verify',verify,name='verify'),
]
