# Generated by Django 3.0.7 on 2020-09-25 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecipeViewer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='RecipeImages/default.jpeg', upload_to='RecipeImages/'),
        ),
    ]
