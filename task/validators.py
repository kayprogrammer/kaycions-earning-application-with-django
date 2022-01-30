import imp
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from . models import Worker
'''
def fullnameValidator(value):
    qwerty = value.split()
    if len(qwerty) >= 2:
        return value
    else:
        raise ValidationError('Please input at least two names without digits')
'''

full_regex_pattern = RegexValidator(regex=r'^[a-zA-Z]+\s[a-zA-Z]*$', message='Please input only two names without digits or special characters',)

def fullnameValidator(value):
    if len(value) < 6:
        raise ValidationError(_('\'%(value)s\' is too short. (Use 6 chars or more)'), params={'value':value},)
    else:
        return value

def IdValidator(value):
    if not value.startswith('@'):
        raise ValidationError('Invalid Id. Please start with the \'@\' symbol')

def youtubeIdValidator(value):
    if not value.endswith('@gmail.com'):
        raise ValidationError('Invalid Id. Please use a valid Gmail address')

def avatar_size(value):
    limit = 3 * 1024 * 1024
    if value.size != None:
        if value.size > limit:
            raise ValidationError('File too large. Size should not exceed 2 MiB.')

def referrer_exist(value):
    if not Worker.objects.filter(code=value).exists():
        raise ValidationError('Referral code does not exist!')
