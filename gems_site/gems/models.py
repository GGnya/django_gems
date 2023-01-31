from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class Gem(models.Model):
    size = models.FloatField(verbose_name='Размер')
    type = models.ForeignKey('GemType', on_delete=models.PROTECT, verbose_name='Тип камня')
    clarity = models.CharField(max_length=2, verbose_name='Чистота')
    gem_image = models.ImageField(blank=True)
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', verbose_name='Цена')
    owner = models.ForeignKey('GemOwner', on_delete=models.CASCADE, verbose_name='Продавец')
    is_available = models.BooleanField(verbose_name='Доступность')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')
    customer = models.ForeignKey('GemCustomer', on_delete=models.PROTECT, verbose_name='Покупатель')


class GemType(models.Model):
    type = models.CharField(max_length=50, verbose_name='Тип камня')


class BaseUserMixin(models.Model):
    first_name = models.CharField(max_length=70, verbose_name='Имя')
    last_name = models.CharField(max_length=70, verbose_name='Фамилия', blank=True)
    email = models.EmailField(verbose_name='Email')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', blank=True)
    user_alias = models.SlugField(verbose_name='Псевдоним', db_index=True)
    logo = models.ImageField(verbose_name='Лого', blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        abstract = True


class GemOwner(BaseUserMixin):
    organization = models.CharField(max_length=70, verbose_name='Названия организации', blank=True)
    bank_account_number = models.BigIntegerField(verbose_name='Номер банковского аккаунта', blank=True)


class GemCustomer(BaseUserMixin):
    pass
