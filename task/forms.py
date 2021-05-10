from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext as _


from . validators import *
from . models import *


class SuscribersForm(ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input', 'rows':2, 'placeholder':'Enter your email...'}))

    class Meta:
        model = Suscribers
        fields = '__all__'

class ContactForm(ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Enter your name...'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Enter your email...'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'input', 'rows':3, 'placeholder':'Enter your message...'}))

    class Meta:
        model = Contact
        fields = '__all__'

class WorkersForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        exclude = ['user']

class AdminTaskForm(ModelForm):

    class Meta:
        model = AdminTask
        fields = '__all__'

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=40, help_text='Full name', validators=[full_regex_pattern, fullnameValidator], widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Enter your full name...'}))
    username = forms.CharField(max_length=15, help_text='Username', validators=[usernameValidator], widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Enter your username...'}))
    email = forms.CharField(max_length=40, help_text='Email', widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'Enter your email...'}))
    password1 = forms.CharField(max_length=25, help_text='Password', widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Enter your password...'}))
    password2 = forms.CharField(max_length=25, help_text='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'input', 'placeholder':'Confirm your password...'}))
    twitter_id = forms.CharField(max_length=30, help_text='Twitter ID', validators=[twitterIdValidator], widget=forms.TextInput(attrs={'class':'input', 'placeholder':'e.g @example...'}))
    instagram_id = forms.CharField(max_length=30, help_text='Instagram ID', validators=[instagramIdValidator], widget=forms.TextInput(attrs={'class':'input', 'placeholder':'e.g @example...'}))
    youtube_id = forms.CharField(max_length=40, help_text='Youtube ID', validators=[youtubeIdValidator], widget=forms.EmailInput(attrs={'class':'input', 'placeholder':'e.g example@gmail.com...'}))

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2', 'twitter_id', 'instagram_id', 'youtube_id']

    '''
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
        # Our previous definition was till this line

        password_field = self.fields['password1']
        password_field.validators.append(MinLengthValidator(limit_value=8))
    '''


    def clean_password2(self):
        super(RegisterForm, self).clean()

        # This method will set the `cleaned_data` attribute

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 == password2:
            raise forms.ValidationError('Password Mismatch')
        if len(password1) < 8:
            raise forms.ValidationError('Password is too short')
        return password2



