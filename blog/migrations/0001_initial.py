# Generated by Django 4.1.4 on 2022-12-25 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='Category name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Article title')),
                ('content', models.TextField(verbose_name='Article means')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='Photography')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('uploaded_at', models.DateTimeField(auto_now=True, verbose_name='Changed date')),
                ('publish', models.BooleanField(default=True, verbose_name='Article status')),
                ('views', models.IntegerField(default=0, verbose_name='Number of views')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
    ]
