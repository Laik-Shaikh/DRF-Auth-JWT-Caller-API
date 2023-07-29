# Generated by Django 4.2.3 on 2023-07-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_contactlist_registeruser_delete_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('spamCount', models.PositiveIntegerField(default=1)),
            ],
        ),
    ]