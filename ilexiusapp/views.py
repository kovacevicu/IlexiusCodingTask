from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# Create your views here.
def login_as(req, uid):
    user = User.objects.get(pk=uid)
    login(req, user)
    return redirect("/admin/")
    