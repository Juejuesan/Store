from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model("posts", "Category")

    categories = [
         "Electronics",
         "Fashion",
         "Books",
         "Furniture",
         "Sports",
         "Home Appliances",
         "Beauty",
         "Toys",
         "Food",
         "Vehicles"
    ]

    for name in categories:
        Category.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]