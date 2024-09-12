# Generated by Django 5.1.1 on 2024-09-10 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='scrapeddata',
            name='description',
        ),
        migrations.RemoveField(
            model_name='scrapeddata',
            name='stock',
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='fitments',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='includes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='load_bearing',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='manufacturer_part_number',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='material',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='placement',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='sku',
            field=models.CharField(default='default_sku', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='surface_finish',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='warranty',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='scrapeddata',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.brand'),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.producttype'),
        ),
    ]
