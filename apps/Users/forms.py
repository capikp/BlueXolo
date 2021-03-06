from django import forms

from apps.Products.models import Source
from .models import User

ROLES_CHOICES = (
    (None, 'Choose a role'),
    ('tester', 'Tester'),
    ('developer', 'Developer'),
    ('auditor', 'Auditor'),
    ('owner', 'Owner'),
)


class UserForm(forms.ModelForm):
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(), label="Confirm Password")
    role = forms.CharField(widget=forms.Select(choices=ROLES_CHOICES))

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'products',
            'role',
            'password',
            'password2',
        ]
        widgets = {
            "email": forms.EmailInput(),
            "password": forms.PasswordInput()
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.count() > 0:
            raise forms.ValidationError("The email {} already exist".format(email))
        else:
            return self.cleaned_data['email']

    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
                raise forms.ValidationError("The password do not match")
        else:
            return self.cleaned_data

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 3(Products)"""
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = Source.objects.filter(category=3)
        self.fields['products'].required = True


class EditUserForm(forms.ModelForm):
    role = forms.CharField(widget=forms.Select(choices=ROLES_CHOICES))

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'is_active',
            'products',
            'role'
        ]
        widgets = {
            "email": forms.EmailInput()
        }

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 3(Products)"""
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = Source.objects.filter(category=3)
        self.fields['products'].required = True


class RequestAccessForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'products'
        ]
        widgets = {
            "email": forms.EmailInput()
        }

    def __init__(self, *args, **kwargs):
        """This filter only for sources in the category 3(Products)"""
        super(RequestAccessForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = Source.objects.filter(category=3)
        self.fields['products'].required = True
