from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    
    task_title = models.CharField(max_length=70, default="")
    task_description = models.CharField(max_length=2000, default="")
    status = (
        (0, _('Not Completed')),
        (1, _('Completed'))
    )
    
    task_status = models.IntegerField(choices=status, default=0, verbose_name='task status')
    
    def __str__(self) -> str:
        return self.task_title