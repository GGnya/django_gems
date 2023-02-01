from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from pytils.translit import slugify

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField


class Gem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from=(lambda instance: slugify(instance.title)),
                         slugify=lambda value: value.replace(' ', '-'),
                         unique=True, db_index=True, verbose_name="URL")
    size = models.FloatField(verbose_name='Размер')
    type = models.ForeignKey('GemType', on_delete=models.PROTECT, verbose_name='Тип камня')
    clarity = models.CharField(max_length=2, verbose_name='Чистота')
    gem_image = models.ImageField(blank=True)
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', verbose_name='Цена')
    # owner = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Продавец', related_name='owner_set')
    is_available = models.BooleanField(verbose_name='Доступность')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')
    # customer = models.ForeignKey('Profile', on_delete=models.PROTECT, verbose_name='Покупатель', related_name='customer_set')

    def __str__(self):
        return self.title

class GemType(models.Model):
    type = models.CharField(max_length=50, verbose_name='Тип камня')

    def __str__(self):
        return self.type


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=70, verbose_name='Имя')
#     last_name = models.CharField(max_length=70, verbose_name='Фамилия', blank=True)
#     email = models.EmailField(verbose_name='Email')
#     # phone_number = PhoneNumberField(verbose_name='Номер телефона', blank=True)
#     user_alias = models.SlugField(verbose_name='Псевдоним', db_index=True)
#     logo = models.ImageField(verbose_name='Лого', blank=True)
#     date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#     organization = models.CharField(max_length=70, verbose_name='Названия организации', blank=True)
#     bank_account_number = models.BigIntegerField(verbose_name='Номер банковского аккаунта', blank=True, default=None)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

