from django.shortcuts import redirect, render
from .models import Picture
from .forms import PictureForm
from .classify import classify
from cloudinary.forms import cl_init_js_callbacks

# Create your views here.
def index(request):
    pictures = Picture.objects.all()
    ctx= {'pictures': pictures}
    return render(request, 'pic/index.html', ctx)

def loadPicture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save()
            #print('https://res.cloudinary.com/dcfcqjyxs/image/upload/v1628422595/'+a.image)
            res = classify('https://res.cloudinary.com/dcfcqjyxs/image/upload/v1628422595/'+str(a.image))
            print(res)
            #print(res['class'],res['class_probability'])
            context ={
                'type' : res,
                'image' : 'https://res.cloudinary.com/dcfcqjyxs/image/upload/v1628422595/'+str(a.image),
            }
            return render(request, 'pic/index.html',context=context)
            
    form = PictureForm()
    ctx = { 'form': form }
    return render(request, 'pic/loadPicture.html', ctx)