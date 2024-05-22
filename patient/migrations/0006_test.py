# Generated by Django 4.2.2 on 2023-07-16 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_jdd'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('appointment_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='patient.visit')),
                ('remark', models.CharField(max_length=250, null=True)),
                ('test1', models.CharField(max_length=100, null=True)),
                ('test2', models.CharField(max_length=100, null=True)),
                ('test3', models.CharField(max_length=100, null=True)),
                ('test4', models.CharField(max_length=100, null=True)),
                ('test5', models.CharField(max_length=100, null=True)),
                ('test6', models.CharField(max_length=100, null=True)),
                ('test7', models.CharField(max_length=100, null=True)),
                ('test8', models.CharField(max_length=100, null=True)),
                ('test9', models.CharField(max_length=100, null=True)),
                ('test10', models.CharField(max_length=100, null=True)),
                ('test11', models.CharField(max_length=100, null=True)),
                ('test12', models.CharField(max_length=100, null=True)),
                ('test13', models.CharField(max_length=100, null=True)),
                ('test14', models.CharField(max_length=100, null=True)),
                ('test15', models.CharField(max_length=100, null=True)),
                ('test16', models.CharField(max_length=100, null=True)),
                ('test17', models.CharField(max_length=100, null=True)),
                ('test18', models.CharField(max_length=100, null=True)),
                ('date_and_time', models.DateTimeField(auto_now_add=True)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patientprimarydata')),
            ],
        ),
    ]
