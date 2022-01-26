from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext as _
from django.utils import timezone

from . validators import *
from . models import *


class SuscribersForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control mr-sm-2', 'type':'email', 'placeholder':'Your email address...'}))

    class Meta:
        model = Suscribers
        fields = ['email']

class ContactForm(ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your name...'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email...'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':'Enter your message...'}))

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class ProfileForm(ModelForm):
    full_name = forms.CharField(max_length=80, validators=[full_regex_pattern, fullnameValidator], widget=forms.TextInput())
    facebook_id = forms.CharField(max_length=80, widget=forms.TextInput())
    twitter_id = forms.CharField(max_length=80, validators=[IdValidator], widget=forms.TextInput())
    instagram_id = forms.CharField(max_length=80, validators=[IdValidator], widget=forms.TextInput())
    youtube_id = forms.EmailField(max_length=80, validators=[youtubeIdValidator], widget=forms.TextInput())
    paypal_address = forms.EmailField(max_length=80, widget=forms.TextInput())
    avatar = forms.ImageField(required=False, validators=[avatar_size], widget=forms.FileInput(attrs={ 'type':'file', 'id':'file', 'size':5, 'class':'input-file' }))

    class Meta:
        model = Worker
        fields = '__all__'
        exclude = ['user', 'email', 'date_created', 'recommended_by', 'updated', 'code']

def date():
    return timezone.now() + timedelta(days=2)

def time():
    return timezone.now() + timedelta(hours=49)

class TaskForm(ModelForm):
    task_expiry_date = forms.DateField(initial = date(), required=False, widget=forms.DateInput(attrs={'type':'date'}))
    task_expiry_time = forms.TimeField(initial = time(), required=False, widget=forms.TimeInput(attrs={'type':'time'}))

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['worker', 'pending', 'completed', 'disapproved']

class WithdrawalForm(ModelForm):

    class Meta:
        model = Withdrawal
        fields = '__all__'
        exclude = ['worker', 'paypal_address', 'amount_withdraw', 'date_created', 'verified']

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=40, help_text='Full name', validators=[full_regex_pattern, fullnameValidator], widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full name...', 'id':'fullnamefield'}))
    email = forms.CharField(max_length=40, help_text='Email', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email address...', 'id':'emailfield'}))
    password1 = forms.CharField(max_length=25, help_text='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password...', 'id':'passwordfield1'}))
    password2 = forms.CharField(max_length=25, help_text='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm password...', 'id':'passwordfield2'}))
    terms_confirmed = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class':'checkbox', }))
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']

    '''
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
        # Our previous definition was till this line

        password_field = self.fields['password1']
        password_field.validators.append(MinLengthValidator(limit_value=8))
    '''

    def clean_password1(self):
        super(RegisterForm, self).clean()

        # This method will set the `cleaned_data` attribute

        password1 = self.cleaned_data.get('password1')
        
        if len(password1) < 8:
            raise forms.ValidationError('Password is too short')
        return password1


    def clean_password2(self):
        super(RegisterForm, self).clean()

        # This method will set the `cleaned_data` attribute

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 == password2:
            raise forms.ValidationError('Password Mismatch')
        return password2



class ComplainForm(ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control mb-2', 'id':'contact', 'placeholder':'Tell us something...'}))
    class Meta:
        model = Complaints
        fields = ['text']
