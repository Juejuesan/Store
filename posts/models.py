from django.core.validators import MinValueValidator
from django.db import models

from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    TYPE_CHOICES = [
        ('brand', 'Brand'),
        ('second', 'Second Hand'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,on_delete=models.CASCADE,related_name='posts'
    )

    price = models.IntegerField(default=0,validators= [MinValueValidator(1)])
    type = models.CharField( max_length=10, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(  max_length=20, choices=STATUS_CHOICES,default='pending')
    description = models.TextField()
    quantity = models.IntegerField(default=1,validators= [MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category.name


class PostImage(models.Model):
        post = models.ForeignKey(
            Post,
            on_delete=models.CASCADE,
            related_name="images"
        )

        image = models.ImageField(
            upload_to='post_images/'
        )