from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    dob = models.DateTimeField(null=True, blank=True)
    address = models.TextField(null=True)
    balance = models.IntegerField(default=0)
    gender = models.CharField(max_length=6, choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
                              null=True)

    def __str__(self):
        return str(self.user.username)


class ManageFunds(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    add = models.FloatField(default=0)
    withdraw = models.FloatField(default=0)


class ItemForm(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    img = models.ImageField(upload_to='images/')

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # to remove
#     try:
#         instance.profile.save()
#     except:
#         pass
