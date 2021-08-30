from django.shortcuts import redirect, render
from .models import Picture
from .forms import PictureForm
from .classify import classify
from cloudinary.forms import cl_init_js_callbacks
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .models import model_image
from authenticate.views import check
from .new import geturl

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    #return redirect('/Get-file')
    pictures = Picture.objects.all()
    ctx= {'pictures': pictures}
    print(request.user)
    return render(request, 'pic/index.html', ctx)

def loadPicture(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save()
            #print('https://res.cloudinary.com/dcfcqjyxs/image/upload/v1628422595/'+a.image)
            res = classify('https://res.cloudinary.com/dcfcqjyxs/image/upload/v1628422595/'+str(a.image))
            print(res)
            #c = res.split(',')[0].split(':')[1]
            c=res['class']
            d = res['class_probablity']
            #d = res.split(',')[1].split(':')[1]
            #print(res['class'],res['class_probability'])
            context ={
                'type' : c,
                'prob':d,
                'image' : 'https://res.cloudinary.com/dcfcqjyxs/image/upload/v1628422595/'+str(a.image),
            }
            return render(request, 'pic/index.html',context=context)
            
    form = PictureForm()
    ctx = { 'form': form }
    print(request.user)
    return render(request, 'pic/loadPicture.html', ctx)

@login_required
def getimg(request):
    if(check(request.user)):
        return redirect('verify')
    if request.method=='POST':
        if request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location='UI/media/'+str(request.user))
            filename = fs.save(myfile.name, myfile)
            usr = request.user
            url = geturl(str(BASE_DIR)+'/UI/media/'+str(request.user)+'/'+filename)
            res = classify(url)
            c=res['class']
            d = res['class_probablity']
            print(c,d)
            img = model_image()
            img.user = usr
            img.image = filename
            img.symptom = c
            img.accuracy = d
            img.image_url = url
            img.save()
            return redirect('results')
    return render(request,'index.html')


@login_required
def results(request):
    if(check(request.user)):
        return redirect('verify')
    datas = model_image.objects.filter(user=request.user)

    context = {
        'data':datas
    }
    return render(request,'results.html',context=context)
