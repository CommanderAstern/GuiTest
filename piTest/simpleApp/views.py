from django.shortcuts import render
from django.http import HttpResponse
import RPi.GPIO as GPIO

# Create your views here.

def index(request):
    if 'counter' in request.session:
        request.session['counter'] += 1
        val = request.session['counter']
        GPIO.output(7,True) if val%2 else GPIO.output(7,False) 
    else:
        request.session['counter'] = 1
        GPIO.output(7,True)

    return render(request, 'simpleApp/index.html', {'counter': request.session['counter']})
    # if request.method == "POST":
    #   try:
    #      request.session['count'] +=1
    #   except:
    #      request.session['count'] = 0
    # else :
    #   request.session['count'] = 0
    #   return render(request, 'simpleApp/index.html')