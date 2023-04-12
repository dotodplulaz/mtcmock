
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.contrib.auth import get_user_model
from.models import *
from import_export.admin import ImportExportModelAdmin#library fo export import
from .forms import UserCreationForm, UserChangeForm

class PersonAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username','fullname','sex','option','is_staff','is_superuser',)
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username','is_staff','is_superuser',)}),
        ('Personal info', {'fields': ('fullname','sex','option','authorities')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username','is_staff','is_superuser','password1','password2')}),
        ('Personal info', {'fields': ('fullname','sex','option','authorities')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
admin.site.register(Person,PersonAdmin)

 
class MockexamAdmin(ImportExportModelAdmin):
    search_fields = ('username_id',)
    list_filter = ('username_id',)
    
    list_display=Mockexam.DisplayFields 
admin.site.register(Mockexam,MockexamAdmin)

class BestandPoorAdmin(ImportExportModelAdmin):
    search_fields = ('username','option',)
    list_filter = ('username',)
    ordering = ('username',)
    list_display=BestandPoor.DisplayFields 
admin.site.register(BestandPoor,BestandPoorAdmin)

admin.site.site_header='STUDENT MOTCO ADMIN PORTAL'
admin.site.site_title='WLCOME TO STUDENT MOTCO PORTAL '
admin.site.site_title=' Welcome to Student MOTCON Portal '
