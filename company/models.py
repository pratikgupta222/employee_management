from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Company(models.Model):
    name = models.CharField(_('Company Name'), max_length=200)

    emp_prefix = models.CharField(_('Employee Prefix'), max_length=4)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Company")

    def __str__(self):
        return self.name
