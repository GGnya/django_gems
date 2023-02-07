from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from gems.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance,
                               user_alias=instance.username)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# @receiver(post_save, sender=User)
# def create_gem(sender, instance, created, **kwargs):
#     if created:
#         Gem.objects.