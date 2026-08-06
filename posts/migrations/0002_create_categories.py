from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')

    categories = [
        # CLOTHING
        {'name': 'T-Shirts', 'size_type': 'clothing', 'size_label': 'Size', 'custom_sizes': ''},
        {'name': 'Shirts', 'size_type': 'clothing', 'size_label': 'Size', 'custom_sizes': ''},
        {'name': 'Hoodies', 'size_type': 'clothing', 'size_label': 'Size', 'custom_sizes': ''},
        {'name': 'Jackets', 'size_type': 'clothing', 'size_label': 'Size', 'custom_sizes': ''},
        {'name': 'Sweaters', 'size_type': 'clothing', 'size_label': 'Size', 'custom_sizes': ''},
        {'name': 'Dresses', 'size_type': 'clothing', 'size_label': 'Size', 'custom_sizes': ''},
        {'name': 'Sport Wear', 'size_type': 'clothing', 'size_label': 'Size', 'custom_sizes': ''},

        # PANTS
        {'name': 'Jeans', 'size_type': 'pants', 'size_label': 'Waist Size (inches)', 'custom_sizes': ''},
        {'name': 'Pants', 'size_type': 'pants', 'size_label': 'Waist Size (inches)', 'custom_sizes': ''},
        {'name': 'Shorts', 'size_type': 'pants', 'size_label': 'Waist Size (inches)', 'custom_sizes': ''},

        # SHOES
        {'name': 'Sneakers', 'size_type': 'shoe', 'size_label': 'EU Size', 'custom_sizes': ''},
        {'name': 'Formal Shoes', 'size_type': 'shoe', 'size_label': 'EU Size', 'custom_sizes': ''},
        {'name': 'Sandals', 'size_type': 'shoe', 'size_label': 'EU Size', 'custom_sizes': ''},
        {'name': 'Boots', 'size_type': 'shoe', 'size_label': 'EU Size', 'custom_sizes': ''},

        # RINGS
        {'name': 'Rings', 'size_type': 'ring', 'size_label': 'Ring Size (US)', 'custom_sizes': ''},

        # BABY/KIDS
        {'name': 'Baby Clothes', 'size_type': 'baby', 'size_label': 'Age Group', 'custom_sizes': ''},
        {'name': 'Kids Clothes', 'size_type': 'baby', 'size_label': 'Age Group', 'custom_sizes': ''},

        # NO SIZES
        {'name': 'Bags', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
        {'name': 'Wallets', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
        {'name': 'Watches', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
        {'name': 'Sunglasses', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
        {'name': 'Electronics', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
        {'name': 'Books', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
        {'name': 'Toys', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
        {'name': 'Perfumes', 'size_type': 'none', 'size_label': '', 'custom_sizes': ''},
    ]

    for cat_data in categories:
        Category.objects.create(**cat_data)


def remove_categories(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0001_initial'),  # Change this to your last migration name
    ]

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]