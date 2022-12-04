from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "ManageIndex.html")


def user_list(request):
    return render(request, "user.html")


def user_list(request):
    return render(request, "user.html")


def tpl(request):
    return render(request, "tpl.html")


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    return render(request, "register.html")


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username, password)
    return render(request, "ManagementLogin.html")


def login_post(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # username = request.POST['username']
        # password = request.POST['password']
        print(username, password)
    return render(request, "ManageIndex.html")


