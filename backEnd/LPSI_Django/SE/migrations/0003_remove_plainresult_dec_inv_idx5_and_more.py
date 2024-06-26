# Generated by Django 4.2.1 on 2023-11-17 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SE', '0002_plainresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plainresult',
            name='dec_inv_idx5',
        ),
        migrations.RemoveField(
            model_name='plainresult',
            name='dec_inv_idx6',
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword1',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词1'),
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword2',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词2'),
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword3',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词3'),
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword4',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词4'),
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword5',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词5'),
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword6',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词6'),
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword7',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词7'),
        ),
        migrations.AlterField(
            model_name='keywordshistory',
            name='Keyword8',
            field=models.CharField(max_length=20, null=True, verbose_name='关键词8'),
        ),
        migrations.AlterField(
            model_name='plainresult',
            name='dec_inv_idx1',
            field=models.CharField(max_length=100, null=True, verbose_name='明文结果1'),
        ),
        migrations.AlterField(
            model_name='plainresult',
            name='dec_inv_idx2',
            field=models.CharField(max_length=100, null=True, verbose_name='明文结果2'),
        ),
        migrations.AlterField(
            model_name='plainresult',
            name='dec_inv_idx3',
            field=models.CharField(max_length=100, null=True, verbose_name='明文结果3'),
        ),
        migrations.AlterField(
            model_name='plainresult',
            name='dec_inv_idx4',
            field=models.CharField(max_length=100, null=True, verbose_name='明文结果4'),
        ),
    ]
