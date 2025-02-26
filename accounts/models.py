from datetime import timedelta
from typing import override
from django.db import models
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.utils import timezone

def time_default():
    return timezone.now() + timedelta(minutes=5)


class Code(models.Model):
    code_number = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_user')
    expire_date = models.DateTimeField(default=time_default)

    @override
    def save(self, *args, **kwargs):
        Code.objects.filter(user=self.user).delete()
        super().save(*args, **kwargs)


    @override
    def __str__(self):
        return f"Code: {self.code_number} for {self.user.email} (Expires: {self.expire_date})"
