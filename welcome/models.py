# from django.db import models
#
# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# class User(AbstractUser):
#
#     ROLE_CHOICES = (
#         ('buyer', 'Buyer'),
#         ('seller', 'Seller'),
#         ('both', 'Buyer & Seller'),
#     )
#
#     phone = models.CharField(
#         max_length=20,
#         blank=True
#     )
#
#     profile_image = models.ImageField(
#         upload_to='profiles/',
#         blank=True,
#         null=True
#     )
#
#     address = models.TextField(
#         blank=True
#     )
#
#     balance = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         default=0
#     )
#
#     role = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='both'
#     )
#
#     trust_score = models.PositiveIntegerField(
#         default=100
#     )
#
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )
#
#     def __str__(self):
#         return self.username
#
# class Product(models.Model):
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='products/')
#     category = models.CharField(max_length=100)
#     is_approved = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.title