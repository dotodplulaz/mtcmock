# Generated by Django 3.2.6 on 2023-04-09 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mock2023', '0002_auto_20230406_0452'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestandPoor',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Username')),
                ('fullname', models.CharField(blank=True, max_length=130, verbose_name='full name')),
                ('sex', models.CharField(blank=True, default='MALE', max_length=10, null=True, verbose_name='Gender')),
                ('option', models.CharField(blank=True, default='NONE', max_length=10, null=True, verbose_name='Option')),
                ('phy', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('chem', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('bio', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('math', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('edu', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('comp', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('bam', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('gs', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
            ],
            options={
                'db_table': 'BestandPoor',
            },
        ),
    ]
