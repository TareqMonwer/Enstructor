# Generated by Django 2.2.13 on 2021-02-16 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='courses/banners/'),
        ),
    ]