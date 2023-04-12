from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):


    def create_user(self,username, password, fullname,sex,option,authorities,**extra_fields):
        """         Create and save a User with the given email and password.         """
        # if not phonenumber :
        #     raise ValueError(_('The phonenumber  must be Entered'))
        # phonenumber  = self.normalize_phonenumber(phonenumber)

        if not fullname :
            raise ValueError(_('The fullname   must be Entered'))
        # fullname  = self.normalize_fullname(fullname)
        user = self.model(username=username,fullname=fullname,sex=sex,option=option,authorities=authorities,**extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,username,password, fullname,sex,option,authorities,**extra_fields):
        """         Create and save a SuperUser with the given phonenumber and password.         """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff be True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser be True.'))
        return self.create_user(username, password, fullname,sex,option,authorities, **extra_fields)
