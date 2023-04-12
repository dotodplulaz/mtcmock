
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from .managers import UserManager


class Person(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Username', max_length=100,primary_key=True) 
    fullname = models.CharField(_('full name'), max_length=130, blank=True)
    sex = models.CharField(_('Gender'), max_length=10,default='MALE',blank=True, null=True)
    option = models.CharField(_('Option'),max_length=10, default='NONE',blank=True, null=True)
    AUTHORITIES=(
      
        ('admin', 'admin'),
        ('principal', 'principal'),
        ('academic', 'academic'),
        ('staff', 'staff'),
        ('student', 'student'),
	  	)
    authorities = models.CharField(_('Role authorities'), max_length=30, choices=AUTHORITIES)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True,blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname','sex','option','authorities',]

    objects = UserManager()

    class Meta:
        db_table="Person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Mockexam(models.Model):
    username  = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    subject= models.JSONField(_('Subjects') ,blank=True, null=True)
    grade= models.JSONField(_('Grade') ,blank=True, null=True)
    division = models.CharField(_('Division'),max_length=10)
    point = models.IntegerField(_('grade point'))
    DisplayFields=['username_id','subject','grade','point','division']
    class Meta:
        db_table = "Mockexam"
    def __str__(self):
        return self.username_id


class BestandPoor(models.Model):
    username = models.CharField(verbose_name='Username', max_length=100,primary_key=True) 
    fullname = models.CharField(_('full name'), max_length=130, blank=True)
    sex = models.CharField(_('Gender'), max_length=10,default='MALE',blank=True, null=True)
    option = models.CharField(_('Option'),max_length=10, default='NONE',blank=True, null=True)
    phy= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    chem= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    bio= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    math= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    edu= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    comp= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    bam= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    gs= models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    DisplayFields=['username','fullname','sex','option','phy','chem','bio','math','edu','comp','gs','bam' ]
    class Meta:
        db_table = "BestandPoor"
    def __str__(self):
        return self.username
