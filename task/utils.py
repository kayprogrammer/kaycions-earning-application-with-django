from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import uuid
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))

generate_token = TokenGenerator()

def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code