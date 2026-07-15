from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Post(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"