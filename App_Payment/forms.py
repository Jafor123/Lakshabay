from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from App_Payment.models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class BillingForm(forms.ModelForm):
    firstname=forms.CharField(max_length=50,label="First Name")
    lastname=forms.CharField(max_length=50,label="Last Name")
    company=forms.CharField(max_length=50,label="Company")
    country=forms.CharField(max_length=50,label="Country")
    address=forms.CharField(max_length=50,label="Address")
    address2=forms.CharField(max_length=50,label="Address 2")
    city=forms.CharField(max_length=50,label="City")
    state=forms.CharField(max_length=50,label="State")
    zipcode=forms.IntegerField(label="Zipcode")
    phone=forms.IntegerField(label="Phone")
    aditional_info = forms.CharField(label="Additional Informatio (optional)",required=False,widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'cols': 40,
        'padding': '10px',
        'placeholder': "Enter  your Text here",
    }))
    class Meta:
        model=BillingAddress
        fields=('firstname','lastname','company','country','address','address2','city','state','zipcode','phone','aditional_info')





