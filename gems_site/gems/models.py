from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField
from uuslug import uuslug


def instance_gem_slug(instance):
    return instance.title


def slugify_value(value):
    return value.replace(' ', '-')


class Gem(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from=instance_gem_slug,
                         slugify=slugify_value,
                         unique=True, db_index=True, verbose_name="URL")
    size = models.FloatField(verbose_name='Размер')
    type = models.ForeignKey('GemType', on_delete=models.PROTECT, verbose_name='Тип камня')
    clarity = models.CharField(max_length=2, verbose_name='Чистота')
    gem_image = models.ImageField(blank=True)
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='RUB', verbose_name='Цена')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Продавец', blank=True, null=True)
    is_available = models.BooleanField(verbose_name='Доступность')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего редактирования')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        last_id = Gem.objects.last().pk
        self.slug = uuslug(self.title, instance=self) + str(last_id + 1)
        super(Gem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gem', kwargs={'gem_slug': self.slug})


class GemType(models.Model):
    type = models.CharField(max_length=50, verbose_name='Тип камня')

    def __str__(self):
        return self.type


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Логин')
    phone_number = PhoneNumberField(verbose_name='Номер телефона', blank=True)
    user_alias = models.SlugField(verbose_name='Псевдоним', db_index=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.username.username
