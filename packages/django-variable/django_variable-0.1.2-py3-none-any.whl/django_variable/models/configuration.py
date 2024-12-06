from django.db import models
from django.conf import settings

class Configuration(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='configurations', default=None, null=True, blank=True)
    created_at = models.DateTimeField(
        null=False,
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        null=False,
        auto_now=True
    )

    class Meta:
        verbose_name_plural = 'Configurations'
        verbose_name = 'Configuration'

    def __str__(self):
        return self.key