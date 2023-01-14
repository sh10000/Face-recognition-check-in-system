# Generated by Django 4.1.3 on 2023-01-14 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_qiandao_teacherno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='password',
        ),
        migrations.AddField(
            model_name='stuqiandao',
            name='status',
            field=models.CharField(default='未签到', max_length=32),
        ),
        migrations.AddField(
            model_name='tea_auth',
            name='authName',
            field=models.CharField(default='null', max_length=32),
        ),
        migrations.AlterField(
            model_name='qiandaomessage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stu_auth',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='studentphoto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stuqiandao',
            name='QTime',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='stuqiandao',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='tea_auth',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
