from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def info(request):
    #return HttpResponse("Welcome to the Info Page")
    template = loader.get_template("info/index.html")
    return render(request, "info/index.html")
