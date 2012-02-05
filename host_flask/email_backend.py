
from django.contrib.auth.backends import ModelBackend
from django.contrib.admin.models import User
from django.utils import timezone
   
class EmailBackend(ModelBackend):
    def authenticate(self, email):
        try:
            moo = email.lower()
            return User.objects.get(email=email.lower())
        except Exception:
            pass
        return None

