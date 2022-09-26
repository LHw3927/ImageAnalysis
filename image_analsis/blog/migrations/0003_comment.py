# Generated by Django 3.2.12 on 2022-09-22 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220919_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('create_at', models.DateField(auto_now=True)),
            ],
        ),
    ]