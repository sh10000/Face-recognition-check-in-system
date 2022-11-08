from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return  HttpResponse("欢迎使用")
def user_list(request):
      return  render(request,"user.html")
def user_list(request):
      return  render(request,"user.html")
def tpl(request):
      return  render(request,"tpl.html")