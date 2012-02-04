from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.core import serializers
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, date
from django import forms

#import models and forms here
from main.models import *
from main.forms import *

def login_required(f):
    def login_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            email = request.META['SSL_CLIENT_S_DN_Email']
            user = authenticate(email=email)
            if user:
                login(request, user)
            else:
                return redirect('main.views.newaccount')
        return f(request, *args, **kwargs)
    return login_function

def newaccount(request):
    rc={}
    return render(request, 'main/login_view.html', rc)

def home(request):
    return render(request, 'main/home.html')

def admin(request):
    rc={}
    return render(request, 'main/admin.html', rc)

def newsite(request):
    rc={}
    return render(request, 'main/newsite.html', rc)

def updatesite(request, pk):
    rc={}
    return render(request, 'main/updatesite.html', rc)

def deletesite(request, pk):
    rc={}
    return render(request, 'main/deletesite.html', rc)

