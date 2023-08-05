from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class UserFcmToken(models.Model):
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="token_user"
    )
    fcm_token = models.TextField(
        _("FCM Token"), default=""
    )


class UserMobileFcmToken(models.Model):
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="token_mobile_user"
    )
    fcm_token = models.TextField(
        _("FCM Token"), default=""
    )
