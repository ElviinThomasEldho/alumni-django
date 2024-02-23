# Generated by Django 5.0.2 on 2024-02-23 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_account_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='Likes', to='main.account'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
