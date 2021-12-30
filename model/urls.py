from django.urls import path
from . import views
import os
from model.dashapps import app1,app2,app3,app4,app5,app6,app7
urlpatterns=[

path('', views.home, name='home'),
path('topicmodeling8/', views.topic_huit, name='topic8'),
path('topicmodeling4/', views.topic_quatre, name='topic4'),

]