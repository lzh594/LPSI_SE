# Generated by Django 4.2.1 on 2023-11-16 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SE', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlainResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dec_inv_idx1', models.CharField(max_length=100, verbose_name='明文结果1')),
                ('dec_inv_idx2', models.CharField(max_length=100, verbose_name='明文结果2')),
                ('dec_inv_idx3', models.CharField(max_length=100, verbose_name='明文结果3')),
                ('dec_inv_idx4', models.CharField(max_length=100, verbose_name='明文结果4')),
                ('dec_inv_idx5', models.CharField(max_length=100, verbose_name='明文结果5')),
                ('dec_inv_idx6', models.CharField(max_length=100, verbose_name='明文结果6')),
            ],
        ),
    ]
