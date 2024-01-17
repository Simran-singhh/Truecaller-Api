from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


phone_regex = r'^\+?1?\d{9,15}$'

class GlobalContactDump(models.Model):
    name = models.CharField(max_length=20)
    phone_regex = RegexValidator(regex=phone_regex)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField(max_length=30, null=True, blank=True)
    registered = models.BooleanField(default=False)

class User(models.Model):
    name = models.CharField(max_length=20)
    phone_regex = RegexValidator(regex=phone_regex)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.phone_number})'

class UserRelationship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['from_user', 'to_user']

@receiver(post_save, sender=User)
def create_global_dump(sender, instance, created, **kwargs):
    if created:
        name = instance.name
        phone_number = instance.phone_number
        email = instance.email
        registered = True
        GlobalContactDump.objects.create(name=name, phone_number=phone_number,email=email,registered=registered)
    return

