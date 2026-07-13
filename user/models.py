from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30,unique=True)
    profile = models.ImageField(upload_to='images/')
    phNumber = models.CharField(max_length=11,unique=True)
    email = models.EmailField(max_length=30,unique=True)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20)
    nrc= models.CharField(max_length=40,unique=True)
    address = models.TextField(max_length=100)
    gender = models.CharField(max_length=10)
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


