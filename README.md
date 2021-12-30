# Author Ibrahim Koné
# Cdiscount-Customer-Reviews-Analysis

Customers leave tons of reviews, advice, complaints in a business portal.Reading and understanding all these take a lot of manual effort, time, and costs.This app can summarise different relevant metrics for our business like most recent reviews, Overall rating, distribution of sentiments, trending keywords,Lda Modeling and so on.

<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/Ibmaria/Cdiscount-Customer-Feedback-Analysis.git
$ cd Cdiscount-Customer-Feedback-Analysis
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Storage
$ pip3 install -r requirements.txt or pip install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.

<br />

## Inscription SnapShot
![App screenshot](https://github.com/Ibmaria/Cdiscount-Customer-Feedback-Analysis/blob/master/screenshot/inscription.PNG)

## Login SnapShot
![App screenshot](https://github.com/Ibmaria/Cdiscount-Customer-Feedback-Analysis/blob/master/screenshot/login.PNG)

## Download Video App Here
![App Video](https://github.com/Ibmaria/Cdiscount-Customer-Feedback-Analysis/blob/master/videoapp.gif)


## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- autentification/                              
   |    |-- settings.py                    
   |    |-- static/
   |    |
   |    |-- templates/                     
   |         *.html 
   |                       
   |    |--fichierspython/
            *.py
   |                             
   |
   |-- chat/                     
   |    |-- urls.py                          
   |    |-- forms.py                        
   |
   |-- kernel/                                
   |    |-- views.py                       
   |    |-- urls.py                          
   |
   |--model/
   |    |--dashapps
        |--static
        |--templates
        |--fichierspython
            *.py
   |--data/
        |*.csv
        |*.ipynb
   |--Projet
   |    |--input
        |--models_trained
        |--notebooks
        |--src
   
   |-- requirements.txt                    # Development modules - SQLite  storage                               
   |-- manage.py                           # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />





