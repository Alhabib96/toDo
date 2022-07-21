# Generated by Django 4.0.5 on 2022-07-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_db_logger', '0004_task_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('SPORTS', 'Sports'), ('FOOD & DRINK', 'Food & Drink'), ('WORK', 'Work'), ('PERSONAL', 'Personal'), ('STUDY', 'Study'), ('VISIT', 'Visit'), ('OTHER', 'Other')], default='OT', max_length=20, null=True),
        ),
    ]
