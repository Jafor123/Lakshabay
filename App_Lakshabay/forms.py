from datetime import date
from django import forms
from App_Lakshabay.models import *
import re
from django.core.exceptions import ValidationError

CHOICES = (
    ('12:00 AM', '12:00 AM'),
    ('12:30 AM', '12:30 AM'),
    ('1:00 AM', '1:00 AM'),
    ('1:30 AM', '1:30 AM'),
    ('2:00 AM', '2:00 AM'),
    ('2:30 AM', '2:30 AM'),
    ('3:00 AM', '3:00 AM'),
    ('4:00 AM', '4:00 AM'),
    ('4:30 AM', '4:30 AM'),
    ('5:00 AM', '5:00 AM'),
    ('6:30 AM', '5:30 AM'),
    ('6:00 AM', '6:00 AM'),
    ('6:30 AM', '6:30 AM'),
    ('7:00 AM', '7:00 AM'),
    ('7:30 AM', '7:30 AM'),
    ('8:00 AM', '8:00 AM'),
    ('8:30 AM', '8:30 AM'),
    ('8:30 AM', '8:30 AM'),
    ('9:00 AM', '9:00 AM'),
    ('9:30 AM', '9:30 AM'),
    ('10:00 AM', '10:00 AM'),
    ('10:30 AM', '10:30 AM'),
    ('11:00 AM', '11:00 AM'),
    ('11:30 AM', '11:30 AM'),
    ('12:00 PM', '12:00 PM'),
    ('1:00 PM', '1:30 PM'),
    ('1:30 PM', '1:30 PM'),
    ('2:00 PM', '2:00 PM'),
    ('2:30 PM', '2:30 PM'),
    ('3:00 PM', '3:00 PM'),
    ('4:00 PM', '4:00 PM'),
    ('4:30 PM', '4:30 PM'),
    ('5:00 PM', '5:00 PM'),
    ('6:30 PM', '5:30 PM'),
    ('6:00 PM', '6:00 PM'),
    ('6:30 PM', '6:30 PM'),
    ('7:00 PM', '7:00 PM'),
    ('7:30 PM', '7:30 PM'),
    ('8:00 PM', '8:00 PM'),
    ('8:30 PM', '8:30 PM'),
    ('8:30 PM', '8:30 PM'),
    ('9:00 PM', '9:00 PM'),
    ('9:30 PM', '9:30 PM'),
    ('10:00 PM', '10:00 PM'),
    ('10:30 PM', '10:30 PM'),
    ('11:00 PM', '11:00 PM'),
    ('11:30 PM', '11:30 PM'),

)


def isAdd(n):
    Pattern = re.compile("^[a-zA-Z0-9.,""'' ]+$")
    return Pattern.match(n)


def isPhone(n):
    Pattern = re.compile("^((\+44\s?\d{4}|\(?\d{5}\)?)\s?\d{6})|((\+44\s?|0)7\d{3}\s?\d{6})$")
    return Pattern.match(n)
def isUkPhone(n):
    Pattern = re.compile("^(?:0|\+?44)\s?(?:\d\s?){9,11}$")
    return Pattern.match(n)


class bookForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=30)
    time = forms.CharField(widget=forms.Select(choices=CHOICES))
    phone = forms.CharField()
    email = forms.EmailField(label="Email Address")
    number_of_people = forms.IntegerField(label="No of People", widget=forms.NumberInput())
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'rows': 3,
        'cols': 40,
        'padding': '10px',
        'placeholder': "Enter  your Text here",
    }))

    class Meta:
        model = book
        fields = ['first_name', 'last_name', 'date', 'time', 'phone', 'email', 'number_of_people', 'message']
        widgets = {
            'email': forms.EmailInput(),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 4:
            raise ValidationError("** minimum 4 character allowed")

        if first_name.replace(" ", "").isalpha():
            return first_name
        else:
            raise ValidationError("** only character are allowed")

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 4:
            raise ValidationError("** minimum 4 character allowed")

        if last_name.replace(" ", "").isalpha():
            return last_name
        else:
            raise ValidationError("** only character are allowed")

    def clean_date(self):
        date = self.cleaned_data.get('date')
        today = date.today()
        if date < today:
            raise ValidationError("** date is not valid")
        else:
            return date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        print(phone)
        if isPhone(phone):
            print("ok")
            return phone
        else:
            print("no")
            raise ValidationError("** use a valid UK format")

    def clean_number_of_people(self):
        number_of_people = self.cleaned_data.get('number_of_people')
        if number_of_people > 0 and number_of_people < 100:
            return number_of_people
        else:
            raise ValidationError("** Enter a valid number")

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if isAdd(message):
            return message
        else:
            raise ValidationError("** enter a valid text")


class ContactForm(forms.ModelForm):
    name=forms.CharField(label="Name",max_length=30)
    email=forms.EmailField(max_length=200,label="Email Address")
    phone=forms.CharField(widget=forms.TextInput(attrs={
        'onkeypress' : "return event.charCode >= 8 && event.charCode <= 57",
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'rows': 3,
        'cols': 40,
        'padding': '10px',
        'placeholder': "Enter  your Text here",
    }))

    class Meta:
        model=contact
        fields='__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 4:
            raise ValidationError("** minimum 4 character allowed")

        if name.replace(" ", "").isalpha():
            return name
        else:
            raise ValidationError("** only character are allowed")

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if isAdd(message):
            return message
        else:
            raise ValidationError("** enter a valid text")

    def clean_phone(self):
        phone = str(self.cleaned_data.get('phone'))
        if isUkPhone(phone):
            return phone
        else:
            raise ValidationError("** use a valid UK format")

