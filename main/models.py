from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, date, timedelta

# Create your models here.
#datetime to string
def time_string(t):
    return timezone.localtime(t).strftime("%I:%M%p").lstrip("0")

def day_string(t):
    return timezone.localtime(t).strftime("%b %d")

def date_string(t):
    return timezone.localtime(t).strftime("%m/%d/%y")

def time_ago(t):
    delta = timezone.now()-t
    if delta < timedelta(seconds=20):
        return "a few seconds ago"
    if delta < timedelta(seconds=50):
        return "thirty seconds ago"
    if delta < timedelta(minutes=1, seconds=30):
        return "one minute ago"
    if delta < timedelta(minutes=60):
        return str(delta.seconds/60) + " minutes ago"
    if delta < timedelta(minutes=100):
        return "about an hour ago"
    if delta < timedelta(hours=24):
        return str(delta.seconds/3600) + " hours ago"
    if delta < timedelta(days=1):
        return "at " + time_string(t)
    else:
        return "on " + day_string(t)



class Site(models.Model):
    owner = models.ForeignKey(User)
    dirname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    time_created = models.DateTimeField(auto_now_add=True)
    def get_url(self, request):
        return "http://" + request.get_host() + "/sites/" +  self.owner.username + "/" + self.name + "/"
    def get_time(self):
        return date_string(self.last_updated) + " at " + time_string(self.last_updated)
