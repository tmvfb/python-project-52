from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Task(models.Model):

    name = models.CharField(
        max_length=50, unique=True, verbose_name=_('Task name '),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at '),
    )

    def __str__(self):
        return self.name
