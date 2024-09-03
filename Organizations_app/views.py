from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def sign_up(request):
    return render(request,"sign_up.html")