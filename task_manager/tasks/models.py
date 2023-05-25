from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):

    name = models.CharField(
        max_length=50, unique=True, verbose_name=_('Task name'),
    )
    description = models.TextField(
        max_length=1000, verbose_name=_('Description'), default=''
    )
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, null=True,
        verbose_name=_('Status')
    )
    assigned_by = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name='creator',
        verbose_name=_('Creator')
    )
    assigned_to = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name='assignee',
        verbose_name=_('Assignee')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at '),
    )

    def __str__(self):
        return self.name
