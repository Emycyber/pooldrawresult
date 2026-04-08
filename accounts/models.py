from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_vip = models.BooleanField(default=False)
    vip_activated_on = models.DateTimeField(blank=True, null=True)
    vip_expires_on = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} — {'VIP' if self.is_vip else 'Free'}"

    @property
    def vip_is_active(self):
        from django.utils import timezone
        if not self.is_vip:
            return False
        if self.vip_expires_on and self.vip_expires_on < timezone.now().date():
            return False
        return True