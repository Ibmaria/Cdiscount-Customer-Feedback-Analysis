from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd 
# Create your views here.


@login_required(login_url='login')
def home(request):
	return render(request,'model/index.html')

def topic_huit(request):
	return render(request, 'model/lda8.html')
def topic_quatre(request):
	return render(request, 'model/lda4.html')