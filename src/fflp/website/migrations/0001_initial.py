# Generated by Django 3.2.9 on 2021-11-14 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=64)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('is_public', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('uuid', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('uuid', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('meta', models.TextField()),
                ('year', models.IntegerField()),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
                ('state', models.IntegerField(default=0)),
                ('sizes', models.TextField(default='xs,m,l,original')),
                ('creation_date', models.DateTimeField()),
                ('groups', models.ManyToManyField(to='website.Group')),
                ('tags', models.ManyToManyField(to='website.Tag')),
            ],
        ),
    ]
