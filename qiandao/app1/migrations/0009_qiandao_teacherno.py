# Generated by Django 2.2.2 on 2023-01-10 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20230110_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='qiandao',
            name='teacherNo',
            field=models.ForeignKey(default=10000000, on_delete=django.db.models.deletion.CASCADE, to='app1.Teacher'),
            preserve_default=False,
        ),
    ]
