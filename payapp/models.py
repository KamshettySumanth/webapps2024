from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from register.lists import CURRENCIES
from register.lists import NOTIFICATION
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Payment(BaseModel):
    sender = models.ForeignKey(
        'register.CustomUser', related_name="sent_payment", on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        'register.CustomUser', related_name="received_payment", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.amount > self.sender.balance:
            raise ValidationError(_("Insufficient Balance"))

    def __str__(self):
        return f"{self.sender.first_name} to {self.recipient.first_name}"
    

    @receiver(post_save, sender='payapp.Payment')
    def payment_send_notify(instance, created, *args, **kwargs):
        if created:
            Notification.objects.create(
                user=instance.recipient,
                message=f"You received a payment of {instance.sender.currency} {instance.amount} by {instance.sender}",
                type="payment_received"
            )



class PaymentRequest(BaseModel):
    requested_from = models.ForeignKey(
        'register.CustomUser', related_name="requested_transactions", on_delete=models.CASCADE)
    requested_to = models.ForeignKey(
        'register.CustomUser', related_name="received_requests", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_accepted = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.requested_from.first_name} to {self.requested_to.first_name}"

    class Meta:
        ordering = ["-created_at"]

    
    @receiver(post_save, sender='payapp.PaymentRequest')
    def payment_request_result_notify(instance, created, **kwargs):
        if not created:
            send_to = instance.requested_to
            result = "accepted" if instance.is_accepted else "rejected"
            Notification.objects.create(
                user=send_to,
                message=f"Payment request of amount {instance.requested_to.currency} {instance.amount} from {instance.requested_to} was {result}",
                type="payment_request_result"
            )
        if created:
            send_from = instance.requested_from
            print("test point")

            notification = Notification.objects.create(
                user=send_from,
                message=f"Payment request of amount {instance.requested_to.currency} {instance.amount} from {instance.requested_to} was received",
                type="payment_request_receive"
            )

            notification.save()



class Notification(BaseModel):
    user = models.ForeignKey(
        'register.CustomUser', related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    is_seen = models.BooleanField(default=False)
    type = models.CharField(
        max_length=50, choices=NOTIFICATION, default="payment_received")

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']
