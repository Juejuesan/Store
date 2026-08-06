from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from user.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=100)

    SIZE_TYPE_CHOICES = [
        ('clothing', 'Clothing'),
        ('pants', 'Pants/Jeans'),
        ('shoe', 'Shoe'),
        ('ring', 'Ring'),
        ('baby', 'Baby/Kids'),
        ('none', 'No Sizes'),
    ]

    size_type = models.CharField(max_length=20, choices=SIZE_TYPE_CHOICES, default='none')
    size_label = models.CharField(max_length=100, blank=True, null=True)
    custom_sizes = models.TextField(blank=True, null=True)

    def get_sizes(self):
        if self.custom_sizes:
            return [size.strip() for size in self.custom_sizes.split(',')]

        default_sizes = {
            'clothing': ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'],
            'pants': ['28', '29', '30', '31', '32', '33', '34', '36', '38', '40'],
            'shoe': ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45'],
            'ring': ['5', '6', '7', '8', '9', '10', '11', '12'],
            'baby': ['0-3m', '3-6m', '6-12m', '12-18m', '18-24m', '2-3y', '3-4y'],
        }
        return default_sizes.get(self.size_type, [])

    def __str__(self):
        return self.name


class Post(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('used', 'Second Hand'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.user.username} - {self.category.name}"


class Item(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    has_sizes = models.BooleanField(default=False)
    simple_quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.post:
            category_supports_sizes = self.post.category.size_type != 'none'
            is_new_item = self.post.condition == 'new'
            self.has_sizes = category_supports_sizes and is_new_item
        else:
            self.has_sizes = False
        super().save(*args, **kwargs)

    @property
    def total_quantity(self):
        if self.has_sizes:
            return sum(variant.quantity for variant in self.size_variants.all())
        return self.simple_quantity

    @property
    def available_sizes(self):
        if self.has_sizes:
            return self.size_variants.filter(quantity__gt=0)
        return SizeVariant.objects.none()

    @property
    def is_in_stock(self):
        if self.has_sizes:
            return self.total_quantity > 0
        return self.simple_quantity > 0


class SizeVariant(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='size_variants')
    size = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # ADD THIS

    class Meta:
        unique_together = ['item', 'size']
        ordering = ['size']

    def __str__(self):
        return f"{self.item.name} - Size {self.size} (Qty: {self.quantity}, Price: {self.price})"


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for {self.item.name}"