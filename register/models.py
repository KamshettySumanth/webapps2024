from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from .managers import CustomUserManager
from .lists import CURRENCIES
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from payapp.utils import exchange_rate

class BaseModel(models.Model):
    """
    Abstract base class that is inheriated by all model class for time stamping
    """
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        try:
            from timestamp_service.thrift_client import send_timestamp
            timestamp = send_timestamp()
        except:
            timestamp=datetime.datetime.now()
        self.updated_at=timestamp
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'currency']

    objects = CustomUserManager()

    @receiver(post_save, sender='register.CustomUser')
    def initialize_balance(sender, instance, created, **kwargs):
        """ Initialize the initial balance of the user """
        if created:
            amount = UserBalance.objects.create(user=instance)
            rate = exchange_rate('USD', instance.currency)
            if rate is not None:
                amount.balance = amount.balance * rate
                amount.save()

        




class UserBalance(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=9, decimal_places=2, default=1000)

    def __str__(self):
        return self.balance
