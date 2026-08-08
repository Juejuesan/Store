# In your app, create a migration file: python manage.py makemigrations --empty yourapp
# Then modify it like this:

from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')

    categories_data = [
        # Clothing categories
        {
            'name': 'T-Shirts',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Shirts',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Dresses',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Jackets',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Sweaters',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Hoodies',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Swimwear',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        # Sportswear (using clothing sizes)
        {
            'name': 'Sports T-Shirts',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Sports Shorts',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Tracksuits',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Sports Bras',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Compression Wear',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Yoga Pants',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        {
            'name': 'Training Jerseys',
            'size_type': 'clothing',
            'size_label': 'Size',
        },
        # Pants/Jeans categories
        {
            'name': 'Jeans',
            'size_type': 'pants',
            'size_label': 'Waist Size',
        },
        {
            'name': 'Trousers',
            'size_type': 'pants',
            'size_label': 'Waist Size',
        },
        {
            'name': 'Shorts',
            'size_type': 'pants',
            'size_label': 'Waist Size',
        },
        # Shoe categories
        {
            'name': 'Sneakers',
            'size_type': 'shoe',
            'size_label': 'Shoe Size',
        },
        {
            'name': 'Boots',
            'size_type': 'shoe',
            'size_label': 'Shoe Size',
        },
        {
            'name': 'Sandals',
            'size_type': 'shoe',
            'size_label': 'Shoe Size',
        },
        {
            'name': 'Formal Shoes',
            'size_type': 'shoe',
            'size_label': 'Shoe Size',
        },
        {
            'name': 'Sports Shoes',
            'size_type': 'shoe',
            'size_label': 'Shoe Size',
        },
        # Ring categories
        {
            'name': 'Rings',
            'size_type': 'ring',
            'size_label': 'Ring Size',
        },
        # Baby/Kids categories
        {
            'name': 'Baby Onesies',
            'size_type': 'baby',
            'size_label': 'Age/Size',
        },
        {
            'name': 'Baby T-Shirts',
            'size_type': 'baby',
            'size_label': 'Age/Size',
        },
        {
            'name': 'Baby Pants',
            'size_type': 'baby',
            'size_label': 'Age/Size',
        },
        {
            'name': 'Kids Dresses',
            'size_type': 'baby',
            'size_label': 'Age/Size',
        },
        # No size categories
        {
            'name': 'Hats',
            'size_type': 'none',
            'size_label': None,
        },
        {
            'name': 'Scarves',
            'size_type': 'none',
            'size_label': None,
        },
        {
            'name': 'Belts',
            'size_type': 'none',
            'size_label': None,
        },
        {
            'name': 'Bags',
            'size_type': 'none',
            'size_label': None,
        },
        {
            'name': 'Sunglasses',
            'size_type': 'none',
            'size_label': None,
        },
        {
            'name': 'Wallets',
            'size_type': 'none',
            'size_label': None,
        },
        {
            'name': 'Jewelry (except rings)',
            'size_type': 'none',
            'size_label': None,
        },
        {
            'name': 'Socks',
            'size_type': 'none',
            'size_label': None,
        },
    ]

    for category_data in categories_data:
        Category.objects.create(**category_data)


def remove_categories(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0001_initial'),  # Replace with your last migration
    ]

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]