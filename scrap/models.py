from django.db import models


class Categories(models.Model):
    name = models.CharField('категория', max_length=256)
    url = models.URLField('URL', default='')

    def __str__(self):
        return self.name


class Ads(models.Model):
    category = models.ForeignKey(Categories, verbose_name='категория', blank=True, null=True)
    header = models.CharField('заголовок', max_length=256)
    city = models.CharField('город', max_length=64)
    price = models.CharField('цена', max_length=64)
    position = models.IntegerField('позиция объявления')

    def __str__(self):
        return self.header
