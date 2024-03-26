from django.db import models


# Create your models here.

# 关键词历史记录
class KeywordsHistory(models.Model):
    Keyword1 = models.CharField(max_length=20, verbose_name="关键词1", name="Keyword1", null=True)
    Keyword2 = models.CharField(max_length=20, verbose_name="关键词2", name="Keyword2", null=True)
    Keyword3 = models.CharField(max_length=20, verbose_name="关键词3", name="Keyword3", null=True)
    Keyword4 = models.CharField(max_length=20, verbose_name="关键词4", name="Keyword4", null=True)
    Keyword5 = models.CharField(max_length=20, verbose_name="关键词5", name="Keyword5", null=True)
    Keyword6 = models.CharField(max_length=20, verbose_name="关键词6", name="Keyword6", null=True)
    Keyword7 = models.CharField(max_length=20, verbose_name="关键词7", name="Keyword7", null=True)
    Keyword8 = models.CharField(max_length=20, verbose_name="关键词8", name="Keyword8", null=True)

    # def display_attributes(self):
    #     attributes = self.__dict__
    #     attribute_values = []
    #     for attribute_name, attribute_value in attributes.items():
    #         if not attribute_name.startswith()

# 明文结果的数据库
class PlainResult(models.Model):
    dec_inv_idx1 = models.CharField(max_length=100, verbose_name="明文结果1", name="dec_inv_idx1", null=True)
    dec_inv_idx2 = models.CharField(max_length=100, verbose_name="明文结果2", name="dec_inv_idx2", null=True)
    dec_inv_idx3 = models.CharField(max_length=100, verbose_name="明文结果3", name="dec_inv_idx3", null=True)
    dec_inv_idx4 = models.CharField(max_length=100, verbose_name="明文结果4", name="dec_inv_idx4", null=True)
