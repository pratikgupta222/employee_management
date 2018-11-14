from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from employee import constants as EmpConst


class Employee(models.Model):
    uid = models.CharField(_('Unique ID'), max_length=12, unique=True)

    fname = models.CharField(_('First Name'), max_length=255)

    lname = models.CharField(_('Last Name'), max_length=255)

    phone = PhoneNumberField(
        _("Mobile Number"), blank=True,
        help_text=_("Employee's primary mobile number e.g. +91{10 digit mobile number}"))
    email = models.EmailField(
        _('email address'), max_length=255, unique=True, db_index=True)

    role = models.CharField(_('Role'), max_length=15,
                            choices=EmpConst.ROLE_CHOICES, default=EmpConst.REGULAR)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return self.uid
