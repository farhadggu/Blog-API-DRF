# Generated by Django 4.0.1 on 2022-01-21 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_article_visit_count_delete_ipaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_reply',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply',
        ),
    ]
