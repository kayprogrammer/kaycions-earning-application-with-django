from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import random
import string
import uuid
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))

generate_token = TokenGenerator()

def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code

def random_string_generator(size=30, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars))

def unique_code_generator(instance, new_code=None):
    if new_code is not None:
        code = new_code
    else:
        code = str(uuid.uuid4()).replace("-", "")[:30]

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(unique_code=code).exists()
    if qs_exists:
        new_code = "{randstr}".format(
            randstr=random_string_generator(size=30)
        )
        return unique_code_generator(instance, new_code=new_code)
    return code