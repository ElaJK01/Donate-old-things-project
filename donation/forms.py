from django import forms
from django.forms import ModelForm
from django.forms import ModelMultipleChoiceField
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, CheckboxSelectMultiple, RadioSelect, SelectDateWidget
from donation.models import MyUser, Donation, Category, Institution
from phone_field.forms import PhoneFormField


class MyAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Hasło'}))


class RegisterForm(forms.Form):
    name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Imię'}), label='')
    last_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Nazwisko'}), label='')
    email = forms.CharField(widget=TextInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = MyUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class DateInput(forms.DateInput):
    input_type= 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class DonationForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple, queryset=Category.objects.all())
    quantity = forms.IntegerField()
    institution = forms.ModelChoiceField(widget=RadioSelect, queryset=Institution.objects.all())
    address = forms.CharField(max_length=60)
    city = forms.CharField(max_length=100)
    postcode = forms.CharField(max_length=6)
    phone = PhoneFormField()
    date = forms.DateField(widget=DateInput)
    time = forms.TimeField(widget=TimeInput)
    comments = forms.CharField(widget=forms.Textarea(attrs={'size': '20'}), required=False)


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'name', 'last_name', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UpdateUserForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'name', 'last_name']

    widgets = {
        "email": forms.EmailInput(),
    }
    labels = {
        "name": "Imię",
        "last_name": "Naziwsko",
        "email": "Adress Email",
    }





