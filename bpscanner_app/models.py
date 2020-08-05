from django.db import models

class Search(models.Model):
    city = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

class Ad(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    desc = models.CharField(max_length=1000)
    timestamp = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    checked = models.BooleanField(default=False)
    checked_photos = models.BooleanField(default=False, null=True)
    bad = models.BooleanField(default=False)

class Images(models.Model):
    images = models.CharField(max_length=1000)

class Person(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=None, null=True)
    email = models.CharField(max_length=1000, default=None, null=True)
    phone = models.CharField(max_length=1000, default=None, null=True)
    age = models.CharField(max_length=1000, default=None, null=True)
    location = models.CharField(max_length=1000,  default=None, null=True)
    images = models.ForeignKey(Images, on_delete=models.CASCADE, default=None, null=True)

