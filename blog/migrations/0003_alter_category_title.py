# Generated by Django 4.1.4 on 2023-01-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_uploaded_at_article_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=30, unique=True, verbose_name='Category title'),
        ),
    ]
