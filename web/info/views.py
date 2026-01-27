from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def index(request):
    #return HttpResponse("Welcome to the Info Page")
    #template = loader.get_template("info/index.html")
    return render(request, "info/index.html")

def info(request):
    #return HttpResponse("Welcome to the Info Page")
    return render(request, "info/info.html")

