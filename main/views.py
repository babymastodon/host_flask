from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.core import serializers
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.template import loader, Context
from datetime import datetime, date
from django import forms
import random, string, cStringIO, zipfile, tempfile, re, os

#import models and forms here
from main.models import *
from main.forms import *

def login_required(f):
    def login_function(request, *args, **kwargs):
        if not request.user.is_authenticated():
            email = request.META.get('SSL_CLIENT_S_DN_Email')
            if not email:
                return redirect("https://"+ request.get_host() + request.get_full_path())
            user = authenticate(email=email)
            if user:
                login(request, user)
            else:
                return redirect("https://"+ request.get_host() + reverse('main.views.newaccount'))
        return f(request, *args, **kwargs)
    return login_function

def newaccount(request):
    rc={}
    if request.method=="POST":
        email = request.META['SSL_CLIENT_S_DN_Email'].lower()
        username = email.split('@')[0]
        name = request.META['SSL_CLIENT_S_DN_CN'].split()
        firstname = name[0]
        lastname = name[-1]
        u = User.objects.filter(email=email)
        if not u:
            user = User(email=email, username=username, first_name = firstname, last_name = lastname)
            user.save()
        user = authenticate(email=email)
        login(request, user)
        return redirect(reverse('main.views.admin'))
    return render(request, 'main/login_view.html', rc)

def home(request):
    rc={}
    sites = Site.objects.all().order_by('-last_updated')
    rc['sites'] = ({'site':x, 'url':x.get_url(request)} for x in sites)
    return render(request, 'main/home.html', rc)

@login_required
def admin(request):
    rc={}
    sites = Site.objects.filter(owner=request.user.pk).order_by('-last_updated')
    rc['sites'] = ({'site':x, 'url':x.get_url(request)} for x in sites)
    return render(request, 'main/admin.html', rc)

def getzip(f):
    try:
        z = zipfile.ZipFile(cStringIO.StringIO(f.read()))
    except:
        return {'success':False, 'msg':'Please upload a valid zip file'}
    bad = z.testzip()
    if bad:
        return {'success':False, 'msg':'Bad file: ' + bad}
    names = z.namelist()
    for n in names:
        if re.match(r'^/', n):
            return {'success':False, 'msg':'All file paths must be relative'}
        if re.match(r'\.\.', n):
            return {'success':False, 'msg':'You are not allowed to extract files to the parent directory'}
    d = tempfile.mkdtemp()
    z.extractall(d)
    for (dirpath, dirname, filenames) in os.walk(d):
        if "app.py" in filenames:
            if (dirpath!=d):
                newd = tempfile.mkdtemp()
                os.system('cp -R ' + dirpath + "/* " + newd)
                os.system('rm -rf ' + dirpath)
                dirpath=newd
            return {'success':True, 'd':dirpath}
    os.system('rm -rf ' + d)
    return {'success':False, 'msg':"Archive must contain a file named app.py with the entry point to your web application"}

def proj_dir():
    return os.path.normpath(os.path.join(os.path.dirname(__file__),'..'))

def rmsite(dirname):
    os.system('rm -rf ' + os.path.join(os.path.dirname(__file__),'..','sites', dirname))

def move(d,dirname):
    f = os.path.join(proj_dir(),'sites', dirname)
    os.system('rm -rf ' + f)
    os.system('mv ' + d + ' ' + f)
    os.system('chmod a+rw -R ' + f)
    os.system('chmod a+x ' + f)

def mkwsgi(request, name, dirname):
    wsgi_dir = os.path.join(proj_dir(),'wsgi',request.user.username)
    try:
        os.mkdir(wsgi_dir)
    except OSError:
        pass
    t = loader.get_template('wsgi/template.py')
    w = open(os.path.join(wsgi_dir, name+'.py'), 'w')
    w.write(t.render(Context({'name':dirname})))
    w.close()

def rmwsgi(request, name):
    os.system('rm -f ' + os.path.join(os.path.dirname(__file__),'..','wsgi',request.user.username, name+'.py'))

@login_required
def newsite(request):
    rc={}
    form = UploadForm()
    if request.method=="POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            if re.match(r'.*[^\w].*', name):
                rc['error'] = "Name Can only contain alpha-numeric characters"
            else:
                if Site.objects.filter(name=name, owner=request.user).exists():
                    rc['error'] = "You alreay have a site by that name"
                else:
                    tmp = getzip(form.cleaned_data['zip_file'])
                    if not tmp['success']:
                        rc['error'] = tmp['msg']
                    else:
                        d=tmp['d']
                        h = "%032x" % random.getrandbits(128)
                        dirname = request.user.username+h
                        move(d,dirname)

                        mkwsgi(request,name, dirname)
                        s = Site(owner=request.user, dirname=dirname, name=name)
                        s.save()

                        return redirect(reverse('main.views.admin'))
    rc['form']=form
    return render(request, 'main/newsite.html', rc)

@login_required
def updatesite(request, pk):
    rc={}
    site = get_object_or_404(Site, pk=pk)
    form = UploadFormOptional({'name':site.name})
    if request.method=="POST":
        form = UploadFormOptional(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            if re.match(r'.*[^\w].*', name):
                rc['error'] = "Name Can only contain alpha-numeric characters"
            else:
                if Site.objects.filter(name=name, owner=request.user).exclude(pk=pk).exists():
                    rc['error'] = "You alreay have a site by that name"
                else:
                    if name != site.name:
                        rmwsgi(request, site.name)
                        site.name = name
                    if form.cleaned_data['zip_file']:
                        tmp = getzip(form.cleaned_data['zip_file'])
                        if not tmp['success']:
                            rc['error'] = tmp['msg']
                        else:
                            d=tmp['d']
                            move(d,site.dirname)
                    if 'error' not in rc:
                        site.save()
                        mkwsgi(request,site.name, site.dirname)
                        return redirect(reverse('main.views.admin'))
    rc['form'] = form
    return render(request, 'main/updatesite.html', rc)

@login_required
def deletesite(request, pk):
    rc={}
    site = get_object_or_404(Site, pk=pk)
    if not site.owner == request.user:
        return redirect(reverse('main.views.home'))
    if request.method=="POST":
        rmsite(site.dirname)
        rmwsgi(request, site.name)
        site.delete()
        return redirect(reverse('main.views.admin'))
    rc['site'] = site
    rc['url'] = site.get_url(request)
    return render(request, 'main/deletesite.html', rc)

