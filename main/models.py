from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Site(models.Model):
    owner = models.ForeignKey(User)
    dirname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)
    def get_url(self, request):
        name = "http://" + request.get_host() + owner.username + "/" + name + ".wsgi"
