from django.db import models

# Create your models here.
class V1Model(models.Model):
    jisilu_cookie = models.CharField(max_length=1000)