# Generated by Django 4.1.4 on 2023-01-28 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_newposts_delete_contact'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewPosts',
            new_name='NewPost',
        ),
        migrations.AlterModelOptions(
            name='newpost',
            options={'verbose_name': 'New Post', 'verbose_name_plural': 'New Posts'},
        ),
    ]
