
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields = ('username','fullname','sex','option','authorities',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Error Occured!! Passwords does not  match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user





class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model =Person
        fields = ('username','fullname','sex','option','authorities','is_active','is_superuser')

    # def clean_password(self):
    #     return self.initial["password"]
