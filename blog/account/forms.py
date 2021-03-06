from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'is_author', 'is_active', 'is_admin')


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input100'}))


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'input100', 'placeholder': 'Email Address'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input100', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input100', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input100', 'placeholder': 'Confirm Password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email).exists()
        if qs:
            raise ValidationError('This Email is Already Taken!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username).exists()
        if qs:
            raise ValidationError('This Username is Already Taken!')
        return username

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            raise ValidationError('Password and Confirm Password Must Match!')
        return password2


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email Address'})

    def clean_username(self):
        username = self.cleaned_data['username']
        self_username = self.request.user.username

        if username != self_username:
            qs = User.objects.filter(username=username).exists()
            if qs:
                raise ValidationError('This Username is Already Taken!')
            return username
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        self_email = self.request.user.email

        if email != self_email:
            qs = User.objects.filter(email=email, id=self.request.user.id).exists()
            if qs:
                raise ValidationError('This Email is Already Taken!')
            return email
        return email