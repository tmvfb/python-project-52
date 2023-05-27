from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
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
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='assignee',
        verbose_name=_('Assignee'), blank=True, default='', null=True
    )
    labels = models.ManyToManyField(
        Label, through='LabelM2m', related_name='labels', blank=True,
        verbose_name=_('Label')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at '),
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name


class LabelM2m(models.Model):  # noqa DJ08 DJ110 DJ11
    # create restrictions for label-task m2m
    label = models.ForeignKey(Label, on_delete=models.PROTECT, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
