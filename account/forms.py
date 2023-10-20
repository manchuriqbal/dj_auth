from typing import Any
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForms(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    username = forms.CharField( 
        max_length=150
    )
    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput       
    )

class RegistationForms(forms.ModelForm):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password"
        )
    
    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        model = self.Meta.model

        if model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with the Username already exists")
        
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        model = self.Meta.model

        if model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with the Email already exists")


    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        password2 = self.data.get('password2')

        if password != password2:
            raise forms.ValidationError('Password Mismatch')
        return password

    def save(self, commit=True, *args, **kwargs):
        user = self.instance
        password = self.cleaned_data.get("password")
        user.set_password(password)

        if commit:
            user.save()

        return user
    

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=150, widget=forms.PasswordInput)
    new_password1 = forms.CharField(max_length=150, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=150, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    
    def clean_new_password1(self, *args, **kwargs):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.data.get("new_password2")
   

        if new_password1 != new_password2:
            raise forms.ValidationError('Password Mismatch')
        return new_password1
    

    def clean_current_password(self, *args, **kwargs):
        current_password = self.cleaned_data.get("current_password")
   

        if not self.user.check_password(current_password):
            raise forms.ValidationError('Invalid Password')
        return current_password