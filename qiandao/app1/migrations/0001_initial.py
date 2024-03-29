# Generated by Django 4.1.3 on 2023-01-14 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('adminNo', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('authNo', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('classNo', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseNo', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('courseName', models.CharField(max_length=32)),
                ('grade', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='QianDao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pubtime', models.DateTimeField(auto_now_add=True)),
                ('duetime', models.DateTimeField()),
                ('qianDaoName', models.CharField(max_length=32)),
                ('courseName', models.CharField(max_length=32)),
                ('class1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.class')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentNo', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('photo', models.ImageField(default='user1.jpg', upload_to='photos')),
                ('img_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='user1.jpg', upload_to='photos')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('teacherNo', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('password', models.CharField(default='null', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Tea_Auth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authName', models.CharField(default='null', max_length=32)),
                ('authNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.authority')),
                ('teacherNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='StuQianDao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('QTime', models.DateTimeField(blank=True)),
                ('status', models.CharField(default='未签到', max_length=32)),
                ('QianDaoId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.qiandao')),
                ('studentNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.student')),
            ],
        ),
        migrations.CreateModel(
            name='Stu_Auth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authName', models.CharField(default='null', max_length=32)),
                ('authNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.authority')),
                ('studentNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.student')),
            ],
        ),
        migrations.CreateModel(
            name='QianDaoMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.student')),
            ],
        ),
        migrations.AddField(
            model_name='qiandao',
            name='teacherNo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.teacher'),
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.course'),
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to='app1.student'),
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.teacher'),
        ),
    ]
