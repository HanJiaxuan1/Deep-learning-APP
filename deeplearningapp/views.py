from django.shortcuts import render


# Create your views here.
def hello(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'header.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def use(request):
    return render(request, 'useModel.html')


def about(request):
    return render(request, 'about.html')


def profile(request):
    return render(request, 'profile.html')
