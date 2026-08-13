from django.db import migrations


def add_perfume(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')

    Category.objects.get_or_create(
        name='Perfume',
        defaults={
            'size_type': 'none',
            'size_label': None,
        }
    )


def remove_perfume(apps, schema_editor):
    Category = apps.get_model('posts', 'Category')

    Category.objects.filter(name='Perfume').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_create_default_categories'),
    ]

    operations = [
        migrations.RunPython(add_perfume, remove_perfume),
    ]