from django.shortcuts import render


# Create your views here.
def hello(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'header.html')


def login(request):
    return render(request, 'login.html')


def use(request):
    return render(request, 'useModel.html')

