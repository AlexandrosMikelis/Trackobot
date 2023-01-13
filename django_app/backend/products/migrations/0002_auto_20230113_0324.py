# Generated by Django 3.2.16 on 2023-01-13 01:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='content',
        ),
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=48, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Pharmacy', 'PHARMACY')], max_length=30, null=True),
        ),
    ]
